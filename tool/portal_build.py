#!/usr/bin/env python3
"""Web oyun portalları için tek oyunluk HTML5 paketleri (CrazyGames, Poki …).

    python tool/portal_build.py            # tool/portal_games.json'daki oyunlar

Her oyun için merkezin bağımlılık sabitleriyle (studio_core, motor, oyun
deposu) küçük bir Flutter web projesi kurulur ve
`--dart-define=PORTAL=1` ile derlenir: tek oyun, dış bağlantı yok, satın
alma yok, PWA/service worker yok, CanvasKit ve Roboto yerel (CDN isteği yok),
göreli yollar (`<base href="./">`).

Aynı derlemeden üç paket çıkar (yalnızca index.html farklı):
  <oyun>-crazygames.zip  CrazyGames HTML5 SDK v3 + portal.js köprüsü
  <oyun>-poki.zip        Poki SDK v2 + portal.js köprüsü
  <oyun>-html5.zip       SDK'sız, reklamsız (itch.io / kendi sitesi)

Dart tarafı SDK'yı bilmez: studio_core `Portal` sınıfı yalnızca
`window.gs100Portal` nesnesini çağırır (gameplayStart/Stop, loadingStop,
commercialBreak, rewardedBreak). Ayrıntılar: ship/MASAUSTU_WEB.md.
"""
import gzip
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import yaml

ROOT = os.getcwd()
WORK = os.path.join(ROOT, "build", "portal_app")
DIST = os.path.join(ROOT, "dist", "portal")
FLUTTER = shutil.which("flutter") or "flutter"

SDK = {
    "crazygames": '<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>',
    "poki": '<script src="https://game-cdn.poki.com/scripts/v2/poki-sdk.js"></script>',
}

PORTAL_JS = r"""<script>
/* gs100 portal köprüsü (tool/portal_build.py). Dart: studio_core Portal. */
(function () {
  var kind = '%(kind)s';
  function cg() { return window.CrazyGames && window.CrazyGames.SDK; }
  function pk() { return window.PokiSDK; }
  var ready = Promise.resolve();
  try {
    if (kind === 'crazygames' && cg()) {
      ready = cg().init().then(function () { try { cg().game.loadingStart(); } catch (e) {} }).catch(function () {});
    } else if (kind === 'poki' && pk()) {
      ready = pk().init().catch(function () {});
    }
  } catch (e) {}
  function safe(f) { return function () { ready.then(function () { try { f(); } catch (e) {} }); }; }
  window.gs100Portal = {
    kind: kind,
    loadingStop: safe(function () {
      if (kind === 'crazygames' && cg()) cg().game.loadingStop();
      if (kind === 'poki' && pk()) pk().gameLoadingFinished();
    }),
    gameplayStart: safe(function () {
      if (kind === 'crazygames' && cg()) cg().game.gameplayStart();
      if (kind === 'poki' && pk()) pk().gameplayStart();
    }),
    gameplayStop: safe(function () {
      if (kind === 'crazygames' && cg()) cg().game.gameplayStop();
      if (kind === 'poki' && pk()) pk().gameplayStop();
    }),
    commercialBreak: function () { return brk(false); },
    rewardedBreak: function () { return brk(true); }
  };
  function brk(rewarded) {
    return ready.then(function () {
      return new Promise(function (resolve) {
        try {
          if (kind === 'crazygames' && cg()) {
            cg().ad.requestAd(rewarded ? 'rewarded' : 'midgame', {
              adStarted: function () {},
              adFinished: function () { resolve(true); },
              adError: function () { resolve(false); }
            });
          } else if (kind === 'poki' && pk()) {
            (rewarded ? pk().rewardedBreak() : pk().commercialBreak().then(function () { return true; }))
              .then(function (ok) { resolve(!!ok); }, function () { resolve(false); });
          } else {
            resolve(false);
          }
        } catch (e) { resolve(false); }
      });
    });
  }
  // Ok tuşları ve boşluk sayfayı kaydırmasın (metin alanları hariç).
  window.addEventListener('keydown', function (e) {
    var t = e.target || {};
    if (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable) return;
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].indexOf(e.key) >= 0) e.preventDefault();
  }, { passive: false });
})();
</script>
"""

STYLE = """<style>
  html, body { margin: 0; height: 100%; overflow: hidden; overscroll-behavior: none; background: #000;
    -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;
    -webkit-tap-highlight-color: transparent; }
</style>
"""


def run(cmd, cwd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def hub_pubspec():
    with open(os.path.join(ROOT, "pubspec.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_project(game, hub):
    pkg = game["id"].replace("-", "_")
    deps = hub["dependencies"]
    spec = {
        "name": "gs100_portal",
        "description": "Portal paketi: %s" % game["id"],
        "publish_to": "none",
        "version": "1.0.0+1",
        "environment": hub.get("environment", {"sdk": ">=3.6.0 <4.0.0"}),
        "dependencies": {
            "flutter": {"sdk": "flutter"},
            "studio_core": deps["studio_core"],
            pkg: deps[pkg],
        },
        "dependency_overrides": hub.get("dependency_overrides") or {},
        "flutter": {"uses-material-design": True, "assets": []},
    }
    for d in ("sfx", "config"):
        src = os.path.join(ROOT, "assets", d)
        dst = os.path.join(WORK, "assets", d)
        shutil.rmtree(dst, ignore_errors=True)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
            spec["flutter"]["assets"].append("assets/%s/" % d)
    with open(os.path.join(WORK, "pubspec.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(spec, f, sort_keys=False, allow_unicode=True)
    with open(os.path.join(WORK, "lib", "main.dart"), "w", encoding="utf-8") as f:
        f.write(
            "// Portal paketi (tool/portal_build.py üretir).\n"
            "import 'package:%s/%s.dart';\n"
            "import 'package:studio_core/studio_core.dart';\n\n"
            "void main() => bootstrap(%s);\n" % (pkg, pkg, game["config"])
        )


def bundle_roboto(web):
    """Flutter web varsayılan yazı tipini (Roboto) fonts.gstatic.com'dan çeker;
    portallar dış isteği engeller. Dosya pakete konur ve FontManifest'e
    eklenir: motor yerel 'Roboto' ailesini görünce dışarı gitmez."""
    js = open(os.path.join(web, "main.dart.js"), encoding="utf-8", errors="ignore").read()
    m = re.search(r"https://fonts\.gstatic\.com/s/roboto/[A-Za-z0-9_./-]+\.(?:ttf|woff2?)", js)
    if m:
        url = m.group(0)
    else:
        # Yeni motor: adres fontFallbackBaseUrl + "roboto/vNN/....woff2" diye birleştirilir.
        m = re.search(r"roboto/v\d+/[A-Za-z0-9_-]+\.(?:ttf|woff2?)", js)
        if not m:
            print("::warning::Roboto adresi main.dart.js'te bulunamadı; yazı tipi paketlenmedi.")
            for hit in sorted(set(re.findall(r"[^\"']{0,40}(?:gstatic|roboto)[^\"']{0,60}", js)))[:10]:
                print("  ipucu:", hit)
            return
        url = "https://fonts.gstatic.com/s/" + m.group(0)
    ext = url.rsplit(".", 1)[1]
    os.makedirs(os.path.join(web, "assets", "fonts"), exist_ok=True)
    rel = "fonts/Roboto-Regular." + ext
    with urllib.request.urlopen(url, timeout=60) as r, open(os.path.join(web, "assets", rel), "wb") as f:
        f.write(r.read())
    fm_path = os.path.join(web, "assets", "FontManifest.json")
    fm = json.load(open(fm_path, encoding="utf-8")) if os.path.exists(fm_path) else []
    if not any(x.get("family") == "Roboto" for x in fm):
        fm.append({"family": "Roboto", "fonts": [{"asset": rel}]})
        json.dump(fm, open(fm_path, "w", encoding="utf-8"))
    print("Roboto paketlendi:", url)


def clean(web, title):
    for name in ("flutter_service_worker.js", ".last_build_id", "manifest.json"):
        p = os.path.join(web, name)
        if os.path.exists(p):
            os.remove(p)
    ck = os.path.join(web, "canvaskit")
    if os.path.isdir(ck):
        for root, _, files in os.walk(ck):
            for f in files:
                # skwasm yalnızca --wasm derlemesinde kullanılır.
                if f.startswith("skwasm") or f.endswith(".symbols"):
                    os.remove(os.path.join(root, f))
    icons = os.path.join(web, "icons")
    shutil.rmtree(icons, ignore_errors=True)
    index = os.path.join(web, "index.html")
    s = open(index, encoding="utf-8").read()
    s = re.sub(r'<base href="[^"]*">', '<base href="./">', s)
    s = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % title, s)
    s = re.sub(r'\s*<link rel="manifest"[^>]*>', "", s)
    s = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>', "", s)
    s = re.sub(r'\s*<meta name="apple-mobile-web-app[^>]*>', "", s)
    s = s.replace("</head>", STYLE + "</head>", 1)
    open(index, "w", encoding="utf-8").write(s)


def variant(web, out_dir, kind):
    shutil.rmtree(out_dir, ignore_errors=True)
    shutil.copytree(web, out_dir)
    index = os.path.join(out_dir, "index.html")
    s = open(index, encoding="utf-8").read()
    head = ""
    if kind in SDK:
        head = SDK[kind] + "\n" + PORTAL_JS % {"kind": kind}
    else:
        # SDK'sız paket: köprü nesnesi yok -> reklam düğmeleri hiç görünmez.
        head = ""
    s = s.replace("<head>", "<head>\n" + head, 1) if head else s
    open(index, "w", encoding="utf-8").write(s)


def sizes(path):
    raw = gz = n = 0
    for root, _, files in os.walk(path):
        for f in files:
            b = open(os.path.join(root, f), "rb").read()
            raw += len(b)
            gz += len(gzip.compress(b, 9))
            n += 1
    return raw, gz, n


def zip_dir(src, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, _, files in os.walk(src):
            for f in sorted(files):
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, src))


def main():
    games = json.load(open(os.path.join(ROOT, "tool", "portal_games.json"), encoding="utf-8"))
    only = set(sys.argv[1:])
    hub = hub_pubspec()
    os.makedirs(DIST, exist_ok=True)
    if not os.path.isdir(WORK):
        run([FLUTTER, "create", "--platforms=web", "--org", "com.gamestudio100", "--project-name", "gs100_portal", WORK], ROOT)
    shutil.rmtree(os.path.join(WORK, "test"), ignore_errors=True)
    rows = []
    for game in games:
        if only and game["id"] not in only:
            continue
        write_project(game, hub)
        run([FLUTTER, "pub", "get"], WORK)
        run([FLUTTER, "build", "web", "--release", "--no-web-resources-cdn", "--dart-define=PORTAL=1",
             "--dart-define=EDITION=portal", "--base-href", "/"], WORK)
        web = os.path.join(WORK, "build", "web")
        clean(web, game.get("title", game["id"]))
        bundle_roboto(web)
        for kind in ("crazygames", "poki", "html5"):
            out = os.path.join(DIST, "%s-%s" % (game["id"], kind))
            variant(web, out, kind)
            zip_dir(out, out + ".zip")
            shutil.rmtree(out)
        raw, gz, n = sizes(web)
        big = sorted(((os.path.getsize(os.path.join(r, f)), os.path.relpath(os.path.join(r, f), web))
                      for r, _, fs in os.walk(web) for f in fs), reverse=True)[:8]
        print("En büyük dosyalar:", ", ".join("%s %.1f MB" % (p, b / 1048576.0) for b, p in big))
        zsize = os.path.getsize(os.path.join(DIST, "%s-html5.zip" % game["id"]))
        rows.append((game["id"], raw, gz, zsize, n))
        shutil.rmtree(os.path.join(WORK, "build"), ignore_errors=True)
    mb = lambda b: "%.1f MB" % (b / 1048576.0)
    lines = ["| Oyun | Ham boyut | gzip (aktarım) | zip | Dosya |", "|---|---|---|---|---|"]
    for gid, raw, gz, z, n in rows:
        lines.append("| %s | %s | %s | %s | %d |" % (gid, mb(raw), mb(gz), mb(z), n))
    lines += ["", "Sınırlar: CrazyGames ilk indirme <= 50 MB (mobil ana sayfa <= 20 MB), en çok 1500 dosya;"
              " Poki hedefi ilk indirme < 8 MB."]
    report = "\n".join(lines) + "\n"
    open(os.path.join(DIST, "SIZES.md"), "w", encoding="utf-8").write(report)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        open(summary, "a", encoding="utf-8").write("## Portal paketleri\n\n" + report)


if __name__ == "__main__":
    main()

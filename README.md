# Kelime Oyunları · Word Games (merkez-kelime-oyunlari)

Kelime ailesinin **merkez uygulaması**: 34 oyunu ve 8 çeşitlik tahmin paketini tek mağaza uygulamasında toplar. Her oyun kendi deposundadır; ortak motor [kelime-motoru](https://github.com/taktemurr-ops/kelime-motoru), ortak çekirdek [studio-core](https://github.com/taktemurr-ops/studio-core). Kelime listeleri: FrequencyWords (OpenSubtitles 2018, CC BY-SA 4.0), uygunsuz kelime süzgeci LDNOOBW (CC BY 4.0).

## Günün Bulmacası (küresel günlük meydan okuma)

Ana sayfadaki kart ve menüdeki **Günün Bulmacası**: katılan her oyunda dünyadaki herkes aynı UTC gününde aynı bulmacayı çözer (tohum yalnızca oyun + gün; motor bölümü verir, `GameRules.globalDailySpec`). Günün ilk çözümü sıralamaya girer (süre/hamle ya da puan), seri ve en iyi seri tutulur, sonuç bulmacayı ele vermeyen emoji izli metinle paylaşılır. Çevrimdışı çözülen sonuç cihazda bekler, bağlantı gelince gönderilir (Firestore `daily/{tablo}/results/{uid}`, kurallar ve emülatör testleri studio-core'da).

## Aile Turnuvası

Menüdeki **Aile Turnuvası** (Parti ve Aile merkezinde ana sayfada da): aynı cihazda 2–8 kişi, merkezin oyunlarından seçilenlerle 1–5 tur. Sırayla oynanan oyunlarda herkes aynı bölümü oynar (1.: 3, 2.: 2, 3.: 1 puan); birlikte oynanan oyunlarda kalabalık aileler gruplara ayrılır. Puan tablosu, şampiyon töreni ve kaldığı yerden devam; çevrimiçi bağlantı, reklam ya da kişisel bilgi yok (takma adlar yalnızca cihazda).

| Oyun | Depo |
|---|---|
| Çengel Bulmaca | [oyun-cengel-bulmaca](https://github.com/taktemurr-ops/oyun-cengel-bulmaca) |
| Kare Bulmaca | [oyun-kare-bulmaca](https://github.com/taktemurr-ops/oyun-kare-bulmaca) |
| Şifreli Bulmaca | [oyun-sifreli-bulmaca](https://github.com/taktemurr-ops/oyun-sifreli-bulmaca) |
| Kriptogram | [oyun-kriptogram](https://github.com/taktemurr-ops/oyun-kriptogram) |
| Kelime Sudoku | [oyun-kelime-sudoku](https://github.com/taktemurr-ops/oyun-kelime-sudoku) |
| Kelime Kafesi | [oyun-kelime-kafesi](https://github.com/taktemurr-ops/oyun-kelime-kafesi) |
| Akrostiş | [oyun-akrostis](https://github.com/taktemurr-ops/oyun-akrostis) |
| Kelime Avı | [oyun-kelime-avi](https://github.com/taktemurr-ops/oyun-kelime-avi) |
| Harf Çarkı | [oyun-kelime-turetme](https://github.com/taktemurr-ops/oyun-kelime-turetme) |
| Kelime Yığını | [oyun-kelime-yigini](https://github.com/taktemurr-ops/oyun-kelime-yigini) |
| Harf Peteği | [oyun-petege-harf](https://github.com/taktemurr-ops/oyun-petege-harf) |
| Harf Izgarası | [oyun-harf-izgarasi](https://github.com/taktemurr-ops/oyun-harf-izgarasi) |
| Kelime Blokları | [oyun-kelime-bloklari](https://github.com/taktemurr-ops/oyun-kelime-bloklari) |
| Kelime Yapbozu | [oyun-kelime-yapbozu](https://github.com/taktemurr-ops/oyun-kelime-yapbozu) |
| Eksik Harfler | [oyun-bosluk-doldurma](https://github.com/taktemurr-ops/oyun-bosluk-doldurma) |
| Beş Harf | [oyun-5-harfli-kelime-tahmini](https://github.com/taktemurr-ops/oyun-5-harfli-kelime-tahmini) |
| Kelime Tahmini Paketi (8) | [oyun-kelime-tahmini-cesit-paketi](https://github.com/taktemurr-ops/oyun-kelime-tahmini-cesit-paketi) |
| Yaprak Tahmini | [oyun-adam-asmaca](https://github.com/taktemurr-ops/oyun-adam-asmaca) |
| Kelime Merdiveni | [oyun-kelime-merdiveni](https://github.com/taktemurr-ops/oyun-kelime-merdiveni) |
| Harf Kaydırma | [oyun-harf-kaydirma](https://github.com/taktemurr-ops/oyun-harf-kaydirma) |
| Hızlı Klavye | [oyun-klavye-hiz-oyunu](https://github.com/taktemurr-ops/oyun-klavye-hiz-oyunu) |
| Düşen Harfler | [oyun-dusen-harfler](https://github.com/taktemurr-ops/oyun-dusen-harfler) |
| Anagram Yarışı | [oyun-ters-kelime-anagram-yarisi](https://github.com/taktemurr-ops/oyun-ters-kelime-anagram-yarisi) |
| Eş ve Zıt | [oyun-es-zit-anlam-eslestirme](https://github.com/taktemurr-ops/oyun-es-zit-anlam-eslestirme) |
| Dörtlü Gruplar | [oyun-kelime-gruplama](https://github.com/taktemurr-ops/oyun-kelime-gruplama) |
| Atasözü Tamamla | [oyun-atasozu-ve-deyim-tamamlama](https://github.com/taktemurr-ops/oyun-atasozu-ve-deyim-tamamlama) |
| Doğru Yazım | [oyun-heceleme-ve-yazim](https://github.com/taktemurr-ops/oyun-heceleme-ve-yazim) |
| Kelime Tahtası | [oyun-kelime-kurma-tahtasi](https://github.com/taktemurr-ops/oyun-kelime-kurma-tahtasi) |
| Kelime Düellosu | [oyun-kelime-duellosu](https://github.com/taktemurr-ops/oyun-kelime-duellosu) |
| Kelime Zinciri | [oyun-kelime-zinciri](https://github.com/taktemurr-ops/oyun-kelime-zinciri) |
| Harf ve Sayı Yarışı | [oyun-harf-ve-sayi-yarisi](https://github.com/taktemurr-ops/oyun-harf-ve-sayi-yarisi) |
| Dört Resim Bir Kelime | [oyun-dort-resim-bir-kelime](https://github.com/taktemurr-ops/oyun-dort-resim-bir-kelime) |
| Beş İpucu | [oyun-bes-ipucu](https://github.com/taktemurr-ops/oyun-bes-ipucu) |
| Harf Kutusu | [oyun-harf-kutusu](https://github.com/taktemurr-ops/oyun-harf-kutusu) |
| Tema Avı | [oyun-kelime-avi](https://github.com/taktemurr-ops/oyun-kelime-avi) (kip) |

Test APK: https://github.com/taktemurr-ops/merkez-kelime-oyunlari/releases/download/test/merkez-kelime-oyunlari.apk

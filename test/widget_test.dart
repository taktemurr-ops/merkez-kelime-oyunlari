import 'package:flutter_test/flutter_test.dart';
import 'package:merkez_kelime_oyunlari/main.dart';

void main() {
  test('merkezde oyunlar benzersiz kimlikle yer alıyor', () {
    final ids = hubConfig.games.map((g) => g.gameId).toList();
    expect(ids, [
      'oyun-cengel-bulmaca',
      'oyun-kare-bulmaca',
      'oyun-sifreli-bulmaca',
      'oyun-kriptogram',
      'oyun-kelime-sudoku',
      'oyun-kelime-kafesi',
      'oyun-akrostis',
      'oyun-kelime-avi',
      'oyun-kelime-turetme',
      'oyun-kelime-yigini',
      'oyun-petege-harf',
      'oyun-harf-izgarasi',
      'oyun-kelime-bloklari',
      'oyun-kelime-yapbozu',
      'oyun-bosluk-doldurma',
      'oyun-5-harfli-kelime-tahmini',
      'oyun-adam-asmaca',
      'oyun-kelime-merdiveni',
      'oyun-harf-kaydirma',
      'oyun-klavye-hiz-oyunu',
      'oyun-dusen-harfler',
      'oyun-ters-kelime-anagram-yarisi',
      'oyun-es-zit-anlam-eslestirme',
      'oyun-kelime-gruplama',
      'oyun-atasozu-ve-deyim-tamamlama',
      'oyun-heceleme-ve-yazim',
      'oyun-kelime-kurma-tahtasi',
      'oyun-kelime-duellosu',
      'oyun-kelime-zinciri',
      'oyun-harf-ve-sayi-yarisi',
    ]);
    final all = hubConfig.allGames.map((g) => g.gameId).toList();
    expect(all.length, ids.length + 8);
    expect(all.toSet().length, all.length);
    expect(ids.toSet().length, ids.length);
    for (final g in hubConfig.allGames) {
      expect(g.rules.gameId, g.gameId, reason: 'kayıt öneki oyun kimliğiyle aynı olmalı');
    }
    expect(hubConfig.title.length, 33);
    expect(hubConfig.tagline.length, 33);
  });

  test('her oyun ve grup bir bölüm başlığı altında', () {
    final ids = {for (final s in hubConfig.sections) ...s.ids};
    for (final g in hubConfig.games) {
      expect(ids.contains(g.gameId), isTrue, reason: g.gameId);
    }
    for (final g in hubConfig.groups) {
      expect(ids.contains(g.id), isTrue, reason: g.id);
    }
    for (final s in hubConfig.sections) {
      expect(s.title.length, 33);
    }
  });
}

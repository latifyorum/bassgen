# bassgen

Akor dizisi girer, bassline MIDI çıkar. bassgen, yazdığın ya da MIDI olarak verdiğin bir akor dizisi için çok sayıda bassline varyantı üretir. Dinler, birini seçer ve DAW'ında düzenlersin. Parçayı kendin yazmanın yerine geçmez, yaratıcı blokajı kırmak için bir başlangıç noktasıdır.

English: [README.md](README.md)

## Özellikler

- Giriş: yazılmış akorlar (`Am F7 C Gsus Dm:2`) veya akor MIDI dosyası
- Tür presetleri: **trap (808)**, **rock**, **metal** ve trap ritmi + rock notalarından oluşan **hybrid**
- Role göre etiketli notalar (kök, beşli, oktav, yaklaşma, gerilim), her stilin menziline oturtulur
- Yerel web arayüzü: piano roll önizleme, tarayıcıda dinleme, MIDI indirme
- Seed'li ve tekrarlanabilir: aynı seed aynı sonucu verir
- Saf Python, tek bağımlılık [mido](https://github.com/mido/mido)

## Hızlı başlangıç

```bash
git clone https://github.com/latifyorum/bassgen.git
cd bassgen
pip install -e .

bassgen-web                       # http://127.0.0.1:8765 adresini açar
```

Komut satırı:

```bash
bassgen --text "Am F C G" --style rock --n 8 --out out
bassgen --chords examples/am_f_c_g.mid --style metal --template gallop --bars 8 --seed 7
```

Kurmadan çalıştırmak için: `pip install mido`, ardından `python -m bassgen.web` veya `python -m bassgen ...`.

## Stiller

| Stil | Ritim | Notalar | Menzil |
|---|---|---|---|
| `trap` | Boşluklu, uzun 808 notaları, her 4. barda küçük fill | kök, beşli, oktav | E1-G2 |
| `rock` | 8'lik motor, itişli ve senkoplu kalıplar | kök, beşli, oktav, sonraki akora yarım ton yaklaşma | E1-D#3 |
| `metal` | Pedal 8'lik/16'lık, gallop, chug, kısa staccato notalar | çoğunlukla kök, nadiren b2 gerilimi | C1-F2 |
| `hybrid` | Trap ritimleri | Rock tarzı nota seçimi | E1-C3 |

Stiller `bassgen/styles.py` içinde düz veri olarak duruyor. Kendi stilini eklemek için yeni bir `Style(...)` satırı yazman yeter.

## Nasıl çalışır

```
akorlar -> parser -> ritim (şablonlar) -> perde (roller) -> MIDI çıktısı
                  \_______ her aşamayı tek bir Style preset'i yönetir _______/
```

## Sınırlar ve yol haritası

- Kök tespiti basit bir triad şablon eşleştirmesi, slash akorlar (`C/E`) henüz desteklenmiyor
- Ritim yalnızca şablonlardan geliyor. Planlanan: ritmi kick veya gitar riff MIDI'sine kilitlemek
- Planlanan: varyant puanlama (kick çakışması, uyum, yoğunluk), 808 için slide ve ghost note

## Lisans

MIT, bkz. [LICENSE](LICENSE).

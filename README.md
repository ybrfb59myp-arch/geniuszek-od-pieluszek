# Geniuszek od Pieluszek – losuj słowo

Prosta aplikacja do kart edukacyjnych „Geniuszek od Pieluszek”.
Wybierasz długość słowa (3, 4, 5, 6, 7, 8 albo 9+ liter, albo „Losowa długość”), naciskasz **Losuj słowo**, a słowo pojawia się
ułożone z kart tak jak na stole: pierwsza karta w całości (np. „Dd”), z kolejnych widać małą literę.

Dwuznaki i zmiękczenia układane są z jednej karty, tak jak w talii:
`ch cz sz rz dz dż dź dzi ci si zi ni` – np. „ciasto” = **ci** · a · s · t · o.

## Ustawienia (pod przyciskiem ⚙ Ustawienia)

- **Tylko słowa, które da się ułożyć z jednego zestawu kart** (domyślnie włączone) – w talii
  podwójne są tylko A, E, I, M, O, T; pozostałe karty występują raz.
- **Bez dwuznaków i zmiękczeń** – same pojedyncze litery (przed etapem 4 metody).

„Losowa długość” najpierw losuje długość (każda tak samo często), potem słowo.
Słowa losowane są bez powtórzeń, dopóki nie przejdzie się całej puli.
Spacja lub Enter też losuje kolejne słowo.

## Pliki

- `index.html` – cała aplikacja
- `slowa.js` – listy słów (generowane)
- `ikony/`, `manifest.webmanifest` – ikona aplikacji (okrągłe logo) do karty przeglądarki i ekranu głównego
- `karty/` – obrazy kart z literami, wyrenderowane z PDF-a zestawu kart (C7)
- `narzedzia/build_words.py` – listy słów do edycji; po zmianie:
  `python3 narzedzia/build_words.py slowa.js`

## Uruchomienie

Wystarczy otworzyć `index.html` przez dowolny serwer WWW (np. GitHub Pages:
Settings → Pages → Deploy from a branch → `main` / root).
Lokalnie: `python3 -m http.server` i wejść na http://localhost:8000.

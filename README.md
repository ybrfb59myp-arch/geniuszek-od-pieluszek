# Geniuszek od Pieluszek – losuj słowo

Prosta aplikacja do kart edukacyjnych „Geniuszek od Pieluszek”.
Wybierasz długość słowa (3, 4, 5, 6, 7, 8 albo 9+ liter, albo „Losowa długość”), naciskasz **Losuj słowo**, a słowo pojawia się
ułożone z kart tak jak na stole: pierwsza karta w całości (np. „Dd”), z kolejnych widać małą literę.

Dwuznaki i zmiękczenia układane są z jednej karty, tak jak w talii:
`ch cz sz rz dz dż dź dzi ci si zi ni` – np. „ciasto” = **ci** · a · s · t · o.

## Ustawienia (pod przyciskiem ⚙ Ustawienia)

- **Tylko słowa, które da się ułożyć z dwóch zestawów kart** (domyślnie włączone) – w jednej talii
  podwójne są tylko A, E, I, M, O, T; pozostałe karty występują raz. Liczbę talii ustawia
  `TALIE` w `narzedzia/build_words.py`.
- **Bez dwuznaków i zmiękczeń** – same pojedyncze litery (przed etapem 4 metody).

„Losowa długość” najpierw losuje długość (każda tak samo często), potem słowo.
Słowa losowane są bez powtórzeń, dopóki nie przejdzie się całej puli.
Spacja lub Enter też losuje kolejne słowo.

## Pliki

- `index.html` – cała aplikacja
- `slowa.js` – listy słów (generowane, nie edytować ręcznie)
- `ikony/`, `manifest.webmanifest` – ikona aplikacji (okrągłe logo) do karty przeglądarki i ekranu głównego
- `karty/` – obrazy kart z literami, wyrenderowane z PDF-a zestawu kart (C7)
- `narzedzia/slowa.txt` – lista słów do edycji (ok. 2800 słów, 3+ liter; opis źródeł w nagłówku pliku)
- `narzedzia/build_words.py` – buduje `slowa.js`; po zmianie listy:
  `python3 narzedzia/build_words.py slowa.js`
  (z opcją `--sjp slowa-sjp.txt` sprawdza też każde słowo w słowniku do gier SJP.pl,
  plik do pobrania z https://sjp.pl/sl/growy/)

- `zdania.js` – proste zdania z 3 wyrazów (generowane); tylko takie, które mieszczą się w dwóch taliach
- `narzedzia/build_zdania.py` – buduje `zdania.js` z podmiotów i pasujących do nich wyrażeń
  („kot” + „na stole”, „mama” + „czyta książkę”); po zmianie:
  `python3 narzedzia/build_zdania.py zdania.js --lista narzedzia/zdania-lista.txt`
- `narzedzia/zdania-lista.txt` – wszystkie zdania do przejrzenia (generowane), z oznaczeniem,
  które mieszczą się nawet w jednej talii

## Skąd są słowa

Kandydaci to rzeczowniki w formie podstawowej (słownik PoliMorf), które są w słowniku do gier
SJP.pl, posortowane według tego, jak często występują w języku (napisy filmowe, FrequencyWords).
Z ok. 12 000 najczęstszych wybrane zostały słowa konkretne i znane małym dzieciom; do tego
zdrobnienia i słowa z mowy dziecięcej dopisane według kategorii (zwierzęta, jedzenie, dom…).

## Uruchomienie

Wystarczy otworzyć `index.html` przez dowolny serwer WWW (np. GitHub Pages:
Settings → Pages → Deploy from a branch → `main` / root).
Lokalnie: `python3 -m http.server` i wejść na http://localhost:8000.

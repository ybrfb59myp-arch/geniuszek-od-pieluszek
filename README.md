# Geniuszek od Pieluszek – losuj słowo albo zdanie

Prosta aplikacja do kart edukacyjnych „Geniuszek od Pieluszek”.
Wybierasz długość słowa (3–8 albo 9+ liter, albo „Losowa długość”) lub rodzaj zdania, naciskasz przycisk
losowania, a słowo albo zdanie pojawia się ułożone z kart tak jak na stole: pierwsza karta każdego wyrazu
w całości (np. „Dd”), z kolejnych widać małą literę.

Dwuznaki i zmiękczenia układane są z jednej karty, tak jak w talii:
`ch cz sz rz dz dż dź dzi ci si zi ni` – np. „ciasto” = **ci** · a · s · t · o.

## Talia

Jedna talia ma 51 kart: **A ×3; E, K, M, O, T ×2; pozostałe karty po jednej** (32 litery i 12 dwuznaków).
Skład został wyliczony tak, żeby z jednej talii dało się ułożyć jak najwięcej słów z listy
(ok. 89%, w tym „mama” i „tata”). Ustawia go `KARTY` w `narzedzia/build_words.py`.

## Zdania

- **Zdania krótkie** – 2–3 słowa: „kot śpi”, „mały kot”, „kot na stole”, „mama je zupę”, „to jest kot”,
  „kot i pies”.
- **Zdania długie** – 4–5 słów: „kot śpi na kanapie”, „mały kot pije mleko”, „na stole jest kubek”,
  „mama je zupę w kuchni”, „kot i pies w domu”, „kot jest mały i rudy”.

Zdania układa na bieżąco `generator.js`: losuje podmiot (każdy tak samo często) i dobiera do niego
elementy, które do niego pasują. Mniej więcej **co czwarte zdanie jest śmieszne** – podmiot dostaje
element, który do niego nie pasuje („krowa miauczy na szafie”, „różowy tata znosi jajka”).
Czasowniki są tylko w formie „kot śpi” (3. osoba liczby pojedynczej, czas teraźniejszy).

## Ustawienia (pod przyciskiem ⚙ Ustawienia)

- **Układam z jednej / dwóch talii** (domyślnie z jednej) – pokazuje tylko słowa i zdania, które da się
  ułożyć z tylu talii. Z jednej talii mieści się ok. 89% słów, ok. 28% zdań krótkich i ok. 2% długich;
  z dwóch prawie wszystkie słowa, ok. 93% zdań krótkich i ok. 68% długich.
- **Bez dwuznaków i zmiękczeń** – same pojedyncze litery (przed etapem 4 metody).

„Losowa długość” najpierw losuje długość (każda tak samo często), potem słowo.
Słowa losowane są bez powtórzeń, dopóki nie przejdzie się całej puli.
Spacja lub Enter też losuje.

## Pliki

- `index.html` – aplikacja (wygląd, układ kart, losowanie słów)
- `generator.js` – układanie zdań i sprawdzanie, czy mieszczą się w talii
- `karty/` – obrazy kart z literami, wyrenderowane z PDF-a zestawu kart (C7)
- `ikony/`, `manifest.webmanifest` – ikona aplikacji do karty przeglądarki i ekranu głównego
- pliki generowane (nie edytować ręcznie): `slowa.js` (słowa), `talia.js` (skład talii),
  `zdania.js` (składniki zdań), `zdania-liczby.js` (ile zdań jest w puli)

Do edycji, w `narzedzia/`:

- `slowa.txt` – lista słów (ok. 2800 słów, 3+ liter; opis źródeł w nagłówku pliku). Po zmianie:
  `python3 narzedzia/build_words.py slowa.js`
- `zdania_dane.py` – podmioty zdań i to, co do nich pasuje: miejsca („na stole”), czynności
  („je zupę”), czasowniki („śpi”, „miauczy”) i przymiotniki („mały”, „rudy”), a także zasady dla zdań
  śmiesznych. Po zmianie: `python3 narzedzia/build_zdania.py zdania.js`
  (skrypt uruchamia też `zdania_narzedzie.js`, które liczy pulę i zapisuje przykłady; potrzebny `node`)
- `zdania-przyklady.txt` – po 30 przykładów każdego wzoru zdania, do przejrzenia (generowane)

Oba skrypty z opcją `--sjp slowa-sjp.txt` sprawdzają każdy wyraz w słowniku do gier SJP.pl
(plik do pobrania z https://sjp.pl/sl/growy/).

## Skąd są słowa

Kandydaci to rzeczowniki w formie podstawowej (słownik PoliMorf), które są w słowniku do gier
SJP.pl, posortowane według tego, jak często występują w języku (napisy filmowe, FrequencyWords).
Z ok. 12 000 najczęstszych wybrane zostały słowa konkretne i znane małym dzieciom; do tego
zdrobnienia i słowa z mowy dziecięcej dopisane według kategorii (zwierzęta, jedzenie, dom…).

## Uruchomienie

Wystarczy otworzyć `index.html` przez dowolny serwer WWW (np. GitHub Pages:
Settings → Pages → Deploy from a branch → `main` / root).
Lokalnie: `python3 -m http.server` i wejść na http://localhost:8000.

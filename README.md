CalcEx to prosty program do zarządzania fakturami, który umożliwia użytkownikowi wprowadzanie danych dotyczących faktur, obliczanie różnicy kursowej między kwotą faktury a kwotą płatności oraz przeglądanie historii wprowadzonych faktur.

Funkcje
Wprowadzanie faktury: Użytkownik może wprowadzić dane dotyczące faktury, takie jak kwota, waluta i data wystawienia.
Obliczanie różnicy kursowej: Aplikacja oblicza różnicę kursową między kwotą faktury a kwotą płatności, uwzględniając kurs wymiany walut.
Zapisywanie faktur: Wprowadzone faktury są zapisywane do pliku tekstowego w celu późniejszego przeglądu.
Sprawdzanie historii faktur: Użytkownik może przeglądać historię wprowadzonych faktur z pliku.

Instalacja
Aby zainstalować i uruchomić aplikację, wykonaj następujące kroki:

Sklonuj repozytorium na swój lokalny komputer:

```
git clone https://github.com/twoje-konto/calcex.git
```

Przejdź do katalogu z aplikacją:

```
cd calcex
```
Zainstaluj wymagane biblioteki za pomocą pip:

```
pip install -r requirements.txt
```

Uruchom aplikację:
```
python calcex.py
```

Korzystanie
Po uruchomieniu aplikacji użytkownik będzie proszony o wybór jednej z dostępnych opcji:

Wprowadzić fakturę 

Sprawdzić historię wprowadzonych faktur

Uzyskać Pomoc

Wyjść z programu

Następnie użytkownik będzie prowadzony przez kolejne kroki zgodnie z wybraną opcją.

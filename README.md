# NorthwindAPI

NorthwindAPI to projekt pozwalający na pozyskiwanie danych o sumie sprzedaży z danych dni, wraz z możliwością przeliczenia tych wartości na złotówki po kursie z danego dnia. 
Możliwe jest takźe uzyskanie samego interesującego nas kursu.

## Pliki
- _exchange_rates_acquirer.py_ - odpowiada za pobieranie kursów ze strony nbp.pl jak i ich odpowiednie formatowanie
- _table_manipulator.py_ - plik dodający dane o kursach i sumie sprzedaży do bazy danych
- _app.py_ - właściwa aplikacja udostępniająca API
- _Northwind.sqlite_ - baza danych Northwind, do pobrania tutaj: https://github.com/jpwhite3/northwind-SQLite3 (Northwind_large.sqlite.zip)
- pliki w folderach: _templates_ i _static_ - pliki odpowiedzialne za wyświetlanie i obsługę strony

Wszystkie pliki należy umieścić w jednym folderze

## Instalacja
Do działania aplikacji potrzebny jest Python, którego można pobrać z, przykładow: https://www.anaconda.com/products/individual. 
Następnie korzystając z polecenia "pip install <nazwa>" dodajemy brakujące biblioteki.
- Flask_Limiter (pip install Flask_Limiter)
- Flask-Caching (pip install Flask-Caching)

Dostępnych jest wiele różnych dystrybucji Pythona, więc w niektórych przypadkach może być wymagane doinstalowanie dodatkowych bibliotek, takich jak:
- requests
- Flask

## Uruchomienie
Przed uruchomieniem właściwej aplikacji app.py należy uruchomić plik table_manipulator.py, który doda i zapełni nowe tabele w bazie danych Northwind.
Następnie należy uruchomić plik app.py, podczas którego działania dostępne jest API.

## API
### /api/exchangerates/{date}
### /api/exchangerates/{start_date}/{end_date}
Powyższe zapytania w polu 'result' zwracają informacje o znalezionych kursach dolara do złotówki. 
Żądanie z pojedynczą datą zwróci przelicznik z danego dnia, żądanie z dwoma zwróci dane z podanego zakresu (włacznie z <end_date>).
Dla każdego pola w 'result' dostępne są trzy informacje:
- **date** - data 
- **rate** - kurs z danego dnia
- **is_interpolated** - true, jeżeli w danym dniu nie był dostępny kurs (kurs jest wtedy z poprzedniego dostępnego dnia); w innym przypadku false

Oprócz tego w odpowiedzi znajdują się użyte w żądaniu wartości (date lub start_date z end_date).

### /api/sum/{currency}/{date}
### /api/sum/{currency}/{start_date}/{end_date}
Te żądania zwracają sumę wartości transakcji z danego dnia. W polu 'result' dostępne są zwrócone wyniki, gdzie 
- **date** - data
- **sum** - suma wartości transakcji z danego dnia

Oprócz tego w odpowiedzi znajdują się użyte w żądaniu wartości (date lub start_date z end_date).

##  Ograniczenia API
### date, start_date, end_date
Daty powinny być w formacie RRRR-MM-DD. 
Przy miesiącach jednocyfrowych możliwe jest pominięcie zera przy wpisywaniu miesiąca ("2014-01-13" jest równoważne "2014-1-13").
W żądaniach korzystających ze start_date i end_date, end_date nie może wystąpić przed start_date.
W przypadku błędnego formatu daty lub złej kolejności dat w zakresie, zostanie zwrócony kod błędu: 400.
Daty w bazie danych pochodzą z okresu od 2012-07-01 do 2016-02-29. Możliwe jest jednak zapytanie o daty spoza tego zakresu, wtedy daty spoza zakresu w bazie nie zostaną uwzględnione.
Przykładowo, zapytanie o dane między 2012-05-10 do 2012-07-03, zwróci dane od 2012-07-01 do 2012-07-03. 
Zapytanie przy użyciu tylko jednej daty, jeżeli jest ona spoza zakresu, zwróci pusty wynik.

### currency
Dostępne są jedynie dwie waluty do wyboru: PLN (złotówki) i USD (dolary amerykańskie).
Wielkość liter nie ma tutaj znaczenia: "PLN", "pln", "pLn" są sobie równoważne.
W przypadku błędnie podanej waluty, zostanie zwrócony kod błędu: 400.

### liczba żądań
Możliwe jest wysłanie 20 żądań na minutę, liczone osobno dla każdego użytkownika. W przypadku przkroczeniu limitu otrzymamy wynik: Too Many Requests.

## Przykładowe zapytania
`/api/exchangerates/2015-12-31` - zapytanie o przelicznik dolarów na złotówki w dniu 2015-12-31

`/api/exchangerates/2015-12-12/2015-12-24` - zapytanie o przelicznik dolarów na złotówki w dniach od 2015-12-12 do 2015-12-24 (włącznie)

`/api/sum/usd/2015-04-5` - zapytanie o sumę transakcji w dniu 2015-04-05, wartości podane w dolarach

`/api/sum/pln/2013-03-04/2013-4-18` - zapytanie o sumę transakcji z zakresu od 2013-03-04 do 2013-4-18 (włacznie), wartości podane w złotówkach

## Cache
W programie używany jest system cache używający Flask-Caching. 
W przypadku wywoływania żądań z jedną, konkretną datą, wynik działania jest przechowywany w pamięci przez 5 minut - ponowienie takiego żądania nie wywołuje połączenia z bazą danych.
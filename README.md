# System zarządzania sklepem komputerowym

## 1. Instalacja bibliotek
![Kod instalacji bibliotek](img/1.png)
```python
def sprawdz_biblioteki():
    wymagane_biblioteki = {
        'mysql-connector-python': 'mysql.connector',
        'colorama': 'colorama'
    }
```

## 2. Połączenie z bazą danych 
![Kod połączenia z bazą](img/2.png)
```python
class BazaDanych:
    def __init__(self):
        self.polaczenie = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sklep"
        )
```

## 3. Zarządzanie klientami
![Kod zarządzania klientami](img/3.png)
Funkcje do wyświetlania i wyszukiwania klientów w systemie.

## 4. Obsługa zamówień
![Kod obsługi zamówień](img/4.png)
Implementacja funkcji do zarządzania zamówieniami i obliczania ich wartości.

## 5. Eksport danych
![Kod eksportu danych](img/5.png)
System eksportu danych z bazy do plików CSV.

## 6. Menu główne
![Kod menu głównego](img/6.png)
Implementacja interaktywnego menu użytkownika.

## 7. Struktura programu
![Struktura programu](img/7.png)
Kompletna struktura aplikacji z podziałem na moduły.

## Instalacja i uruchomienie

1. Wymagania:
- Python 3.x
- MySQL Server

2. Instalacja zależności:
```bash
pip install mysql-connector-python colorama
```

3. Import schematu bazy danych:
```sql
source baza_sklep.sql
```

4. Uruchomienie aplikacji:
```bash
python sklep.py
```

## Autor
[Twoje imię i nazwisko]

## Licencja
MIT License
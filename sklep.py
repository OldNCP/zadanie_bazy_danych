import importlib
import subprocess
import sys

def sprawdz_biblioteki():
    """Sprawdza i instaluje wymagane biblioteki."""
    wymagane_biblioteki = {
        'mysql-connector-python': 'mysql.connector',
        'colorama': 'colorama'
    }
    
    for paczka, nazwa_importu in wymagane_biblioteki.items():
        if importlib.util.find_spec(nazwa_importu) is None:
            print(f"Instalowanie biblioteki {paczka}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", paczka])
                print(f"Biblioteka {paczka} została zainstalowana pomyślnie!")
            except subprocess.CalledProcessError:
                print(f"Błąd podczas instalacji {paczka}!")
                exit(1)

# Sprawdzenie i instalacja bibliotek
sprawdz_biblioteki()

# Importy
import mysql.connector
import csv
from datetime import datetime
from colorama import init, Fore, Style

init()  # Initialize colorama

class BazaDanych:
    """Klasa obsługująca operacje na bazie danych sklepu."""
    
    def __init__(self):
        """Inicjalizacja połączenia z bazą danych."""
        try:
            self.polaczenie = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sklep"
            )
            self.kursor = self.polaczenie.cursor()
        except mysql.connector.Error as err:
            print(f"Błąd połączenia: {err}")
            exit(1)

    # Operacje na klientach
    def pokaz_klientow(self):
        """Wyświetla listę wszystkich klientów."""
        try:
            self.kursor.execute("SELECT * FROM klienci")
            klienci = self.kursor.fetchall()
            if not klienci:
                print(Fore.YELLOW + "Brak klientów w bazie." + Style.RESET_ALL)
                return
            print(Fore.CYAN + "\nLista klientów:" + Style.RESET_ALL)
            for klient in klienci:
                print(f"{Fore.GREEN}ID: {klient[0]}, Imię: {klient[1]}, Nazwisko: {klient[2]}, Email: {klient[3]}, Telefon: {klient[4]}{Style.RESET_ALL}")
        except mysql.connector.Error as err:
            print(f"{Fore.RED}Błąd: {err}{Style.RESET_ALL}")

    def znajdz_klienta(self, nazwisko):
        """Wyszukuje klienta po nazwisku."""
        try:
            self.kursor.execute("SELECT * FROM klienci WHERE nazwisko = %s", (nazwisko,))
            klienci = self.kursor.fetchall()
            if not klienci:
                print(f"{Fore.YELLOW}Nie znaleziono klienta o nazwisku: {nazwisko}{Style.RESET_ALL}")
                return
            for klient in klienci:
                print(f"\n{Fore.CYAN}Znaleziono klienta:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}ID: {klient[0]}, Imię: {klient[1]}, Nazwisko: {klient[2]}, Email: {klient[3]}, Telefon: {klient[4]}{Style.RESET_ALL}")
        except mysql.connector.Error as err:
            print(f"{Fore.RED}Błąd: {err}{Style.RESET_ALL}")

    # Operacje na zamówieniach
    def pokaz_zamowienia_klienta(self, id_klienta):
        """Wyświetla wszystkie zamówienia danego klienta."""
        try:
            self.kursor.execute("""
                SELECT z.id, z.data_zamowienia, k.imie, k.nazwisko 
                FROM zamowienia z 
                JOIN klienci k ON z.klient_id = k.id 
                WHERE k.id = %s""", (id_klienta,))
            zamowienia = self.kursor.fetchall()
            if not zamowienia:
                print(f"Brak zamówień dla klienta o ID: {id_klienta}")
                return
            print("\nZnalezione zamówienia:")
            for zam in zamowienia:
                print(f"ID zamówienia: {zam[0]}, Data: {zam[1]}, Klient: {zam[2]} {zam[3]}")
        except mysql.connector.Error as err:
            print(f"Błąd: {err}")

    def oblicz_wartosc_zamowienia(self, id_zamowienia):
        """Oblicza łączną wartość zamówienia."""
        try:
            self.kursor.execute("""
                SELECT SUM(p.cena * pz.ilosc) as suma
                FROM pozycje_zamowienia pz
                JOIN produkty p ON pz.produkt_id = p.id
                WHERE pz.zamowienie_id = %s""", (id_zamowienia,))
            wynik = self.kursor.fetchone()
            if wynik[0] is None:
                print(f"Nie znaleziono zamówienia o ID: {id_zamowienia}")
                return
            print(f"\nŁączna wartość zamówienia {id_zamowienia}: {wynik[0]:.2f} zł")
        except mysql.connector.Error as err:
            print(f"Błąd: {err}")

    # Operacje eksportu danych
    def eksportuj_do_csv(self, nazwa_tabeli):
        """Eksportuje dane z wybranej tabeli do pliku CSV."""
        dozwolone_tabele = ['klienci', 'produkty', 'zamowienia', 'pozycje_zamowienia']
        if nazwa_tabeli not in dozwolone_tabele:
            print("Nieprawidłowa nazwa tabeli!")
            return
        
        try:
            self.kursor.execute(f"SELECT * FROM {nazwa_tabeli}")
            rekordy = self.kursor.fetchall()
            nazwy_kolumn = [i[0] for i in self.kursor.description]
            
            nazwa_pliku = f"{nazwa_tabeli}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as plik:
                writer = csv.writer(plik)
                writer.writerow(nazwy_kolumn)
                writer.writerows(rekordy)
            
            print(f"\nDane zostały wyeksportowane do pliku: {nazwa_pliku}")
        except mysql.connector.Error as err:
            print(f"Błąd: {err}")

# Program główny
def glowna():
    """Główna funkcja programu zawierająca menu użytkownika."""
    baza = BazaDanych()
    
    while True:
        print(f"\n{Fore.BLUE}=== MENU GŁÓWNE ==={Style.RESET_ALL}")
        print(Fore.CYAN + "1. Pokaż listę klientów")
        print("2. Znajdź klienta po nazwisku")
        print("3. Pokaż zamówienia klienta")
        print("4. Oblicz wartość zamówienia")
        print("5. Eksportuj dane do CSV")
        print(f"0. Zakończ{Style.RESET_ALL}")

        wybor = input(f"\n{Fore.YELLOW}Wybierz opcję: {Style.RESET_ALL}")

        if wybor == "1":
            baza.pokaz_klientow()
        
        elif wybor == "2":
            nazwisko = input("Podaj nazwisko klienta: ")
            baza.znajdz_klienta(nazwisko)
        
        elif wybor == "3":
            try:
                klient_id = int(input("Podaj ID klienta: "))
                baza.pokaz_zamowienia_klienta(klient_id)
            except ValueError:
                print("Błąd: ID klienta musi być liczbą!")
        
        elif wybor == "4":
            try:
                zamowienie_id = int(input("Podaj ID zamówienia: "))
                baza.oblicz_wartosc_zamowienia(zamowienie_id)
            except ValueError:
                print("Błąd: ID zamówienia musi być liczbą!")
        
        elif wybor == "5":
            print("\nDostępne tabele: klienci, produkty, zamowienia, pozycje_zamowienia")
            nazwa_tabeli = input("Podaj nazwę tabeli do eksportu: ")
            baza.eksportuj_do_csv(nazwa_tabeli)
        
        elif wybor == "0":
            print(f"{Fore.GREEN}Do widzenia!{Style.RESET_ALL}")
            break
        
        else:
            print(f"{Fore.RED}Nieprawidłowy wybór!{Style.RESET_ALL}")

if __name__ == "__main__":
    glowna()
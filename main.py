import requests
from utilities import save_invoice_to_file

def welcome_message():
    """Funkcja wyświetlająca powitalne wiadomości."""
    print("\n" * 50)  # Drukuje 50 pustych linii, "przewijając" ekran w górę
    print("Witaj w programie CalcEx!")
    print("Jestem tutaj, aby pomóc Ci w zarządzaniu fakturami.")

def get_invoice_data():
    """Funkcja pobierająca dane dotyczące faktur od użytkownika."""
    while True:
        try:
            invoice_amount = float(input("Podaj kwotę faktury: "))
            break  # Wyjście z pętli jeśli wprowadzono poprawną kwotę
        except ValueError:
            print("Podana kwota jest nieprawidłowa. Spróbuj ponownie.")
    
    invoice_currency = input("Podaj walutę faktury (USD, EUR, GBP, PLN): ").upper()
    invoice_date = input("Podaj datę wystawienia faktury (RRRR-MM-DD): ")
    
    return invoice_amount, invoice_currency, invoice_date

def get_payment_data():
    """Funkcja pobierająca informacje o płatnościach od użytkownika."""
    while True:
        try:
            payment_amount = float(input("Podaj kwotę płatności: "))
            break  # Wyjście z pętli jeśli wprowadzono poprawną kwotę
        except ValueError:
            print("Podana kwota jest nieprawidłowa. Spróbuj ponownie.")
    
    payment_currency = input("Podaj walutę płatności (USD, EUR, GBP, PLN): ").upper()
    payment_date = input("Podaj datę płatności (RRRR-MM-DD): ")
    
    return payment_amount, payment_currency, payment_date

def get_exchange_rate(currency_code, date):
    if currency_code == 'PLN':
        # W przypadku PLN zwracamy kurs 1, bo nie musimy go pobierać z API
        return 1.0
    try:
        response = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{date}/?format=json")
        data = response.json()
        rate = data['rates'][0]['mid']
        print(f"Kurs waluty {currency_code} dla daty {date}: {rate}")
        return rate
    except Exception as e:
        print(f"Błąd podczas pobierania kursu waluty: {e}")
        return None

def calculate_exchange_difference(invoice_amount, invoice_currency, invoice_date, payment_amount, payment_currency, payment_date):
    invoice_rate = get_exchange_rate(invoice_currency, invoice_date)
    payment_rate = get_exchange_rate(payment_currency, payment_date)
    
    if invoice_rate is not None and payment_rate is not None:
        invoice_amount_pln = invoice_amount if invoice_currency == 'PLN' else invoice_amount * invoice_rate
        payment_amount_pln = payment_amount if payment_currency == 'PLN' else payment_amount * payment_rate
        exchange_difference = payment_amount_pln - invoice_amount_pln
        return exchange_difference
    else:
        return None

def enter_invoice():
    """Funkcja do wprowadzania faktury."""
    invoice_data = get_invoice_data()
    payment_data = get_payment_data()
    
    exchange_difference = calculate_exchange_difference(*invoice_data, *payment_data)
    if exchange_difference is not None:
        if exchange_difference < 0:
            print(f"Niedopłata {abs(exchange_difference):.2f} PLN.")
            discrepancy = f"Niedopłata {abs(exchange_difference):.2f} PLN."
        elif exchange_difference > 0:
            print(f"Nadpłata {exchange_difference:.2f} PLN.")
            discrepancy = f"Nadpłata {exchange_difference:.2f} PLN."
        else:
            print("Faktura opłacona w całości.")
            discrepancy = "Brak rozbieżności"
        
        # Zapisujemy fakturę do pliku wraz z informacją o rozbieżności
        save_invoice_to_file(invoice_data, payment_data, is_paid=True, discrepancy=discrepancy)
        
    else:
        print("Nie udało się obliczyć różnicy kursowej.")

def show_invoice_history():
    """Funkcja do wyświetlania historii wprowadzonych faktur."""
    try:
        with open("spis-faktur.txt", "r") as file:
            print("Historia wprowadzonych faktur:")
            print(file.read())
    except FileNotFoundError:
        print("Nie znaleziono pliku spis-faktur.txt.")
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku: {e}")

def help_menu():
    """Funkcja wyświetlająca informacje o funkcjach programu."""
    print("\nDostępne funkcje programu:")
    print("1. Wprowadzić fakturę - pozwala użytkownikowi wprowadzić nową fakturę do systemu.")
    print("2. Sprawdzić historię wprowadzonych faktur - wyświetla listę faktur zapisanych w pliku spis-faktur.txt.")
    print("3. Pomoc - wyświetla informacje o dostępnych funkcjach programu.")
    print("4. Wyjść z programu - zamyka program.")

def main():
    welcome_message()
    while True:
        print("\nCo dzisiaj chcesz zrobić?")
        print("1. Wprowadzić fakturę")
        print("2. Sprawdzić historię wprowadzonych faktur")
        print("3. Pomoc")
        print("4. Wyjść z programu")
        
        choice = input("Wybierz opcję (1/2/3/4): ")
        
        if choice == '1':
            print("\n" * 50)  # Czyszczenie ekranu przed wywołaniem funkcji wprowadzania faktury
            enter_invoice()
        elif choice == '2':
            print("\n" * 50)  # Czyszczenie ekranu przed wywołaniem funkcji sprawdzania historii faktur
            show_invoice_history()
        elif choice == '3':
            print("\n" * 50)  # Czyszczenie ekranu przed wyświetleniem pomocy
            help_menu()
        elif choice == '4':
            print("\n" * 50)  # Czyszczenie ekranu przed wyjściem z programu
            print("Dziękujemy za skorzystanie z programu CalcEx. Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()

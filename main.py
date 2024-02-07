import requests
from utilities import save_invoice_to_file
from datetime import datetime

def get_invoice_data():
    """Funkcja pobierająca dane dotyczące faktur od użytkownika."""
    while True:
        try:
            invoice_amount = float(input("Podaj kwotę faktury: "))
            break  # Wyjście z pętli jeśli wprowadzono poprawną kwotę
        except ValueError:
            print("Podana kwota jest nieprawidłowa. Spróbuj ponownie.")
    
    invoice_currency = input("Podaj walutę faktury (USD, EUR, GBP, PLN): ").upper()
    
    while True:
        invoice_date = input("Podaj datę wystawienia faktury (RRRR-MM-DD): ")
        try:
            # Sprawdzamy czy data ma właściwy format
            datetime.strptime(invoice_date, "%Y-%m-%d")
            # Sprawdzamy czy data jest wcześniejsza niż dzisiejsza data
            if datetime.strptime(invoice_date, "%Y-%m-%d") > datetime.now():
                print("Data faktury nie może być z przyszłości. Spróbuj ponownie.")
                continue
            break  # Wyjście z pętli jeśli wprowadzono poprawną datę
        except ValueError:
            print("Nieprawidłowy format daty. Wprowadź datę w formacie RRRR-MM-DD.")
    
    return invoice_amount, invoice_currency, invoice_date

from datetime import datetime

def get_payment_data():
    """Funkcja pobierająca informacje o płatnościach od użytkownika."""
    while True:
        try:
            payment_amount = float(input("Podaj kwotę płatności: "))
            break  # Wyjście z pętli jeśli wprowadzono poprawną kwotę
        except ValueError:
            print("Podana kwota jest nieprawidłowa. Spróbuj ponownie.")
    
    payment_currency = input("Podaj walutę płatności (USD, EUR, GBP, PLN): ").upper()
    
    while True:
        payment_date = input("Podaj datę płatności (RRRR-MM-DD): ")
        try:
            # Sprawdzamy czy data ma właściwy format
            datetime.strptime(payment_date, "%Y-%m-%d")
            # Sprawdzamy czy data jest wcześniejsza niż dzisiejsza data
            if datetime.strptime(payment_date, "%Y-%m-%d") > datetime.now():
                print("Data płatności nie może być z przyszłości. Spróbuj ponownie.")
                continue
            break  # Wyjście z pętli jeśli wprowadzono poprawną datę
        except ValueError:
            print("Nieprawidłowy format daty. Wprowadź datę w formacie RRRR-MM-DD.")
    
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

def main():
    while True:
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
        
        next_invoice = input("Czy chcesz przeliczyć kolejną fakturę? (Tak/Nie): ").lower()
        if next_invoice != 'tak':
            break


if __name__ == "__main__":
    main()

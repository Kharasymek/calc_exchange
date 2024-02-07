import requests
from utilities import save_invoice_to_file

def get_invoice_data():
    """Funkcja pobierająca dane dotyczące faktur od użytkownika."""
    invoice_amount = float(input("Podaj kwotę faktury: "))
    invoice_currency = input("Podaj walutę faktury (USD, EUR, GBP, PLN): ").upper()
    invoice_date = input("Podaj datę wystawienia faktury (RRRR-MM-DD): ")
    
    return invoice_amount, invoice_currency, invoice_date

def get_payment_data():
    """Funkcja pobierająca informacje o płatnościach od użytkownika."""
    payment_amount = float(input("Podaj kwotę płatności: "))
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

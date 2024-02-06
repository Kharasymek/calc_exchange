# Main.py
import requests

def get_invoice_data():
    """Funkcja pobierająca dane dotyczące faktur od użytkownika."""
    invoice_amount = float(input("Podaj kwotę faktury: "))
    while True:
        invoice_currency = input("Podaj walutę faktury (USD, EUR, GBP): ")
        if invoice_currency.upper() in ["USD", "EUR", "GBP"]:
            break
        else:
            print("Nieprawidłowa waluta. Wybierz spośród opcji: USD, EUR, GBP")
    invoice_date = input("Podaj datę wystawienia faktury (RRRR-MM-DD): ")
    
    return invoice_amount, invoice_currency, invoice_date

def get_payment_data():
    """Funkcja pobierająca informacje o płatnościach od użytkownika."""
    payment_amount = float(input("Podaj kwotę płatności: "))
    while True:
        payment_currency = input("Podaj walutę płatności (USD, EUR, GBP): ")
        if payment_currency.upper() in ["USD", "EUR", "GBP"]:
            break
        else:
            print("Nieprawidłowa waluta. Wybierz spośród opcji: USD, EUR, GBP")
    payment_date = input("Podaj datę płatności (RRRR-MM-DD): ")
    
    return payment_amount, payment_currency, payment_date

def get_exchange_rate(currency_code):
    try:
        response = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/?format=json")
        data = response.json()
        return data['rates'][0]['mid']
    except Exception as e:
        print(f"Błąd podczas pobierania kursu waluty: {e}")
        return None

def calculate_exchange_difference(invoice_data, payment_data):
    invoice_amount, invoice_currency, invoice_date = invoice_data
    payment_amount, payment_currency, payment_date = payment_data
    
    payment_rate = get_exchange_rate(payment_currency)
    invoice_rate = get_exchange_rate(invoice_currency)
    
    if payment_rate and invoice_rate:
        print(f"Kurs waluty {invoice_currency} dla daty faktury: {invoice_rate}")
        print(f"Kurs waluty {payment_currency} dla daty płatności: {payment_rate}")
        
        invoice_amount_pln = invoice_amount * invoice_rate
        payment_amount_pln = payment_amount * payment_rate
        print(f"Kwota faktury w złotówkach: {invoice_amount_pln:.2f} PLN")
        print(f"Kwota płatności w złotówkach: {payment_amount_pln:.2f} PLN")
        
        exchange_difference = (invoice_amount_pln / invoice_rate) - (payment_amount_pln / payment_rate)
        return exchange_difference
    else:
        return None

def main():
    invoice_data = get_invoice_data()
    payment_data = get_payment_data()
    exchange_difference = calculate_exchange_difference(invoice_data, payment_data)
    
    if exchange_difference is not None:
        print(f"Różnica kursowa: {exchange_difference:.2f} PLN")
    else:
        print("Nie udało się obliczyć różnicy kursowej.")

if __name__ == "__main__":
    main()

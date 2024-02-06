# Main.py
import requests

def get_invoice_data():
    """Funkcja pobierająca dane dotyczące faktur od użytkownika."""
    invoice_amount = float(input("Podaj kwotę faktury: "))
    
    # Pytanie użytkownika o wybór waluty z podanych opcji
    while True:
        invoice_currency = input("Podaj walutę faktury (USD, EUR, GBP): ").upper()
        if invoice_currency in ['USD', 'EUR', 'GBP']:
            break
        else:
            print("Nieprawidłowa waluta. Wybierz spośród opcji: USD, EUR, GBP")
    
    invoice_date = input("Podaj datę wystawienia faktury (RRRR-MM-DD): ")
    
    return invoice_amount, invoice_currency, invoice_date

def get_payment_data():
    """Funkcja pobierająca informacje o płatnościach od użytkownika."""
    payment_amount = float(input("Podaj kwotę płatności: "))
    
    # Pytanie użytkownika o wybór waluty z podanych opcji
    while True:
        payment_currency = input("Podaj walutę płatności (USD, EUR, GBP): ").upper()
        if payment_currency in ['USD', 'EUR', 'GBP']:
            break
        else:
            print("Nieprawidłowa waluta. Wybierz spośród opcji: USD, EUR, GBP")
    
    payment_date = input("Podaj datę płatności (RRRR-MM-DD): ")
    
    return payment_amount, payment_currency, payment_date

def get_exchange_rate(currency_code):
    """Funkcja pobierająca kurs waluty z API NBP."""
    try:
        response = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/?format=json")
        data = response.json()
        return data['rates'][0]['mid']
    except Exception as e:
        print(f"Błąd pobierania kursu waluty: {e}")
        return None

def calculate_exchange_difference(amount, currency, payment_date, invoice_date):
    """Funkcja obliczająca różnicę kursową."""
    payment_rate = get_exchange_rate(currency)
    invoice_rate = get_exchange_rate(currency)
    
    if payment_rate and invoice_rate:
        exchange_difference = (amount / invoice_rate) - (amount / payment_rate)
        return exchange_difference
    else:
        return None

def main():
    invoice_data = get_invoice_data()
    payment_data = get_payment_data()
    
    # Dalsza logika programu, np. obliczenia różnic kursowych i wyświetlanie wyników.

if __name__ == "__main__":
    main()

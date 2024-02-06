# Main.py

def get_invoice_data():
    """Funkcja pobierająca dane dotyczące faktur od użytkownika."""
    invoice_amount = float(input("Podaj kwotę faktury: "))
    invoice_currency = input("Podaj walutę faktury: ")
    invoice_date = input("Podaj datę wystawienia faktury (RRRR-MM-DD): ")
    
    return invoice_amount, invoice_currency, invoice_date

def get_payment_data():
    """Funkcja pobierająca informacje o płatnościach od użytkownika."""
    payment_amount = float(input("Podaj kwotę płatności: "))
    payment_currency = input("Podaj walutę płatności: ")
    payment_date = input("Podaj datę płatności (RRRR-MM-DD): ")
    
    return payment_amount, payment_currency, payment_date

def main():
    invoice_data = get_invoice_data()
    payment_data = get_payment_data()
    
    # Dalsza logika

if __name__ == "__main__":
    main()

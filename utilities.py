def save_invoice_to_file(invoice_data, payment_data, is_paid, discrepancy):
    try:
        filename = "spis-faktur.txt"
        with open(filename, "a") as file:
            with open(filename, "r") as f:
                num_invoices = sum(1 for line in f if line.startswith("Faktura"))
            file.write(f"Faktura {num_invoices + 1}:\n")
            file.write(f"Kwota faktury: {invoice_data[0]} {invoice_data[1]}\n")
            file.write(f"Data wystawienia: {invoice_data[2]}\n")
            file.write(f"Kwota płatności: {payment_data[0]} {payment_data[1]}\n")
            file.write(f"Data płatności: {payment_data[2]}\n")
            file.write(f"Opłacona: {'Tak' if is_paid else 'Nie'}\n")
            file.write(f"Rozbieżność: {discrepancy}\n")
            file.write("\n")
        print("Dane rozliczenia zostały zapisane.")
    except Exception as e:
        print(f"Błąd podczas zapisywania danych rozliczenia do pliku: {e}")

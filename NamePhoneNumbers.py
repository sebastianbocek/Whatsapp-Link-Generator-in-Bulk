import csv

def extract_name_and_phone(csv_file, txt_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as infile, \
         open(txt_file, 'w', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        
        for row in reader:
            if len(row) > 8:  # Verificamos que exista la columna H
                name = row[1].strip() if len(row) > 0 else "SinNombre"
                phone = row[8].strip()

                if phone:
                    # Normalizamos el número para Argentina
                    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                    
                    # Si empieza con +549 o +54 9 lo dejamos en +54
                    if phone.startswith("+549"):
                        phone = "+54" + phone[4:]
                    elif phone.startswith("+54 9"):
                        phone = "+54" + phone[5:]
                    
                    # Si empieza con 9 y tiene 11 dígitos, lo dejamos igual (ya es cel)
                    # Si empieza con 0 lo quitamos (prefijo nacional innecesario)
                    if phone.startswith("0"):
                        phone = phone[1:]

                    outfile.write(f"{name} - {phone}\n")

    print(f"✅ Nombres y teléfonos exportados a {txt_file}")

# Ejemplo de uso
extract_name_and_phone('input.csv', 'NamePhoneNumbers.txt')

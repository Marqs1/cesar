from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Zmodyfikowana funkcja szyfrująca za pomocą szyfru Cezara
def szyfr_cezara(text, przesuniecie):
    zaszyfrowany_tekst = ""
    for znak in text:
        if znak.isalpha():
            przesuniecie_znaku = 65 if znak.isupper() else 97
            zaszyfrowany_tekst += chr((ord(znak) + przesuniecie - przesuniecie_znaku) % 26 + przesuniecie_znaku)
        elif znak.isdigit():
            zaszyfrowany_tekst += str((int(znak) + przesuniecie) % 10)
        else:
            zaszyfrowany_tekst += znak
    return zaszyfrowany_tekst

# Funkcja generująca hasło
def passwordGenerator(dlugosc, ilosc_wielkich, ilosc_malych, ilosc_cyfr, ilosc_znakow_specjalnych):
    haslo = []

    haslo.extend(random.choices(string.ascii_uppercase, k=ilosc_wielkich))
    haslo.extend(random.choices(string.ascii_lowercase, k=ilosc_malych))
    haslo.extend(random.choices(string.digits, k=ilosc_cyfr))
    haslo.extend(random.choices(string.punctuation, k=ilosc_znakow_specjalnych))

    random.shuffle(haslo)
    haslo = ''.join(haslo) + ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=dlugosc - len(haslo)))

    return haslo

# Endpoint do generowania hasła
@app.route('/generate-password', methods=['POST'])
def generate_password():
    data = request.json
    dlugosc_hasla = data.get('dlugosc')
    ilosc_wielkich = data.get('ilosc_wielkich')
    ilosc_malych = data.get('ilosc_malych')
    ilosc_cyfr = data.get('ilosc_cyfr')
    ilosc_znakow_specjalnych = data.get('ilosc_znakow_specjalnych')

    if dlugosc_hasla < ilosc_wielkich + ilosc_malych + ilosc_cyfr + ilosc_znakow_specjalnych:
        return jsonify({"error": "Suma określonych typów znaków jest większa niż żądana długość hasła."}), 400

    wygenerowane_haslo = passwordGenerator(dlugosc_hasla, ilosc_wielkich, ilosc_malych, ilosc_cyfr, ilosc_znakow_specjalnych)
    zaszyfrowane_haslo = szyfr_cezara(wygenerowane_haslo, 3)

    # Zapis zaszyfrowanego hasła do pliku
    with open('zaszyfrowane_haslo.txt', 'w') as plik:
        plik.write(zaszyfrowane_haslo)

    return jsonify({"wygenerowane_haslo": wygenerowane_haslo, "zaszyfrowane_haslo": zaszyfrowane_haslo})

if __name__ == '__main__':
    app.run(debug=True)

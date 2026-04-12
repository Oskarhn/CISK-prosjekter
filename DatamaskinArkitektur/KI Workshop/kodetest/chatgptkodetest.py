import secrets

# Generer et "ekte" tilfeldig tall (0–100)
random_number = secrets.randbelow(101)

# Be brukeren gjette to tall
a = int(input("Skriv inn første tall: "))
b = int(input("Skriv inn andre tall: "))

# Sjekk om summen matcher det tilfeldige tallet
if a + b == random_number:
    print(f"Riktig! {a} + {b} = {random_number}")
else:
    print(f"Feil. {a} + {b} = {a + b}, men tallet var {random_number}")
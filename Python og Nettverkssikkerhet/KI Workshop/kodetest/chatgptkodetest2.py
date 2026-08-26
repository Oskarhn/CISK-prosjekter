import secrets

r = secrets.randbelow(101)
a = int(input("Første tall: "))
b = int(input("Andre tall: "))

print("Riktig!" if a + b == r else f"Feil. Summen er {a + b}, tallet var {r}")
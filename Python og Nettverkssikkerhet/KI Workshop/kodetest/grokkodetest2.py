import secrets
r = secrets.randbelow(101)
print("I've picked a random number (0-100). Guess two numbers that sum to it.")
n1 = int(input("First number: "))
n2 = int(input("Second number: "))
s = n1 + n2
print("Correct!" if s == r else f"Wrong. The number was {r}. Your sum: {s}")
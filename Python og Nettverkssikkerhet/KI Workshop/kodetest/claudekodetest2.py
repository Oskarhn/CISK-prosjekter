import secrets

target = secrets.randbelow(100) + 1
print(f"Guess two numbers that sum to the secret number (1-100).")
a = int(input("First number: "))
b = int(input("Second number: "))
print(f"{a} + {b} = {a+b} | Secret: {target}")
print("✅ Correct!" if a + b == target else f"❌ Wrong — off by {target - (a+b)}.")
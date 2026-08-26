import secrets
target = secrets.randbelow(100) + 1
print("Target set (1-100). Can you pick two numbers that sum to it?")
try:
    n1, n2 = int(input("No. 1: ")), int(input("No. 2: "))
    total = n1 + n2
    win = (total == target)
    print(f"Your Sum: {total} | Target: {target}")
    print("🎯 Nailed it!" if win else f"❌ No luck. Off by {abs(target - total)}.")
except ValueError:
    print("Invalid input. Please use whole numbers.")
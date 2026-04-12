import secrets

def generate_random_number(lower: int = 1, upper: int = 100) -> int:
    """Generate a cryptographically secure random integer in [lower, upper]."""
    return secrets.randbelow(upper - lower + 1) + lower

def get_user_guess(prompt: str, lower: int, upper: int) -> int:
    """Prompt user for a number within range, retry on invalid input."""
    while True:
        try:
            value = int(input(prompt))
            if lower <= value <= upper:
                return value
            print(f"  Please enter a number between {lower} and {upper}.")
        except ValueError:
            print("  Invalid input — enter a whole number.")

def main():
    LOWER, UPPER = 1, 100

    target = generate_random_number(LOWER, UPPER)
    print(f"\n🎲 A secret number has been generated in the range [{LOWER}, {UPPER}].")
    print("Your goal: guess two numbers whose SUM equals it.\n")

    a = get_user_guess(f"Enter your first number  ({LOWER}–{UPPER}): ", LOWER, UPPER)
    b = get_user_guess(f"Enter your second number ({LOWER}–{UPPER}): ", LOWER, UPPER)

    total = a + b
    print(f"\nYour numbers : {a} + {b} = {total}")
    print(f"Secret number: {target}")

    if total == target:
        print("✅ Correct! Your numbers sum to the secret number.")
    else:
        diff = target - total
        hint = "higher" if diff > 0 else "lower"
        print(f"❌ Not quite — your sum is {abs(diff)} {hint} than the secret number.")

if __name__ == "__main__":
    main()
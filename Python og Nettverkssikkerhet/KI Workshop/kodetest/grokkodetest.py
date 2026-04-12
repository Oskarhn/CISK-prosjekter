import secrets

def main():
    # Generate a special and truly random number using the secrets module
    # (cryptographically secure randomness sourced from the OS)
    # Range: 0 to 100 (inclusive) – chosen to keep the guessing game fun and manageable
    random_number = secrets.randbelow(101)
    
    print("🎲 I've generated a special and truly random number (between 0 and 100)!")
    print("Your mission: guess TWO numbers whose sum exactly equals it.\n")
    
    try:
        num1 = int(input("Enter your first guessed number: "))
        num2 = int(input("Enter your second guessed number: "))
        
        user_sum = num1 + num2
        
        if user_sum == random_number:
            print(f"\n🎉 Perfect match! {num1} + {num2} = {user_sum}")
            print(f"The special random number was indeed {random_number}!")
        else:
            print(f"\n😔 Not quite... Your sum ({num1} + {num2} = {user_sum})")
            print(f"The special random number was {random_number}.")
    
    except ValueError:
        print("\n⚠️ Oops! Please enter valid whole numbers only.")

if __name__ == "__main__":
    main()
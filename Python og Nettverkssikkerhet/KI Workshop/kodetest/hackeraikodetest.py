import secrets
import random

def generate_special_random_number():
    """
    Generates a 'special and truly random' number using secrets module for cryptographically secure randomness.
    Range: 1 to 1000 for a practical guessing game.
    """
    return secrets.randbelow(1000) + 1

def main():
    # Generate the special random number
    target = generate_special_random_number()
    print("I've generated a special truly random number between 1 and 1000.")
    print("Guess two numbers that sum to it!")
    
    while True:
        try:
            # Get user guesses
            guess1 = int(input("Enter your first number: "))
            guess2 = int(input("Enter your second number: "))
            
            total = guess1 + guess2
            
            if total == target:
                print(f"🎉 Correct! {guess1} + {guess2} = {target}")
                break
            elif total < target:
                print("Too low! Try a larger sum.")
            else:
                print("Too high! Try a smaller sum.")
                
        except ValueError:
            print("Please enter valid integers.")
    
    print(f"The special random number was: {target}")

if __name__ == "__main__":
    main()
import secrets

def play_sum_game():
    # 1. Generating a cryptographically strong random number between 1 and 100
    # Unlike 'random.randint', 'secrets' is designed for security and higher entropy.
    target_number = secrets.randbelow(100) + 1
    
    print("--- The Secret Number Game ---")
    print("I have generated a truly random number between 1 and 100.")
    
    try:
        # 2. Getting user guesses
        guess_1 = int(input("Enter your first number: "))
        guess_2 = int(input("Enter your second number: "))
        
        user_sum = guess_1 + guess_2
        
        # 3. Evaluating the result
        print(f"\nYour total: {user_sum}")
        print(f"The secret number was: {target_number}")
        
        if user_sum == target_number:
            print("✨ Incredible! Your sum matches the random number perfectly.")
        else:
            diff = abs(target_number - user_sum)
            print(f"Close, but no cigar. You were off by {diff}.")
            
    except ValueError:
        print("Invalid input! Please enter whole numbers only.")

if __name__ == "__main__":
    play_sum_game()
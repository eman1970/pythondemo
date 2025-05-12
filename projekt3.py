import random

def generate_question(operation, value, used_questions, question_limits):
    """Generates a unique mathematical question based on the selected operation."""
    attempts = 0
    while True:
        # Generera en ny fråga
        if operation == "multiplication":
            factor = random.randint(0, 12)
            question = (factor, value)
            answer = factor * value
        elif operation == "division":
            dividend = random.randint(0, 12)
            question = (dividend, value)
            answer = dividend // value
        elif operation == "modulo":
            dividend = random.randint(0, 12)
            question = (dividend, value)
            answer = dividend % value
        else:
            raise ValueError("Invalid operation!")

        max_occurrences = question_limits[0] if len(used_questions) < 14 else \
                          question_limits[1] if len(used_questions) < 27 else \
                          question_limits[2]

        if used_questions.get(question, 0) < max_occurrences:
            used_questions[question] = used_questions.get(question, 0) + 1
            return question[0], answer

        attempts += 1
        if attempts > 100:
            raise ValueError("Failed to generate a unique question.")

def input_valid_int(prompt_text, min_value, max_value=None):
    """Validates integer input and ensures it is within the allowed range."""
    while True:
        try:
            user_answer = int(input(prompt_text).strip())
            if max_value is None or min_value <= user_answer <= max_value:
                return user_answer
            print(f"Invalid number! Enter an integer between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input! Enter a valid integer.")

def input_valid_str(prompt_text, valid_answers):
    """Validates string input and ensures the user selects a valid option."""
    while True:
        user_answer = input(prompt_text).strip().lower()
        if user_answer in valid_answers:
            return user_answer
        print(f"Invalid choice! Enter one of the following: {', '.join(valid_answers)}.")

def main():
    """Main function that handles the entire game."""
    print("Welcome to Zombie House! 🧟‍♂️")
    print("You must answer math questions correctly and avoid zombie doors to escape.")

    # Initial input for game settings
    num_questions = input_valid_int("Select the number of questions (12-39): ", 12, 39)
    operation = input_valid_str("Select an operation (multiplication, division, modulo): ", 
                                ["multiplication", "division", "modulo"])
    
    if operation == "multiplication":
        value = input_valid_int("Choose a multiplication table (2-12): ", 2, 12)
    else:
        value = input_valid_int("Choose a divisor (2-5): ", 2, 5)

    while True:
        used_questions = {}
        question_limits = (1, 2, 3)
        doors = num_questions
        won_game = False

        for question_num in range(1, num_questions + 1):
            factor_or_dividend, correct_answer = generate_question(operation, value, used_questions, question_limits)
            print(f"\nQuestion {question_num}: What is {factor_or_dividend} {operation} {value}?")
            
            user_answer = input_valid_int("Your answer: ", 0)

            if user_answer != correct_answer:
                print("Wrong answer! The zombies got you! Game over! 😱")
                break

            print(f"Correct answer! You have completed {question_num} of {num_questions} questions.")

            if doors > 1:
                print(f"Choose a door between 1 and {doors}. The zombies are hiding behind one of them!")
                zombie_door = random.randint(1, doors)
                print(f"DEBUG: The zombies are hiding behind door {zombie_door}")

                chosen_door = input_valid_int(f"Which door do you choose (1-{doors})? ", 1, doors)

                if chosen_door == zombie_door:
                    print(f"Oh no! The zombies got you! They were hiding behind door {zombie_door}. Game over! 😱")
                    break

                doors -= 1
            else:
                print("Congratulations! You completed all questions and survived Zombie House! 🎉")
                won_game = True
                break

        play_again = input_valid_str("Do you want to play again? (yes/no): ", ["yes", "no"])
        
        if play_again != "yes":
            print("Thanks for playing Zombie House! Goodbye!")
            break

        if won_game:
            # If the player won, let them choose new settings
            num_questions = input_valid_int("Select the number of questions (12-39): ", 12, 39)
            operation = input_valid_str("Select an operation (multiplication, division, modulo): ", 
                                        ["multiplication", "division", "modulo"])
            if operation == "multiplication":
                value = input_valid_int("Choose a multiplication table (2-12): ", 2, 12)
            else:
                value = input_valid_int("Choose a divisor (2-5): ", 2, 5)

if __name__ == "__main__":
    main()

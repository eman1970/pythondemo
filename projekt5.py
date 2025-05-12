import random

def generate_question(operation, value, used_questions, question_limits):
    """Genererar en unik matematisk fråga från en fördefinierad lista."""
    possible_questions = [(operand, value) for operand in range(0, 13)]  # Fast lista över möjliga frågor
    attempts = 0

    while attempts < 1000:
        if not possible_questions:  # If list is empty, reset it
            possible_questions = [(operand, value) for operand in range(0, 13)]

        question = random.choice(possible_questions)  # Pick a question from the list
        operand = question[0]

        operations = {
            "*": operand * value,
            "//": operand // value if value != 0 else None,  # Prevent division by zero
            "%": operand % value if value != 0 else None
        }
        answer = operations.get(operation)

        if answer is None:
            raise ValueError("Invalid operation!")

        max_occurrences = question_limits[0] if len(used_questions) < 14 else \
                          question_limits[1] if len(used_questions) < 27 else \
                          question_limits[2]

        if used_questions.get(question, 0) < max_occurrences:
            used_questions[question] = used_questions.get(question, 0) + 1
            return question[0], answer

        possible_questions.remove(question)
        attempts += 1

    raise ValueError("Failed to generate a unique question.")  # If all questions are exhausted

def main():
    """Huvudfunktionen som hanterar användarinmatning och spelets gång."""
    while True:
        used_questions = {}
        question_limits = (1, 2, 3)
        doors = num_questions

        for question_num in range(1, num_questions + 1):
            factor_or_dividend, correct_answer = generate_question(operation, value, used_questions, question_limits)
            print(f"\nFråga {question_num}: Vad är {factor_or_dividend} {operation} {value}?")
            
            user_answer = input_valid_int("Ditt svar: ", 0)

            if user_answer != correct_answer:
                print("Fel svar! Zombierna tog dig! Spelet är över! 😱")
                break

            print(f"Korrekt svar! Du har klarat {question_num} av {num_questions} frågor.")

            if question_num == num_questions:  # If last question, win instantly
                print("Grattis! Du klarade alla frågor och överlevde Zombie House! 🎉")
                break  # Exit loop immediately

            # Door selection for earlier rounds
            if doors > 1:
                zombie_door = random.randint(1, doors)
                chosen_door = input_valid_int(f"Vilken dörr väljer du (1-{doors})? ", 1, doors)

                if chosen_door == zombie_door:
                    print(f"Åh nej! Zombierna tog dig! Spelet är över! 😱")
                    break

                doors -= 1

        play_again = input_valid_str("Vill du spela igen? (yes/no): ", ["yes", "no"])
        if play_again != "yes":
            print("Tack för att du spelade Zombie House! Hejdå!")
            break

import random

def generate_question(operation, value, used_questions, question_limits):
    """Genererar en unik matematisk fråga från en fördefinierad lista."""
    possible_questions = [(operand, value) for operand in range(0, 13)]  # Fast lista över möjliga frågor
    attempts = 0

    while attempts < 1000:
        if not possible_questions:  # Om listan är tom, återställ den
            possible_questions = [(operand, value) for operand in range(0, 13)]

        question = random.choice(possible_questions)  # Välj en fråga från listan
        operand = question[0]

        operations = {
            "*": operand * value,
            "//": operand // value if value != 0 else None,  # Förhindra division med noll
            "%": operand % value if value != 0 else None
        }
        answer = operations.get(operation)

        if answer is None:
            raise ValueError("Ogiltig operation!")

        max_occurrences = question_limits[0] if len(used_questions) < 14 else \
                          question_limits[1] if len(used_questions) < 27 else \
                          question_limits[2]

        if used_questions.get(question, 0) < max_occurrences:
            used_questions[question] = used_questions.get(question, 0) + 1
            return question[0], answer

        possible_questions.remove(question)
        attempts += 1

    raise ValueError("Misslyckades med att generera en unik fråga.")  # Om alla frågor är förbrukade

def input_valid_int(prompt_text, min_value, max_value=None):
    """Validerar heltalsinmatning och ser till att den ligger inom tillåtet intervall."""
    while True:
        try:
            user_answer = int(input(prompt_text).strip())
            if max_value is None or min_value <= user_answer <= max_value:
                return user_answer
            print(f"Ogiltigt nummer! Ange ett heltal mellan {min_value} och {max_value}.")
        except ValueError:
            print("Ogiltig inmatning! Ange ett giltigt heltal.")

def input_valid_str(prompt_text, valid_answers):
    """Validerar stränginmatning och ser till att användaren väljer ett giltigt alternativ."""
    while True:
        user_answer = input(prompt_text).strip()
        if user_answer in valid_answers:
            return user_answer
        print(f"Ogiltigt val! Ange något av följande: {', '.join(valid_answers)}.")

def main():
    """Huvudfunktionen som hanterar användarinmatning och spelets gång."""
    print("Välkommen till Zombie House! 🧟‍♂️")
    print("Du måste svara rätt på matematikfrågor och undvika zombiedörrar för att fly.")

    # Initial inmatning för spelinställningar
    num_questions = input_valid_int("Välj antal frågor (12-39): ", 12, 39)
    operation = input_valid_str("Välj ett räknesätt (*, //, %): ", ["*", "//", "%"])
    
    if operation == "*":
        value = input_valid_int("Välj en multiplikationstabell (2-12): ", 2, 12)
    else:
        value = input_valid_int("Välj en divisor (2-5): ", 2, 5)

    while True:
        used_questions = {}
        question_limits = (1, 2, 3)
        doors = num_questions
        won_game = False  # Standardvärde

        for question_num in range(1, num_questions + 1):
            factor_or_dividend, correct_answer = generate_question(operation, value, used_questions, question_limits)
            print(f"\nFråga {question_num}: Vad är {factor_or_dividend} {operation} {value}?")
            
            user_answer = input_valid_int("Ditt svar: ", 0)

            if user_answer != correct_answer:
                print("Fel svar! Zombierna tog dig! Spelet är över! 😱")
                won_game = False
                break

            print(f"Korrekt svar! Du har klarat {question_num} av {num_questions} frågor.")

            if doors == 2:  # Om bara två dörrar återstår, välj en dörr först
                zombie_door = random.randint(1, doors)

                # DEBUGGING: Visa vilken dörr zombierna gömmer sig bakom
                print(f"[DEBUG] Zombierna gömmer sig bakom dörr {zombie_door}.")

                chosen_door = input_valid_int(f"Vilken dörr väljer du (1-{doors})? ", 1, doors)

                if chosen_door == zombie_door:
                    print(f"Åh nej! Zombierna tog dig! De gömde sig bakom dörr {zombie_door}. Spelet är över! 😱")
                    won_game = False
                else:
                    print("Bra val! Nu måste du klara den **sista matematikfrågan** för att vinna!")

                    # Generera sista frågan
                    final_factor, final_answer = generate_question(operation, value, used_questions, question_limits)
                    print(f"Sista frågan: Vad är {final_factor} {operation} {value}?")
                    
                    final_user_answer = input_valid_int("Ditt svar: ", 0)

                    if final_user_answer == final_answer:
                        print("Grattis! Du klarade sista frågan och överlevde Zombie House! 🎉")
                        won_game = True
                    else:
                        print("Aj! Du svarade fel på sista frågan. Zombierna tog dig! 😱")
                        won_game = False

                break  # Spelet slutar här direkt efter sista matematiksfrågan

            if doors > 2:
                zombie_door = random.randint(1, doors)

                # DEBUGGING: Visa vilken dörr zombierna gömmer sig bakom
                print(f"[DEBUG] Zombierna gömmer sig bakom dörr {zombie_door}.")

                chosen_door = input_valid_int(f"Vilken dörr väljer du (1-{doors})? ", 1, doors)

                if chosen_door == zombie_door:
                    print(f"Åh nej! Zombierna tog dig! Spelet är över! 😱")
                    won_game = False
                    break

                doors -= 1  # Dörrantalet minskas korrekt och spelet fortsätter

        play_again = input_valid_str("Vill du spela igen? (yes/no): ", ["yes", "no"])
        if play_again != "yes":
            print("Tack för att du spelade Zombie House! Hejdå!")
            break

        if won_game:
            # Om spelaren vann, låt dem välja nya inställningar
            num_questions = input_valid_int("Välj antal frågor (12-39): ", 12, 39)
            operation = input_valid_str("Välj ett räknesätt (*, //, %): ", ["*", "//", "%"])
            if operation == "*":
                value = input_valid_int("Välj en multiplikationstabell (2-12): ", 2, 12)
            else:
                value = input_valid_int("Välj en divisor (2-5): ", 2, 5)

if __name__ == "__main__":
    main()

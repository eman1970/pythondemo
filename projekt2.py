import random

def generate_question(operation, value, used_questions, question_limits):
    """Genererar en unik matematisk fråga baserat på valt räknesätt."""
    attempts = 0
    while True:
        factor_or_dividend = random.randint(0, 12)
        question = (factor_or_dividend, value)

        max_occurrences = question_limits[0] if len(used_questions) < 14 else \
                          question_limits[1] if len(used_questions) < 27 else \
                          question_limits[2]

        if used_questions.get(question, 0) < max_occurrences:
            used_questions[question] = used_questions.get(question, 0) + 1
            
            if operation == "multiplikation":
                return factor_or_dividend, factor_or_dividend * value
            elif operation == "division":
                return factor_or_dividend, factor_or_dividend / value
            elif operation == "modulo":
                return factor_or_dividend, factor_or_dividend % value

        attempts += 1
        if attempts > 100:
            raise ValueError("Misslyckades med att generera en unik fråga.")

def choose_door(zombie_door, chosen_door):
    """Kontrollerar om användaren valde en säker dörr."""
    return chosen_door != zombie_door

def setup_zombie_door(doors):
    """Slumpmässigt väljer en dörr där zombiesarna gömmer sig."""
    return random.randint(1, doors)

def input_valid_int(prompt_text, min_value, max_value=None):
    """Validerar heltalsinmatning och säkerställer att det alltid är ett giltigt heltal."""
    while True:
        try:
            user_answer = int(input(prompt_text))
            if max_value is None or min_value <= user_answer <= max_value:
                return user_answer
            print(f"Felaktigt nummer! Ange ett heltal mellan {min_value} och {max_value}.")
        except ValueError:
            print("Felaktig inmatning! Ange ett giltigt heltal.")

def input_valid_str(prompt_text, valid_answers):
    """Validerar stränginmatning och säkerställer att användaren väljer ett giltigt alternativ."""
    while True:
        user_answer = input(prompt_text).strip().lower()
        if user_answer in valid_answers:
            return user_answer
        print(f"Felaktigt val! Ange ett av följande: {', '.join(valid_answers)}.")

def main():
    """Huvudfunktionen som hanterar hela spelet."""
    print("Välkommen till Zombiehuset! 🧟‍♂️")
    print("Du måste svara rätt på matematiska frågor och undvika zombiedörrar för att fly.")

    while True:
        num_questions = input_valid_int("Välj antal frågor (12-39): ", 12, 39)
        operation = input_valid_str("Välj räknesätt (multiplikation, division, modulo): ", 
                                    ["multiplikation", "division", "modulo"])
        
        if operation == "multiplikation":
            value = input_valid_int("Välj en multiplikationstabell (2-12): ", 2, 12)
        else:
            value = input_valid_int("Välj en divisor (2-5): ", 2, 5)

        used_questions = {}
        question_limits = (1, 2, 3)  # Max antal gånger en fråga får förekomma

        doors = num_questions  # Startvärde för antal dörrar

        for question_num in range(1, num_questions + 1):
            factor_or_dividend, correct_answer = generate_question(operation, value, used_questions, question_limits)
            print(f"\nFråga {question_num}: Vad är {factor_or_dividend} {operation} {value}?")
            user_answer = input_valid_int("Ditt svar: ", 0)

            if user_answer != correct_answer:
                print("Fel svar! Zombiesarna tog dig! Game over! 😱")
                break

            print(f"Rätt svar! Du har klarat {question_num} av {num_questions} frågor.")

            if question_num < num_questions - 1:  # Dörrval görs tills näst sista frågan
                print(f"Välj en dörr mellan 1 och {doors}. Zombiesarna gömmer sig bakom en av dem!")
                zombie_door = setup_zombie_door(doors)
                chosen_door = input_valid_int(f"Vilken dörr väljer du (1-{doors})? ", 1, doors)

                if not choose_door(zombie_door, chosen_door):
                    print(f"Oh nej! Zombiesarna tog dig! De gömde sig bakom dörr {zombie_door}. Game over! 😱")
                    break

                doors -= 1  # Minska antal dörrar efter varje runda
            else:
                print("Grattis! Du har klarat alla frågor och överlevt Zombiehuset! 🎉")

        play_again = input_valid_str("Vill du spela igen? (ja/nej): ", ["ja", "nej"])
        if play_again != "ja":
            print("Tack för att du spelade Zombiehuset! Hejdå!")
            break

if __name__ == "__main__":
    main()

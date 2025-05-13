import random

def generate_question(operation, value, used_questions):
    """Genererar en unik matematisk fråga baserat på vald operation."""
    attempts = 0
    possible_questions = [(operand, value) for operand in range(0, 13)]
    
    # Bestäm max upprepningar baserat på antal frågor
    max_repeats = (
        0 if len(used_questions) <= 13 else  # Ingen upprepning vid ≤13 frågor
        2 if len(used_questions) <= 26 else  # Max 2 upprepningar vid ≤26 frågor
        3  # Max 3 upprepningar vid >26 frågor
    )

    while True:
        available_questions = [q for q in possible_questions if used_questions.get(q, 0) < max_repeats]

        if not available_questions:
            print("[DEBUG] Inga fler unika frågor tillgängliga. Återanvänder en av de tidigare.")
            return random.choice(list(used_questions.keys()))[0], used_questions[random.choice(list(used_questions.keys()))]

        question = random.choice(available_questions)
        operand = question[0]

        operations = {
            "*": operand * value,
            "//": operand // value,
            "%": operand % value
        }

        answer = operations.get(operation)

        used_questions[question] = used_questions.get(question, 0) + 1
        return operand, answer

def input_valid_int(prompt_text, min_value, max_value=None):
    """Validerar heltalsinmatning och säkerställer att den är inom giltigt intervall."""
    while True:
        try:
            user_answer = int(input(prompt_text).strip())
            if max_value is None or min_value <= user_answer <= max_value:
                return user_answer
            print(f"Ogiltigt nummer! Ange ett tal mellan {min_value} och {max_value}.")
        except ValueError:
            print("Ogiltig inmatning! Ange ett giltigt heltal.")

def input_valid_str(prompt_text, valid_answers):
    """Validerar stränginmatning och säkerställer att användaren väljer ett giltigt alternativ."""
    while True:
        user_answer = input(prompt_text).strip().lower()
        if user_answer in valid_answers:
            return user_answer
        print(f"Ogiltigt val! Ange något av följande: {', '.join(valid_answers)}.")

def main():
    """Huvudfunktionen som styr hela spelet."""
    print("Välkommen till Zombie House! 🧟‍♂️")
    print("Du måste svara rätt på mattefrågor och undvika zombiedörrar för att fly.")

    num_questions = input_valid_int("Välj antal frågor (12-39): ", 12, 39)
    operation = input_valid_str("Välj en operation (*, //, %): ", ["*", "//", "%"])
    
    if operation == "*":
        value = input_valid_int("Välj multiplikationstabell (2-12): ", 2, 12)
    else:
        value = input_valid_int("Välj en divisor (2-5): ", 2, 5)

    while True:
        used_questions = {}
        doors = num_questions
        won_game = False

        for question_num in range(1, num_questions + 1):
            try:
                factor_or_dividend, correct_answer = generate_question(operation, value, used_questions)
            except ValueError as e:
                print(f"⚠️ Spelet kunde inte generera fler unika frågor: {e}")
                break

            print(f"\nFråga {question_num}: Vad blir {factor_or_dividend} {operation} {value}?")
            
            user_answer = input_valid_int("Ditt svar: ", 0)

            if user_answer != correct_answer:
                print("Fel svar! Zombierna fångade dig! Spelet är över! 😱")
                break

            print(f"Korrekt! Du har klarat {question_num} av {num_questions} frågor.")

            if doors > 1:
                zombie_door = random.randint(1, doors)
                
                # 🛠 Debugg-kod: Visa vilken dörr zombierna gömmer sig bakom innan valet
                print(f"\n🚪 [DEBUG] Zombierna gömmer sig bakom dörr {zombie_door}!")

                chosen_door = input_valid_int(f"Vilken dörr väljer du (1-{doors})? ", 1, doors)

                if chosen_door == zombie_door:
                    print(f"☠️ Ajdå! Zombierna fångade dig genom dörr {zombie_door}! Spelet är över.")
                    break

                doors -= 1
            else:
                print("🎉 Grattis! Du har klarat alla frågor och överlevt Zombie House!")
                won_game = True
                break

        play_again = input_valid_str("Vill du spela igen? (ja/nej): ", ["ja", "nej"])
        
        if play_again != "ja":
            print("👋 Tack för att du spelade Zombie House! Hejdå!")
            break

        if won_game:
            num_questions = input_valid_int("Välj antal frågor (12-39): ", 12, 39)
            operation = input_valid_str("Välj en operation (*, //, %): ", ["*", "//", "%"])
            if operation == "*":
                value = input_valid_int("Välj multiplikationstabell (2-12): ", 2, 12)
            else:
                value = input_valid_int("Välj en divisor (2-5): ", 2, 5)

if __name__ == "__main__":
    main()

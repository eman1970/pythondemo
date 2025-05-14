import random

# Globala konstanter
DEBUG = True  # Set to False to disable debug mode

def generate_question(operation, value, used_questions, max_repeats):
    """Genererar en matematisk fråga med begränsad upprepning"""
    possible_questions = [(operand, value) for operand in range(13)]
    available_questions = [q for q in possible_questions if used_questions.get(q, 0) <= max_repeats]
    
    if not available_questions:
        return None

    question = random.choice(available_questions)
    operand = question[0]
    answer = {
        "*": operand * value,
        "//": operand // value,
        "%": operand % value
    }.get(operation)

    used_questions[question] = used_questions.get(question, 0) + 1
    return operand, answer

def validate_int(prompt_text, min_value, max_value=None):
    """Validerar heltalsinput"""
    while True:
        try:
            user_input = int(input(prompt_text))
            if max_value is None or min_value <= user_input <= max_value:
                return user_input
            print(f"Fel! Ange ett tal mellan {min_value} och {max_value}.")
        except ValueError:
            print("Ogiltig inmatning! Ange ett heltal.")

def validate_str(prompt_text, valid_answers):
    """Validerar stränginput mot giltiga alternativ"""
    while True:
        user_input = input(prompt_text).strip().lower()
        if user_input in valid_answers:
            return user_input
        print(f"Fel! Ange något av: {', '.join(valid_answers)}")

def handle_door_selection(doors):
    """Hanterar dörrval och returnerar vald dörr"""
    return validate_int(f"Välj dörr (1-{doors}): ", 1, doors)

def main():
    """Huvudfunktion med centraliserade utskrifter"""
    print("Välkommen till Zombie House!")
    print("Svara rätt på mattefrågor och undvik zombiedörrar för att fly.")

    # Spelinställningar
    num_questions = validate_int("Antal frågor (12-39): ", 12, 39)
    operation = validate_str("Räknesätt (*, //, %): ", ["*", "//", "%"])
    value = validate_int(
        f"Multiplikationstabell (2-12): " if operation == "*" else "Divisor (2-5): ",
        2, 12 if operation == "*" else 5
    )

    while True:
        used_questions = {}
        max_repeats = 0 if num_questions < 14 else 1 if num_questions <= 26 else 2
        doors = num_questions
        won_game = False

        for question_num in range(1, num_questions + 1):
            # Frågedel
            question_data = generate_question(operation, value, used_questions, max_repeats)
            if not question_data:
                print("Inga fler unika frågor!")
                break

            operand, correct = question_data
            user_answer = validate_int(
                f"\nFråga {question_num}/{num_questions}: {operand} {operation} {value} = ? ", 0)

            if user_answer != correct:
                print("Fel! Zombierna attackerar!")
                break

            print("Rätt! Du överlevde denna runda.")

            # Dörrdel med centraliserade utskrifter
            if doors > 1:
                zombie_door = random.randint(1, doors)
                
                # Debug-utskrift 
                if DEBUG:
                    print(f"\n[DEBUG] Zombies are behind door: {zombie_door}")
                
                chosen_door = handle_door_selection(doors)
                
                # Alltid visa zombiedörr efter val
                print(f"\nYou chose door {chosen_door}, zombies were behind door {zombie_door}")
                
                if chosen_door == zombie_door:
                    print("Zombierna fångade dig! Spelet är över.")
                    break

                doors -= 1
                print(f"{doors} dörrar kvar")

                if doors == 1:  # Sista frågan
                    final_question = generate_question(operation, value, used_questions, max_repeats)
                    if not final_question:
                        print("Kunde inte generera sista fråga!")
                        break

                    final_op, final_corr = final_question
                    final_ans = validate_int(f"\nSista fråga: {final_op} {operation} {value} = ? ", 0)
                    
                    won_game = final_ans == final_corr
                    print("GRATTIS! Du vann!" if won_game else "Sista frågan blev din undergång!")
                    break

        # Spela igen-logik
        if not validate_str("\nSpela igen? (ja/nej): ", ["ja", "nej"]) == "ja":
            print("Tack för att du spelade!")
            break

        if won_game:
            print("Startar om med nya inställningar...")
            num_questions = validate_int("Antal frågor (12-39): ", 12, 39)
            operation = validate_str("Räknesätt (*, //, %): ", ["*", "//", "%"])
            value = validate_int(
                "Multiplikationstabell (2-12): " if operation == "*" else "Divisor (2-5): ",
                2, 12 if operation == "*" else 5
            )

if __name__ == "__main__":
    main()
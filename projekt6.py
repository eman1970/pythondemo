import random

def generate_question(operation, value, used_questions, max_repeats):
    """Genererar en matematisk fråga och hanterar återanvändning av frågor."""
    possible_questions = [(operand, value) for operand in range(0, 13)]
    
    # Filtrera frågor som inte överskridit max upprepningar
    available_questions = [q for q in possible_questions if used_questions.get(q, 0) <= max_repeats]

    if not available_questions:
        return None  # Inga fler unika frågor tillgängliga

    question = random.choice(available_questions)
    operand = question[0]

    operations = {
        "*": operand * value,
        "//": operand // value,
        "%": operand % value
    }

    answer = operations.get(operation)

    if answer is None:
        return None

    used_questions[question] = used_questions.get(question, 0) + 1
    return operand, answer

def validate_int(prompt_text, min_value, max_value=None):
    """Validerar heltalsinmatning och säkerställer att det ligger inom giltigt intervall."""
    while True:
        try:
            user_answer = int(input(prompt_text).strip())
            if max_value is None or min_value <= user_answer <= max_value:
                return user_answer
            print(f"🚫 Fel! Ange ett tal mellan {min_value} och {max_value}.")
        except ValueError:
            print("🚫 Ogiltig inmatning! Ange ett heltal.")

def validate_str(prompt_text, valid_answers):
    """Validerar stränginmatning och säkerställer att det är ett giltigt alternativ."""
    while True:
        user_answer = input(prompt_text).strip().lower()
        if user_answer in valid_answers:
            return user_answer
        print(f"🚫 Fel! Ange något av följande: {', '.join(valid_answers)}.")

def main():
    print("Välkommen till Zombie House! 🧟‍♂️")
    print("Svara rätt på mattefrågor och undvik zombiedörrar för att fly.")

    num_questions = validate_int("Antal frågor (12-39): ", 12, 39)
    operation = validate_str("Räknesätt (*, //, %): ", ["*", "//", "%"])
    
    if operation == "*":
        value = validate_int("Multiplikationstabell (2-12): ", 2, 12)
    else:
        value = validate_int("Divisor (2-5): ", 2, 5)

    while True:
        used_questions = {}
        max_repeats = (
            0 if num_questions < 14 else
            1 if num_questions <= 26 else
            2
        )
        doors = num_questions
        won_game = False

        for question_num in range(1, num_questions + 1):
            question_data = generate_question(operation, value, used_questions, max_repeats)
            if question_data is None:
                print("⚠️ Kunde inte skapa fler unika frågor!")
                break

            operand, correct_answer = question_data
            user_answer = validate_int(f"\n🔢 Fråga {question_num}/{num_questions}: {operand} {operation} {value} = ? ", 0)

            if user_answer != correct_answer:
                print("❌ Fel! Zombierna attackerar! 😱")
                break

            print("✅ Rätt! Du överlevde denna runda.")

            # Dörrvalssekvens med debug-information
            if doors == 2:
                zombie_door = random.randint(1, doors)
                print(f"\n🚪 [DEBUG] Zombierna gömmer sig bakom dörr {zombie_door}!")

                chosen_door = validate_int(f"Välj dörr (1-{doors}): ", 1, doors)

                if chosen_door == zombie_door:
                    print(f"☠️ Zombierna fångade dig genom dörr {zombie_door}! Spelet är över.")
                    break

                print("🌟 Bra val! Sista frågan nu...")

                # Sista matematikfrågan
                final_question_data = generate_question(operation, value, used_questions, max_repeats)
                if final_question_data is None:
                    print("⚠️ Kunde inte generera sista fråga!")
                    break

                final_operand, final_correct = final_question_data
                final_answer = validate_int(f"\n⚡ Sista fråga: {final_operand} {operation} {value} = ? ", 0)

                if final_answer == final_correct:
                    print("🎉 GRATTIS! Du överlevde Zombie House!")
                    won_game = True
                else:
                    print("☠️ Sista frågan blev din undergång!")
                break  # Spelet avslutas efter sista frågan.

            zombie_door = random.randint(1, doors)
            print(f"\n🚪 [DEBUG] Zombierna gömmer sig bakom dörr {zombie_door}!")

            chosen_door = validate_int(f"Välj dörr (1-{doors}): ", 1, doors)

            if chosen_door == zombie_door:
                print(f"☠️ Zombierna fångade dig genom dörr {zombie_door}! Spelet är över.")
                break

            doors -= 1
            print(f"Du har {doors} dörrar kvar att välja mellan.")

        play_again = validate_str("\nSpela igen? (ja/nej): ", ["ja", "nej"])

        if play_again != "ja":
            print("👋 Tack för att du spelade!")
            break  # Avsluta spelet om användaren inte vill spela igen

        if won_game:
            print("Startar om spelet med **nya inställningar**...")
            num_questions = validate_int("Antal frågor (12-39): ", 12, 39)
            operation = validate_str("Räknesätt (*, //, %): ", ["*", "//", "%"])
            if operation == "*":
                value = validate_int("Multiplikationstabell (2-12): ", 2, 12)
            else:
                value = validate_int("Divisor (2-5): ", 2, 5)
        else:
            print("Startar om spelet med **samma inställningar**...")

if __name__ == "__main__":
    main()

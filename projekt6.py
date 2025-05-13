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

def validate_int(user_input, min_value, max_value=None):
    """Validerar om inmatning är ett giltigt heltal inom rätt intervall."""
    try:
        user_answer = int(user_input.strip())
        if max_value is None or min_value <= user_answer <= max_value:
            return user_answer
    except ValueError:
        return None
    return None

def validate_str(user_input, valid_answers):
    """Validerar om stränginmatning är ett giltigt val."""
    user_answer = user_input.strip().lower()
    return user_answer if user_answer in valid_answers else None

def main():
    print("Välkommen till Zombie House! 🧟‍♂️")
    print("Svara rätt på mattefrågor och undvik zombiedörrar för att fly.")

    num_questions = validate_int(input("Antal frågor (12-39): "), 12, 39)
    operation = validate_str(input("Räknesätt (*, //, %): "), ["*", "//", "%"])
    
    if operation == "*":
        value = validate_int(input("Multiplikationstabell (2-12): "), 2, 12)
    else:
        value = validate_int(input("Divisor (2-5): "), 2, 5)

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
            user_answer = validate_int(input(f"\n🔢 Fråga {question_num}/{num_questions}: {operand} {operation} {value} = ? "), 0)

            if user_answer != correct_answer:
                print("❌ Fel! Zombierna attackerar! 😱")
                break

            print("✅ Rätt! Du överlevde denna runda.")

            # Dörrvalssekvens med debug-information
            zombie_door = random.randint(1, doors)
            print(f"\n🚪 [DEBUG] Zombierna gömmer sig bakom dörr {zombie_door}!")

            chosen = validate_int(input(f"Välj dörr (1-{doors}): "), 1, doors)

            if chosen == zombie_door:
                print(f"☠️ Zombierna fångade dig i dörr {zombie_door}!")
                break

            doors -= 1
            print(f"Du har {doors} dörrar kvar att välja mellan.")

            if doors == 1:
                print("🎉 Grattis! Du har klarat alla frågor och överlevt Zombie House!")
                won_game = True

        play_again = validate_str(input("\nSpela igen? (ja/nej): "), ["ja", "nej"])

        if play_again != "ja":
            print("👋 Tack för att du spelade!")
            break  # Avsluta spelet om användaren inte vill spela igen

        if won_game:
            print("Startar om spelet med **nya inställningar**...")
            num_questions = validate_int(input("Antal frågor (12-39): "), 12, 39)
            operation = validate_str(input("Räknesätt (*, //, %): "), ["*", "//", "%"])
            value = validate_int(input("Multiplikationstabell (2-12) eller divisor (2-5): "), 2, 12 if operation == "*" else 2, 5)
        else:
            print("Startar om spelet med **samma inställningar**...")

if __name__ == "__main__":
    main()

import random

def generate_question(operation, value, used_questions, max_repeats):
    """Genererar en matematisk fråga och hanterar återanvändning av frågor."""
    possible_questions = [(operand, value) for operand in range(0, 13)]

    # Filtrera frågor som inte överskridit max upprepningar
    available_questions = [q for q in possible_questions if used_questions.get(q, 0) <= max_repeats]

    if not available_questions:
        raise ValueError("Inga fler unika frågor tillgängliga")

    question = random.choice(available_questions)
    operand = question[0]

    # Uppdaterad operations-dictionary utan onödig nollkontroll
    operations = {
        "*": operand * value,
        "//": operand // value,
        "%": operand % value
    }

    answer = operations.get(operation)

    if answer is None:
        raise ValueError("Ogiltig operation!")

    used_questions[question] = used_questions.get(question, 0) + 1
    return question[0], answer

def input_valid_int(prompt_text, min_value, max_value=None):
    """Validerar heltalsinmatning."""
    while True:
        try:
            user_answer = int(input(prompt_text).strip())
            if max_value is None or min_value <= user_answer <= max_value:
                return user_answer
            print(f"Ogiltigt nummer! Ange mellan {min_value} - {max_value}.")
        except ValueError:
            print("Ogiltig inmatning! Ange ett heltal.")

def input_valid_str(prompt_text, valid_answers):
    """Validerar stränginmatning."""
    while True:
        user_answer = input(prompt_text).strip().lower()
        if user_answer in valid_answers:
            return user_answer
        print(f"Ogiltigt val! Välj bland: {', '.join(valid_answers)}")

def main():
    print("Välkommen till Zombie House! 🧟‍♂️")
    print("Svara rätt på mattefrågor och undvik zombiedörrar för att fly.")

    # Spelinställningar
    num_questions = input_valid_int("Antal frågor (12-39): ", 12, 39)
    operation = input_valid_str("Räknesätt (*, //, %): ", ["*", "//", "%"])

    if operation == "*":
        value = input_valid_int("Multiplikationstabell (2-12): ", 2, 12)
    else:
        value = input_valid_int("Divisor (2-5): ", 2, 5)

    while True:
        used_questions = {}

        # Uppdaterade repetitionsregler enligt din önskan:
        if num_questions < 14:
            max_repeats = 0  # Ingen upprepning
        elif num_questions <= 26:
            max_repeats = 1  # Max 2 gånger
        else:
            max_repeats = 2  # Max 3 gånger

        doors = num_questions
        won_game = False

        for question_num in range(1, num_questions + 1):
            try:
                x, correct = generate_question(operation, value, used_questions, max_repeats)
            except ValueError:
                print("⚠️ Kunde inte skapa fler unika frågor!")
                print(f"Använda frågor: {used_questions}")
                break

            print(f"\n🔢 Fråga {question_num}/{num_questions}: {x} {operation} {value} = ?")
            user_answer = input_valid_int("Ditt svar: ", 0)

            if user_answer != correct:
                print("❌ Fel! Zombierna attackerar! 😱")
                break

            print("✅ Rätt! Du överlevde denna runda.")

            # Dörrvalssekvens med debug
            if doors == 2:
                zombie_door = random.randint(1, doors)
                print(f"\n🚪 [DEBUG] Zombier bakom dörr {zombie_door}")
                chosen = input_valid_int(f"Välj dörr (1-{doors}): ", 1, doors)

                if chosen == zombie_door:
                    print(f"☠️ Zombierna fångade dig i dörr {zombie_door}!")
                    break
                else:
                    print("🌟 Bra val! Sista frågan nu...")
                    try:
                        fx, fc = generate_question(operation, value, used_questions, max_repeats)
                    except ValueError:
                        print("⚠️ Kunde inte generera sista fråga!")
                        break

                    print(f"\n⚡ Sista fråga: {fx} {operation} {value} = ?")
                    final_answer = input_valid_int("Slutgiltigt svar: ", 0)

                    if final_answer == fc:
                        print("🎉 GRATTIS! Du överlevde Zombie House!")
                        won_game = True
                    else:
                        print("☠️ Sista frågan blev din undergång!")
                    break

            if doors > 2:
                zombie_door = random.randint(1, doors)
                print(f"\n🚪 [DEBUG] Zombier bakom dörr {zombie_door}")
                chosen = input_valid_int(f"Välj dörr (1-{doors}): ", 1, doors)

                if chosen == zombie_door:
                    print(f"☠️ Zombierna drog in dig genom dörr {zombie_door}!")
                    break

                doors -= 1
                print(f"Du har {doors} dörrar kvar att välja mellan.")

        # Avslutning
        play_again = input_valid_str("\nSpela igen? (ja/nej): ", ["ja", "nej"])

        if play_again == "ja":
            if won_game:
                # Om spelaren vann, fråga om nya inställningar
                num_questions = input_valid_int("Antal frågor (12-39): ", 12, 39)
                operation = input_valid_str("Räknesätt (*, //, %): ", ["*", "//", "%"])
                if operation == "*":
                    value = input_valid_int("Multiplikationstabell (2-12): ", 2, 12)
                else:
                    value = input_valid_int("Divisor (2-5): ", 2, 5)
            else:
                print("Startar om spelet med samma inställningar...")
        else:
            print("👋 Tack för att du spelade!")
            break

if __name__ == "__main__":
    main()

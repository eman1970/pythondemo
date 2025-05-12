import random

def generate_question(table, used_questions):
    """Genererar en unik multiplikationsfråga baserad på den valda tabellen.

    Args:
        table (int): Multiplikationstabellen som används (2-12).
        used_questions (set): En uppsättning av redan använda faktorer.

    Returns:
        tuple: En faktor och det korrekta svaret för frågan.
    """
    while True:
        factor = random.randint(0, 12)
        if factor not in used_questions:
            used_questions.add(factor)
            return factor, factor * table

def choose_door(zombie_door, chosen_door):
    """Kontrollerar om spelaren har valt en säker dörr.

    Args:
        zombie_door (int): Dörrnumret där zombiesarna gömmer sig.
        chosen_door (int): Spelarens valda dörrnummer.

    Returns:
        bool: True om spelaren valde en säker dörr, False om zombiesarna fångade dem.
    """
    return chosen_door != zombie_door

def setup_zombie_door(doors):
    """Slumpar en dörr där zombiesarna gömmer sig.

    Args:
        doors (int): Totala antalet dörrar som finns tillgängliga.

    Returns:
        int: Numret på den dörr där zombiesarna gömmer sig.
    """
    return random.randint(1, doors)

def input_valid_int(prompt_text, min_value, max_value=None):
    """Tar emot och validerar en heltalsinmatning från användaren.

    Args:
        prompt_text (str): Texten som visas för användaren vid inmatning.
        min_value (int): Det lägsta giltiga värdet.
        max_value (int, optional): Det högsta giltiga värdet. Standard är None.

    Returns:
        int | None: Returnerar det giltiga heltalet, eller None vid felaktig inmatning.
    """
    try:
        user_answer = int(input(prompt_text))
        if max_value is None or min_value <= user_answer <= max_value:
            return user_answer
        return None  # Om numret är utanför tillåtet intervall
    except ValueError:
        return None  # Returnerar None vid felaktig inmatning

def input_valid_str(prompt_text, valid_answers):
    """Tar emot och validerar en stränginmatning från användaren.

    Args:
        prompt_text (str): Texten som visas för användaren vid inmatning.
        valid_answers (list): En lista med giltiga svarsalternativ.

    Returns:
        str | None: Returnerar en giltig sträng, eller None om inmatningen är ogiltig.
    """
    user_answer = input(prompt_text).strip().lower()
    return user_answer if user_answer in valid_answers else None

def main():
    """Huvudfunktionen som hanterar spelet Zombiehuset.

    - Spelaren väljer en multiplikationstabell och svarar på 12 frågor.
    - Efter varje korrekt svar måste spelaren välja en dörr för att undvika zombies.
    - Spelet fortsätter tills spelaren svarar fel eller väljer en dörr där zombies gömmer sig.
    - Om alla 12 frågor besvaras korrekt överlever spelaren.

    Funktionen hanterar även användarinmatning och ser till att den är giltig.
    """
    print("Välkommen till Zombiehuset! 🧟‍♂️")
    print("Du måste svara rätt på matematiska frågor och undvika zombiedörrar för att fly.")

    while True:
        # Väljer multiplikationstabell, ser till att inmatningen är giltig
        table = None
        while table is None:
            table = input_valid_int("Välj en multiplikationstabell (2-12): ", 2, 12)
            if table is None:
                print("Felaktigt nummer! Ange ett heltal mellan 2 och 12.")

        used_questions = set()
        doors = 12  # Totalt antal dörrar i spelet

        for question_num in range(1, 13):
            factor, correct_answer = generate_question(table, used_questions)
            print(f"\nFråga {question_num}: Vad är {factor} * {table}?")

            # Kontroll av giltig inmatning för spelarens svar
            user_answer = None
            while user_answer is None:
                user_answer = input_valid_int("Ditt svar: ", 0)
                if user_answer is None:
                    print("Felaktig inmatning! Ange ett giltigt heltal.")

            if user_answer != correct_answer:
                print("Fel svar! Zombiesarna tog dig! Game over! 😱")
                break

            print(f"Rätt svar! Du har klarat {question_num} av 12 frågor.")

            if question_num < 12:
                zombie_door = setup_zombie_door(doors)
                print(f"[DEBUG] Zombiesarna gömmer sig bakom dörr {zombie_door}.")

                # Kontroll av giltig dörrval
                chosen_door = None
                while chosen_door is None:
                    chosen_door = input_valid_int(f"Välj en dörr mellan 1 och {doors}: ", 1, doors)
                    if chosen_door is None:
                        print(f"Felaktigt nummer! Ange ett heltal mellan 1 och {doors}.")

                # Meddelar spelaren om zombiesarnas position innan spelet fortsätter
                if not choose_door(zombie_door, chosen_door):
                    print(f"Oh nej! Zombiesarna tog dig! De gömde sig bakom dörr {zombie_door}. Game over! 😱")
                    break  
                else:
                    print(f"Puh! Du valde rätt dörr. Zombiesarna gömde sig bakom dörr {zombie_door}. Du klarade denna runda! 🎉")

                doors -= 1  # Minska antal dörrar efter varje runda
            else:
                print("Grattis! Du har klarat alla frågor och överlevt Zombiehuset! 🎉")

        # Frågar spelaren om de vill spela igen och säkerställer giltig inmatning
        play_again = None
        while play_again is None:
            play_again = input_valid_str("Vill du spela igen? (ja/nej): ", ["ja", "nej"])
            if play_again is None:
                print("Felaktigt val! Ange 'ja' eller 'nej'.")

        if play_again != "ja":
            print("Tack för att du spelade Zombiehuset! Hejdå!")
            break

if __name__ == "__main__":
    main()

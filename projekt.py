import random, math 

MIN_TABLE = 2
MAX_TABLE = 12
TOTAL_QUESTIONS = 12
INITIAL_DOORS = 12
DEBUG = True

def generate_question(table, used_questions):
    """Genererar en unik multiplikationsfråga baserad på den valda tabellen.

    Args:
        table (int): Multiplikationstabellen som används (2-12).
        used_questions (set): En uppsättning av redan använda faktorer.

    Returns:
        tuple: En faktor och det korrekta svaret för frågan.
    """
    while True:
        factor = random.randint(0, MAX_TABLE)
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

def input_valid_int(question, prompt_text, min_value, max_value):
    """Tar emot och validerar en heltalsinmatning från användaren.

    Args:
        prompt_text (str): Texten som visas för användaren vid inmatning.
        min_value (int): Det lägsta giltiga värdet.
        max_value (int, optional): Det högsta giltiga värdet. Standard är None.

    Returns:
        int | None: Returnerar det giltiga heltalet, eller None vid felaktig inmatning.
    """ 
    while True:  # Loopa tills korrekt värde skrivs in
        user_input = input(question)
        if user_input.isdigit():
            user_int = int(user_input)
            if user_int >= min_value and (max_value is None or user_int <= max_value):
                return user_int  # Korrekt tal, returnera värdet
        print(prompt_text)
        
def input_valid_str(question, prompt_text, valid_answers):
    """Tar emot och validerar en stränginmatning från användaren.

    Args:
        prompt_text (str): Texten som visas för användaren vid inmatning.
        valid_answers (list): En lista med giltiga svarsalternativ.

    Returns:
        str | None: Returnerar en giltig sträng, eller None om inmatningen är ogiltig.
    """
    while True:
        user_input = input(question).strip().lower()
        if user_input in valid_answers:
            return user_input
        print(prompt_text)

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

    while True:  # Huvudloop för spelomgångar
        # Spelinitiering
        table = None
        while table is None:
            table = input_valid_int(f"Välj en multiplikationstabell ({MIN_TABLE}-{MAX_TABLE}): ", 
                                  "Felaktig inmatning! Ange ett giltigt heltal.", MIN_TABLE, MAX_TABLE)
        used_questions = set()
        doors = INITIAL_DOORS

        # Spelloop för frågor
        for question_num in range(1, TOTAL_QUESTIONS + 1):
            factor, correct_answer = generate_question(table, used_questions)
            print(f"\nFråga {question_num}: Vad är {factor} * {table}?")

            user_answer = None
            while user_answer is None:
                user_answer = input_valid_int("Ditt svar: ", "Felaktig inmatning! Ange ett giltigt heltal.", 0, math.inf)

            if user_answer != correct_answer:
                print("Fel svar! Zombiesarna tog dig! Game over! 😱")
                break

            print(f"Rätt svar! Du har klarat {question_num} av {TOTAL_QUESTIONS} frågor.")

            if question_num < TOTAL_QUESTIONS:
                zombie_door = setup_zombie_door(doors)
                
                if DEBUG:  # <-- Debug-meddelande som bara visas när DEBUG är True
                    print(f"[DEBUG] Zombiesarna gömmer sig bakom dörr {zombie_door}.")


                chosen_door = None
                while chosen_door is None:
                    chosen_door = input_valid_int(f"Välj en dörr mellan 1 och {doors}: ",
                                                f"Felaktigt val! Ange ett heltal mellan 1 och {doors}.", 1, doors)

                if not choose_door(zombie_door, chosen_door):
                    print(f"Oh nej! Zombiesarna tog dig! De gömde sig bakom dörr {zombie_door}. Game over! 😱")
                    break
                else:
                    print(f"Puh! Du valde rätt dörr. Zombiesarna gömde sig bakom dörr {zombie_door}. Du klarade denna runda! 🎉")
                    doors -= 1
            else:
                print("Grattis! Du har klarat alla frågor och överlevt Zombiehuset! 🎉")

        # Hantera "spela igen" utan nested loop
        play_again = input_valid_str("Vill du spela igen? (ja/nej): ",
                                   "Felaktigt val! Ange 'ja' eller 'nej'.", ["ja", "nej"])
        if play_again != "ja":
            print("Tack för att du spelade Zombiehuset! Hejdå!")
            break
    
if __name__ == "__main__":
    main()
               
        
    


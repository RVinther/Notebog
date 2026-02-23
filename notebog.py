from pathlib import Path
import json
import shutil

BASE_DIR = Path.home() / ".Notebog"
BASE_DIR.mkdir(parents=True, exist_ok=True)
JSON_FIL = BASE_DIR / "Notebog.json"

def init_filer():
    for fil in [JSON_FIL]:
        if not fil.exists():
            fil.touch()

def hent_json():
    try:
        with open(JSON_FIL, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def backup_json():
    if JSON_FIL.exist():
        backup = JSON_FIL.with_suffix(".backup.json")
        shutil.copy(JSON_FIL, backup)

def gem_json(notes):
    backup_json()
    with open(JSON_FIL, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4, ensure_ascii=False)

def add_note(notes):
    term = input("Indtast begreb > ").strip().upper()
    if term == "":
        return "Du glemte at indtaste et begreb!"
    
    for note in notes:
        if note["term"] == term:
            return f"Begrebet [{term}] findes allerede i notebogen!"
    definition = input("Indtast definition > ")
    notes.append({
        "term": term,
        "definition": definition
    })
    gem_json(notes)
    return "Noteret!"

def vis_noter(notes):
    if not notes:
        return ["Der findes endnu ingen noter!"]
    sorterede = sorted(notes, key=lambda x: x["term"])
    return [f"[{n['term']}] = {n['definition']}" for n in sorterede]

def søg_note(notes):
    søg = input("Søg efter begreb > ").strip().upper()
    try:
        if søg == "":
            raise ValueError("Hov, du glemte at indtaste et begreb!")
    except ValueError as e:
        return f"Fejl: {e}"
    else:
        for n in notes:
            if n['term'] == søg:
                return f"[{n['term']}] = {n['definition']}"

        return f"Begreb [{søg}] findes ikke i notebogen!"
        
def slet_note(notes):
    slet_term = input("Indtast begreb, du vil slette > ").strip().upper()    
    ny_liste = [n for n in notes if n['term'] != slet_term]

    if len(ny_liste) == len(notes):
        return f"Begreb [{slet_term}] findes ikke!", notes
    
    gem_json(ny_liste)
    return f"Begreb [{slet_term}] er nu slettet!", ny_liste

def red_note(notes):
    term = input("Indtast begreb at redigere > ").strip().upper()

    if term not in [n["term"] for n in notes]:
        return f"Begreb [{term}] findes ikke!", notes
    
    ny_liste = [n for n in notes if n["term"] != term]

    ny_def = input("Redigér definition > ")

    ny_liste.append({
        "term": term,
        "definition": ny_def
    })

    gem_json(ny_liste)
    return f"[{term}] er nu opdateret!", ny_liste

def main():
    init_filer()
    notes = hent_json()
    
    print("Starter notebogen...")

    while True:
        print("== NOTEBOG ===")
        print("1. Se noter")
        print("2. Søg i noter")
        print("3. Tilføj note")
        print("4. Rediger note")
        print("5. Slet note")
        print("6. Afslut")

        valg = input("Vælg > ").strip()

        if valg == "1":
            resultat = vis_noter(notes)
            for r in resultat:
                print(r)
        
        elif valg == "2":
            resultat = søg_note(notes)
            print(resultat)

                    
        elif valg == "3":
            resultat = add_note(notes)
            print(resultat)

        elif valg == "4":
            besked, notes = red_note(notes)
            print(besked)

        elif valg == "5":
            besked, notes = slet_note(notes)
            print(besked)

        elif valg == "6":
            print("Afslutter notebogen...")
            break
        
        else:
            print("Ugyldigt input. Prøv igen!")
            
if __name__ == "__main__":
    main()
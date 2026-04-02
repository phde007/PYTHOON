import json
from tkinter import filedialog

def sauvegarder_dossier(dictionnaire_complet):
    """Sauvegarde le dictionnaire complet (chantier + zones) dans un fichier JSON."""
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Fichiers JSON", "*.json")]
    )
    
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            # On écrit directement le dictionnaire fourni
            json.dump(dictionnaire_complet, f, indent=4, ensure_ascii=False)
        return True
    return False

def charger_dossier():
    filepath = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
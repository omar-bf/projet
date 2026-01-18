import tkinter as tk
from tkinter import messagebox

def read_words(filename):
    words = []
    with open(filename, 'r') as f:
        for line in f:
            word = line.strip().upper()
            if len(word) >= 3:
                words.append(word)
    return words

def read_sequences(filename):
    sequences = {}
    current_id = None
    current_seq = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_id:
                    sequences[current_id] = "".join(current_seq)
                parts = line.split('|')
                if len(parts) > 1:
                    current_id = parts[1]
                current_seq = []
            else:
                current_seq.append(line)
        if current_id:
            sequences[current_id] = "".join(current_seq)
    return sequences

def search_words_in_proteome(word_list, protein_dict):
    results = {}
    for word in word_list:
        count = 0
        for seq in protein_dict.values():
            if word in seq:
                count += 1
        if count > 0:
            results[word] = count
            print(word, "found in", count, "sequences")
    return results

def find_most_frequent_word(results_dict):
    if not results_dict:
        return None, 0
    word = max(results_dict, key=results_dict.get)
    return word, results_dict[word]

# --- TRAITEMENT DES DONNEES ---
# Etape 1 [cite: 15, 16]
mots_selectionnes = read_words("english-common-words.txt")
print("Nombre de mots selectionnes:", len(mots_selectionnes))

# Etape 2 [cite: 39, 41, 42]
proteome = read_sequences("human-proteome.fasta")
print("Nombre de sequences lues:", len(proteome))
if "095139" in proteome:
    print("Sequence associée à 095139:", proteome["095139"])

# Etape 3 [cite: 44, 46, 52]
resultats_complets = search_words_in_proteome(mots_selectionnes, proteome)

# Etape 4 [cite: 54, 55, 57]
top_m, top_c = find_most_frequent_word(resultats_complets)
if top_m:
    pourcentage = (top_c / len(proteome)) * 100
    print("=>", top_m, "found in", top_c, "sequences")
    print("Pourcentage:", pourcentage, "%")

# --- INTERFACE GRAPHIQUE (GUI) [cite: 64, 69] ---

def chercher():
    mot = E1.get().upper()
    if mot in resultats_complets:
        messagebox.showinfo("Resultat", mot + " trouvé dans " + str(resultats_complets[mot]) + " sequences")
    else:
        messagebox.showinfo("Resultat", "Mot non trouvé dans le protéome")

main = tk.Tk()
main.title("Hire now") # [cite: 78, 90]

# Label et Entry comme dans le PDF [cite: 92, 94, 96, 98]
L1 = tk.Label(main, text="User Name")
L1.pack(side=tk.LEFT)
E1 = tk.Entry(main, bd=5)
E1.pack(side=tk.RIGHT)

# Boutons comme dans le PDF [cite: 112, 114, 117, 119]
B1 = tk.Button(main, text="Ok", command=chercher)
B1.pack(side=tk.LEFT)
B2 = tk.Button(main, text="Cancel", command=main.destroy)
B2.pack(side=tk.RIGHT)

main.mainloop() # [cite: 79, 99, 125]
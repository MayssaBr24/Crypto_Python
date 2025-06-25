import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import collections
from sympy import randprime
from math import gcd as pgcd


#Fonctions de Base Formate le texte par blocs de 5 caractères pour
# une meilleure lisibilité c'est un deal que nous avans fait en classe


def formatage(text, chiffrer=True):
    if chiffrer:
        text = text.upper()
        text2 = ""
        c = 0
        for char in text:
            text2 += char
            c += 1
            if c == 5:
                text2 += ' '
                c = 0
        return text2
    else:
        text = text.lower()
        text2 = ""
        c = 0
        for char in text:
            text2 += char
            c += 1
            if c == 5:
                text2 += ' '
                c = 0
        return text2

# methode classique de chiffrement
#Décalage simple des lettres dans l'alphabet.
def cesar(text, decalage, chiffrer=True):
    text = text.replace(' ', '').upper()
    result = []
    for char in text:
        if char.isalpha():
            if chiffrer:
                new_char = chr(((ord(char) - ord('A') + decalage) % 26) + ord('A'))
            else:
                new_char = chr(((ord(char) - ord('A') - decalage) % 26) + ord('A'))
            result.append(new_char)


    txt_result = ""
    for c in result:
        txt_result += c
    return formatage(txt_result, chiffrer)


def horisental(cle):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cle2 = cle.upper()
    cle3 = ""
    for i in cle2:
        if i in alphabet:
            cle3 += i
            alphabet = alphabet.replace(i, '')
    return cle3 + alphabet


def vertical(cle):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cle2 = cle.upper()
    cle3 = ""
    for i in cle2:
        if i in alphabet:
            cle3 += i
            alphabet = alphabet.replace(i, '')
    cle4 = cle3 + alphabet
    cle5 = ""
    for j in range(len(cle3)):
        for i in range(j, len(cle4), len(cle3)):
            cle5 += cle4[i]
    return cle5

# Crée un alphabet mélangé à partir d'une clé
def alphabet_desordonne(text, cle, chiffrer=True):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.replace(' ', '')
    text = text.upper()
    if chiffrer:
        txtchiffrer = ""
        for i in text:
            txtchiffrer += cle[alphabet.find(i)]
        return formatage(txtchiffrer, True)
    else:
        clair = ""
        for i in text:
            clair += alphabet[cle.find(i)]
        return formatage(clair, False)

# Réorganise les lettres selon un motif défini par une clé
def cle_transposition(cle):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cle = cle.upper()
    cle2 = ""
    for i in alphabet:
        for j in cle:
            if i == j:
                cle2 += j
    cle3 = []
    cle4 = []
    for i in cle:
        cle4.append(i)
    for i in cle4:
        cle3.append((cle2.index(i)))
        cle4[cle4.index(i)] = '#'
    return cle3


def transposition(text, cle, chiffrer=True):
    text = text.replace(' ', '')
    text = text.upper()
    if chiffrer:
        txtchiffrer = ""
        while len(text) % len(cle) != 0:
            text += "X"
        blocs = []
        for i in range(0, len(text), len(cle)):
            blocs.append(text[i:i + len(cle)])

        for i in blocs:
            bl = ""
            for j in range(len(cle)):
                bl += i[cle[j]]
            txtchiffrer += bl
        return formatage(txtchiffrer, True)
    else:
        clair = ""
        blocs = []
        for i in range(0, len(text), len(cle)):
            blocs.append(text[i:i + len(cle)])
        for i in blocs:
            bl = ""
            for j in range(len(cle)):
                bl += i[cle.index(j)]
            clair += bl
        return formatage(clair, False)


def inverse_modulo_26(a):
    inverses = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    for i in inverses:
        if (a * i) % 26 == 1:
            return i
    return -1

#Utilise une fonction mathématique (ax + b) mod 26.
def affine(text, cleA, cleB, chiffrer=True):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.replace(' ', '')
    text = text.upper()
    if chiffrer:
        txtchiffrer = ""
        for i in text:
            index_i_in_alphabet = alphabet.find(i)
            chiffrement_numerique_de_i = ((index_i_in_alphabet * cleA) + cleB) % 26
            chiffrement_alphabetique_de_i = alphabet[chiffrement_numerique_de_i]
            txtchiffrer += chiffrement_alphabetique_de_i

        return formatage(txtchiffrer, True)
    else:
        a_prim = inverse_modulo_26(cleA)
        if a_prim == -1:
            return "impossible de dechiffrer ce texte, a' introuvable"
        clair = ""
        for i in text:
            index_i_in_alphabet = alphabet.find(i)
            dechiffrement_numerique_de_i = ((index_i_in_alphabet - cleB) * a_prim) % 26
            dechiffrement_alphabetique_de_i = alphabet[dechiffrement_numerique_de_i]
            clair += dechiffrement_alphabetique_de_i
        return formatage(clair, False)


def vigenere(text, cle, chiffrer=True):
    text = text.replace(' ', '')
    text = text.upper()
    if chiffrer:
        txtchiffrer = ""
        for i in range(len(text)):
            caractere = ord(text[i]) + ord(cle[i % len(cle)]) - ord('A')
            if caractere > ord('Z'):
                caractere -= 26
            txtchiffrer += chr(caractere)
        return formatage(txtchiffrer, True)
    else:
        textclaire = ""
        for i in range(len(text)):
            caractere = ord(text[i]) - ord(cle[i % len(cle)]) + ord('A')
            if caractere < ord('A'):
                caractere += 26
            textclaire += chr(caractere)
        return formatage(textclaire, False)


def indice_coincidance(text):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    hist = [0] * 26
    for i in text:
        index_i_in_alphabet = alphabet.find(i)
        hist[index_i_in_alphabet] += 1
    n = len(text)
    n2 = n * (n - 1)
    ic = 0
    for i in hist:
        ic += (i * (i - 1)) / n2
    return ic


def longeur_de_cle(text):
    lncle = 1
    while True:
        texts = []
        for k in range(lncle):
            text2 = ""
            for i in range(k, len(text), lncle):
                text2 += text[i]
            texts.append(text2)
            ic = indice_coincidance(text2)
        if ic > 0.05:
            break
        lncle += 1
    return lncle, texts


def detecte_cle(text):
    ln, texts = longeur_de_cle(text)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cle = ""
    for i in texts:
        hist = [0] * 26
        for j in i:
            hist[alphabet.find(j)] += 1
        x = 0
        pos = 0
        for j in range(len(hist)):
            if hist[j] > x:
                x = hist[j]
                pos = j
        alpha = (pos - 4) % 26
        cle += alphabet[alpha]
    return cle


def porta_alphabet(alphabet_letter):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha1 = alphabet[:13]
    alphabet_letter = alphabet_letter.upper()
    pos = alphabet.find(alphabet_letter)
    decalage = pos // 2
    alpha2 = alphabet[13:] + alphabet[13:]
    alpha2 = alpha2[13 - decalage:26 - decalage]
    return [alpha1, alpha2]

# Utilise un alphabet divisé en deux parties avec substitution réciproque
def porta(text, cle, chiffrer=True):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.replace(' ', '')
    text = text.upper()
    text2 = ""
    for i in range(len(text)):
        c = cle[i % len(cle)]
        alpha = porta_alphabet(c)
        if alphabet.find(text[i]) > 12:
            text2 += alpha[0][alpha[1].find(text[i])]
        else:
            text2 += alpha[1][alpha[0].find(text[i])]
    return formatage(text2, chiffrer)


def porta_déchiffrement(text, key):
    key_length = len(key)
    if key_length == 0:
        raise ValueError("La clé ne peut pas être vide.")

    decrypted_text = ""
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            key_char = key[i % key_length].upper()
            key_val = ord(key_char) - ord('A')

            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            char_val = ord(char) - base
            half = key_val // (26 // 2)
            decrypted_val = (char_val - key_val + 13) % 13 + half * 13
            decrypted_char = chr(decrypted_val + base)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text


def frequency_analysis(text):
    text = text.upper()
    letters = [c for c in text if c.isalpha()]
    frequency = collections.Counter(letters)
    total = sum(frequency.values())
    if total == 0:
        return {}
    frequency = {char: count / total for char, count in frequency.items()}
    return frequency

#Chiffrement complexe combinant substitution et transposition
def horisentalADFGVX(cle):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    cle2 = cle.upper()
    cle3 = ""
    for i in cle2:
        if i in alphabet:
            cle3 += i
            alphabet = alphabet.replace(i, '')
    return cle3 + alphabet


def verticalADFGVX(cle):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    cle2 = cle.upper()
    cle3 = ""
    for i in cle2:
        if i in alphabet:
            cle3 += i
            alphabet = alphabet.replace(i, '')
    cle4 = cle3 + alphabet
    cle5 = ""
    for j in range(len(cle3)):
        for i in range(j, len(cle4), len(cle3)):
            cle5 += cle4[i]
    return cle5


def adfgvx(text, cle_sub, cle_trans, chiffrer=True):
    text = text.replace(' ', '')
    text = text.upper()
    cle_sub = cle_sub.upper()
    adf = "ADFGVX"
    adftab = ['A', 'D', 'F', 'G', 'V', 'X']
    text_inter = ""
    for i in text:
        lig = cle_sub.find(i) // len(adftab)
        col = cle_sub.find(i) % len(adftab)
        text_inter += adftab[lig]
        text_inter += adftab[col]

    for i in range(len(cle_trans) - len(text_inter) % len(cle_trans)):
        text_inter += "X"

    blocs = []
    for i in range(len(cle_trans)):
        blocs.append("")
    for i in range(len(text_inter)):
        blocs[i % len(cle_trans)] += text_inter[i]

    blocs2 = []
    for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        while i in cle_trans:
            pos = cle_trans.find(i)
            blocs2.append(blocs[pos])
            cle_trans2 = ""
            for h in range(len(cle_trans)):
                if h != pos:
                    cle_trans2 += cle_trans[h]
                else:
                    cle_trans2 += 'm'
            cle_trans = cle_trans2
    chiff = ""
    for i in blocs2:
        chiff += i
    return chiff

def dechiffrement_adfgvx(texte_chiffre, cle_sub, cle_trans):
    texte_chiffre = texte_chiffre.replace(" ", "").upper()
    cle_sub = cle_sub.upper()
    adf = "ADFGVX"
    n = len(texte_chiffre)
    nb_col = len(cle_trans)
    nb_lig = n // nb_col


    ordre = sorted([(lettre, i) for i, lettre in enumerate(cle_trans)])
    colonnes_vides = [''] * nb_col
    index = 0

    for lettre, i in ordre:
        colonnes_vides[i] = texte_chiffre[index:index + nb_lig]
        index += nb_lig


    texte_inter = ''
    for i in range(nb_lig):
        for col in colonnes_vides:
            texte_inter += col[i]

    
    texte_final = ''
    for i in range(0, len(texte_inter), 2):
        a = texte_inter[i]
        b = texte_inter[i + 1]
        ligne = adf.index(a)
        colonne = adf.index(b)
        index_sub = ligne * 6 + colonne
        if index_sub < len(cle_sub):
            texte_final += cle_sub[index_sub]
        else:
            texte_final += '?'

    return texte_final

# Cryptographie Moderne RSA
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generer_cles_rsa(bits=1024):
    # Génération de deux nombres premiers p et q
    p = randprime(2 ** (bits // 2), 2 ** (bits // 2 + 1))
    q = randprime(2 ** (bits // 2), 2 ** (bits // 2 + 1))
    while q == p:
        q = randprime(2 ** (bits // 2), 2 ** (bits // 2 + 1))

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choix de e premier avec phi
    e = 65537
    while pgcd(e, phi) != 1:
        e += 2

    # Calcul de d, l'inverse de e modulo phi
    d = pow(e, -1, phi)

    return ((n, e), (n, d))


def chiffrer_rsa(texte, cle_publique):
    n, e = cle_publique
    texte_chiffre = []
    for char in texte:
        m = ord(char)
        c = pow(m, e, n)
        texte_chiffre.append(str(c))
    return ' '.join(texte_chiffre)


def dechiffrer_rsa(texte_chiffre, cle_privee):
    n, d = cle_privee
    nombres = texte_chiffre.split()
    texte_clair = []
    for nombre in nombres:
        c = int(nombre)
        m = pow(c, d, n)
        texte_clair.append(chr(m))
    return ''.join(texte_clair)


# Interface graphique
class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Chiffrement Avancée de Mayssa BR")
        self.root.geometry("900x700")

        # Style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 9))
        self.style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))

        # Variables
        self.method_var = tk.StringVar()
        self.key1_var = tk.StringVar()
        self.key2_var = tk.StringVar()
        self.key3_var = tk.StringVar()
        self.rsa_keys = None

        # Création des onglets
        self.notebook = ttk.Notebook(root)

        # Onglet 1: Méthodes simples
        self.simple_frame = ttk.Frame(self.notebook)
        self.create_simple_widgets()

        # Onglet 2: RSA
        self.rsa_frame = ttk.Frame(self.notebook)
        self.create_rsa_widgets()

        # Onglet 3: Analyse fréquentielle
        self.analysis_frame = ttk.Frame(self.notebook)
        self.create_analysis_widgets()

        # Ajout des onglets
        self.notebook.add(self.simple_frame, text="Méthodes Simples")
        self.notebook.add(self.rsa_frame, text="RSA")
        self.notebook.add(self.analysis_frame, text="Analyse Fréquentielle")
        self.notebook.pack(expand=1, fill="both", padx=5, pady=5)

    def create_simple_widgets(self):
        # Titre
        ttk.Label(self.simple_frame, text="Méthodes Classiques de Chiffrement", style='Title.TLabel') \
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Sélection de méthode
        ttk.Label(self.simple_frame, text="Méthode:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        methods = ["César", "Alphabet Désordonné", "Transposition", "Affine", "Vigenère", "Porta", "ADFGVX"]
        method_menu = ttk.Combobox(self.simple_frame, textvariable=self.method_var, values=methods, state="readonly")
        method_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        method_menu.current(0)

        # Zone de texte
        input_frame = ttk.LabelFrame(self.simple_frame, text="Texte d'entrée")
        input_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.input_text = scrolledtext.ScrolledText(input_frame, height=10, width=50, wrap=tk.WORD)
        self.input_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Clés
        key_frame = ttk.Frame(self.simple_frame)
        key_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Label(key_frame, text="Clé 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(key_frame, textvariable=self.key1_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(key_frame, text="Clé 2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(key_frame, textvariable=self.key2_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(key_frame, text="Clé 3:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(key_frame, textvariable=self.key3_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Boutons
        btn_frame = ttk.Frame(self.simple_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(btn_frame, text="Chiffrer", command=self.encrypt).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Déchiffrer", command=self.decrypt).grid(row=0, column=1, padx=5, pady=5)

        # Résultat
        output_frame = ttk.LabelFrame(self.simple_frame, text="Résultat")
        output_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, width=50, wrap=tk.WORD)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Configuration du redimensionnement
        self.simple_frame.grid_columnconfigure(1, weight=1)
        self.simple_frame.grid_rowconfigure(2, weight=1)
        self.simple_frame.grid_rowconfigure(5, weight=1)

    def create_rsa_widgets(self):
        # Titre
        ttk.Label(self.rsa_frame, text="Chiffrement RSA", style='Title.TLabel') \
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Zone de texte
        input_frame = ttk.LabelFrame(self.rsa_frame, text="Texte d'entrée")
        input_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.rsa_input_text = scrolledtext.ScrolledText(input_frame, height=8, width=50, wrap=tk.WORD)
        self.rsa_input_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Boutons RSA
        btn_frame = ttk.Frame(self.rsa_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(btn_frame, text="Générer clés RSA", command=self.generate_rsa_keys).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Chiffrer", command=self.rsa_encrypt).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Déchiffrer", command=self.rsa_decrypt).grid(row=0, column=2, padx=5)

        # Affichage des clés
        key_frame = ttk.LabelFrame(self.rsa_frame, text="Clés RSA")
        key_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        ttk.Label(key_frame, text="Clé publique (n, e):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.rsa_pub_key_label = ttk.Label(key_frame, text="Non générée", foreground="blue")
        self.rsa_pub_key_label.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(key_frame, text="Clé privée (n, d):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.rsa_priv_key_label = ttk.Label(key_frame, text="Non générée", foreground="red")
        self.rsa_priv_key_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Résultat
        output_frame = ttk.LabelFrame(self.rsa_frame, text="Résultat")
        output_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.rsa_output_text = scrolledtext.ScrolledText(output_frame, height=8, width=50, wrap=tk.WORD)
        self.rsa_output_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Configuration du redimensionnement
        self.rsa_frame.grid_columnconfigure(1, weight=1)
        self.rsa_frame.grid_rowconfigure(1, weight=1)
        self.rsa_frame.grid_rowconfigure(4, weight=1)

    def create_analysis_widgets(self):
        # Titre
        ttk.Label(self.analysis_frame, text="Analyse Fréquentielle", style='Title.TLabel') \
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Zone de texte
        input_frame = ttk.LabelFrame(self.analysis_frame, text="Texte à analyser")
        input_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.analysis_input_text = scrolledtext.ScrolledText(input_frame, height=10, width=50, wrap=tk.WORD)
        self.analysis_input_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Boutons d'analyse
        btn_frame = ttk.Frame(self.analysis_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(btn_frame, text="Analyse de Fréquence", command=self.do_frequency_analysis).grid(row=0, column=0,
                                                                                                    padx=5)
        ttk.Button(btn_frame, text="Indice de Coïncidence", command=self.do_coincidence_index).grid(row=0, column=1,
                                                                                                    padx=5)

        # Résultats d'analyse
        self.analysis_result_frame = ttk.LabelFrame(self.analysis_frame, text="Résultats d'analyse")
        self.analysis_result_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.analysis_result_text = scrolledtext.ScrolledText(
            self.analysis_result_frame, height=10, width=50, wrap=tk.WORD)
        self.analysis_result_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Configuration du redimensionnement
        self.analysis_frame.grid_columnconfigure(1, weight=1)
        self.analysis_frame.grid_rowconfigure(1, weight=1)
        self.analysis_frame.grid_rowconfigure(3, weight=1)

    def encrypt(self):
        method = self.method_var.get()
        text = self.input_text.get("1.0", tk.END).strip()
        key1 = self.key1_var.get()
        key2 = self.key2_var.get()
        key3 = self.key3_var.get()

        try:
            if method == "César":
                if not key1.isdigit():
                    raise ValueError("Le décalage doit être un nombre entier")
                result = cesar(text, int(key1), True)
            elif method == "Alphabet Désordonné":
                cle = horisental(key1) if key2 == "H" else vertical(key1)
                result = alphabet_desordonne(text, cle, True)
            elif method == "Transposition":
                cle = cle_transposition(key1)
                result = transposition(text, cle, True)
            elif method == "Affine":
                if not key1.isdigit() or not key2.isdigit():
                    raise ValueError("Les clés A et B doivent être des nombres entiers")
                result = affine(text, int(key1), int(key2), True)
            elif method == "Vigenère":
                result = vigenere(text, key1, True)
            elif method == "Porta":
                result = porta(text, key1, True)
            elif method == "ADFGVX":
                result = adfgvx(text, key1, key2)
            else:
                result = "Méthode non reconnue"

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def decrypt(self):
        method = self.method_var.get()
        text = self.input_text.get("1.0", tk.END).strip()
        key1 = self.key1_var.get()
        key2 = self.key2_var.get()
        key3 = self.key3_var.get()
        try:
            if method == "César":
                if not key1.isdigit():
                    raise ValueError("Le décalage doit être un nombre entier")
                result = cesar(text, int(key1), False)
            elif method == "Alphabet Désordonné":
                cle = horisental(key1) if key2 == "H" else vertical(key1)
                result = alphabet_desordonne(text, cle, False)
            elif method == "Transposition":
                cle = cle_transposition(key1)
                result = transposition(text, cle, False)
            elif method == "Affine":
                if not key1.isdigit() or not key2.isdigit():
                    raise ValueError("Les clés A et B doivent être des nombres entiers")
                result = affine(text, int(key1), int(key2), False)
            elif method == "Vigenère":
                result = vigenere(text, key1, False)
            elif method == "Porta":
                result = porta_déchiffrement(text, key1)
            elif method == "ADFGVX":
                result = dechiffrement_adfgvx(text, key1, key2)
            else:
                result = "Méthode non reconnue"
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    def generate_rsa_keys(self):
        self.rsa_keys = generer_cles_rsa(64)  # 64 bits pour des clés plus courtes (démonstration)
        self.rsa_pub_key_label.config(text=str(self.rsa_keys[0]))
        self.rsa_priv_key_label.config(text=str(self.rsa_keys[1]))
        messagebox.showinfo("Succès", "Clés RSA générées avec succès!")

    def rsa_encrypt(self):
        if not self.rsa_keys:
            messagebox.showerror("Erreur", "Veuillez d'abord générer des clés RSA")
            return

        text = self.rsa_input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Erreur", "Veuillez entrer un texte à chiffrer")
            return

        try:
            result = chiffrer_rsa(text, self.rsa_keys[0])
            self.rsa_output_text.delete("1.0", tk.END)
            self.rsa_output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def rsa_decrypt(self):
        if not self.rsa_keys:
            messagebox.showerror("Erreur", "Veuillez d'abord générer des clés RSA")
            return

        text = self.rsa_input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Erreur", "Veuillez entrer un texte à déchiffrer")
            return

        try:
            result = dechiffrer_rsa(text, self.rsa_keys[1])
            self.rsa_output_text.delete("1.0", tk.END)
            self.rsa_output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def do_frequency_analysis(self):
        text = self.analysis_input_text.get("1.0", tk.END).strip().upper()
        if not text:
            messagebox.showerror("Erreur", "Veuillez entrer un texte à analyser")
            return

        freq = frequency_analysis(text)
        if not freq:
            self.analysis_result_text.delete("1.0", tk.END)
            self.analysis_result_text.insert("1.0", "Aucune lettre à analyser")
            return

        # Trier par fréquence décroissante
        sorted_freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)

        # Afficher les résultats
        result = "Analyse de fréquence:\n\n"
        result += "Lettre | Fréquence\n"
        result += "----------------\n"
        for char, frequency in sorted_freq:
            result += f"   {char}   | {frequency:.4f}\n"

        self.analysis_result_text.delete("1.0", tk.END)
        self.analysis_result_text.insert("1.0", result)
    #Mesure la probabilité que deux lettres tirées au hasard soient identiques
    def do_coincidence_index(self):
        text = self.analysis_input_text.get("1.0", tk.END).strip().upper()
        if not text:
            messagebox.showerror("Erreur", "Veuillez entrer un texte à analyser")
            return

        ic = indice_coincidance(text)
        result = f"Indice de coïncidence: {ic:.4f}\n\n"

        # Interprétation
        if ic > 0.075:
            result += "Probablement un texte en langue naturelle (français/anglais)"
        elif 0.06 < ic <= 0.075:
            result += "Possiblement un texte chiffré avec substitution monoalphabétique"
        elif 0.04 < ic <= 0.06:
            result += "Possiblement un texte chiffré avec substitution polyalphabétique"
        else:
            result += "Texte probablement aléatoire ou très court"

        self.analysis_result_text.delete("1.0", tk.END)
        self.analysis_result_text.insert("1.0", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
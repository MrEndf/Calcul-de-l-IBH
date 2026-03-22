import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog

# ---------------- GUI SETUP ----------------
ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("Calcul de IBH")
root.geometry("420x320")
root.resizable(False, False)

df = None

# ---------------- CONFIG IBH ----------------
config = {
    'revenu': {'min': 45000, 'max': 500000, 'poids': 0.11},
    'eau': {'min': 20, 'max': 300, 'poids': 0.10},
    'electricite': {'min': 4, 'max': 24, 'poids': 0.11},
    'internet': {'min': 0.5, 'max': 20, 'poids': 0.07},

    'sante': {'min': 10, 'max': 100, 'poids': 0.10},
    'distance_hopitaux': {'min': 1, 'max': 20, 'poids': 0.08},  # corrigé logique
    'qualite_sys_medical': {'min': 0, 'max': 100, 'poids': 0.04},

    'securite': {'min': 20, 'max': 100, 'poids': 0.10},
    'routes': {'min': 0, 'max': 100, 'poids': 0.07},
    'qualite_routes': {'min': 0, 'max': 100, 'poids': 0.03},
    'transport': {'min': 10, 'max': 100, 'poids': 0.05},
    'dechets': {'min': 0, 'max': 100, 'poids': 0.05},

    'education': {'min': 30, 'max': 100, 'poids': 0.05},
    'loisir': {'min': 0, 'max': 100, 'poids': 0.02},
    'nourriture': {'min': 40, 'max': 100, 'poids': 0.02}
}

# ---------------- LABELS ----------------
title = ctk.CTkLabel(root, text="Calcul de l'IBH", font=("Arial", 16))
title.pack(pady=10)

status_label = ctk.CTkLabel(root, text="Aucun fichier chargé")
status_label.pack(pady=5)

result_label = ctk.CTkLabel(root, text="")
result_label.pack(pady=5)

# ---------------- LOAD FILE ----------------
def load_file():
    global df

    file_path = filedialog.askopenfilename(
        title="Choisir le fichier CSV",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    df = pd.read_csv(file_path)
    status_label.configure(text="Fichier chargé ✔")
    print(df.head())


# ---------------- CALCUL IBH ----------------
def calculate_ibh():
    global df

    if df is None:
        status_label.configure(text="❌ Aucun fichier chargé")
        return

    for col, param in config.items():
        df[f'score_{col}'] = (
            (df[col] - param['min']) / (param['max'] - param['min'])
        ).clip(0, 1)

    df['IBH'] = sum(
        df[f'score_{col}'] * param['poids']
        for col, param in config.items()
    ) * 100

    result_label.configure(text=f"IBH calculé ✔ (moyenne: {df['IBH'].mean():.2f})")
    print(df[['IBH']].head())


# ---------------- GRAPH ----------------
def show_graph():
    if df is None or 'IBH' not in df.columns:
        status_label.configure(text="❌ IBH non calculé")
        return

    n, bins, _ = plt.hist(df['IBH'], bins=10, range=(0, 100), edgecolor='black')

    for i in range(len(n)):
        print(f"Tranche {bins[i]:.0f}-{bins[i+1]:.0f}% : {int(n[i])} familles")

    plt.xlabel("IBH (%)")
    plt.ylabel("Nombre de familles")
    plt.title("Distribution IBH")
    plt.show()


# ---------------- BUTTONS ----------------
btn_load = ctk.CTkButton(root, text="Charger CSV", command=load_file)
btn_load.pack(pady=8)

btn_calc = ctk.CTkButton(root, text="Calculer IBH", command=calculate_ibh)
btn_calc.pack(pady=8)

btn_graph = ctk.CTkButton(root, text="Afficher graphique", command=show_graph)
btn_graph.pack(pady=8)


root.mainloop()

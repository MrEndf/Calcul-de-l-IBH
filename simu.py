import matplotlib.pyplot as plt
import numpy as np, pandas as pd

df = pd.read_csv(r"C:\Users\PRIME\Desktop\dev\immc 26\code\data.csv")
print(df)


config = {
    # SERVICES DE BASE (Échelle : Valeurs physiques)
    'revenu':              {'min': 45000, 'max': 500000, 'poids': 0.11}, # FCFA (SMIC à Max)
    'eau':                 {'min': 20,    'max': 300,    'poids': 0.10}, # Litres / jour / personne
    'electricite':         {'min': 4,     'max': 24,     'poids': 0.11}, # Heures / jour
    'internet':            {'min': 0.5,   'max': 20,     'poids': 0.07}, # Mbps (Débit)

    # SANTÉ & INFRASTRUCTURE (Échelle : Distance et Qualité)
    'sante':               {'min': 10,    'max': 100,    'poids': 0.10}, # Score d'accès global
    'distance_hopitaux':   {'min': 20,    'max': 1,      'poids': 0.08}, # Inverse : 20km = 0, 1km = 1
    'qualite_sys_medical': {'min': 0,     'max': 100,    'poids': 0.04}, # Score qualitatif

    # CADRE DE VIE (Échelle : Perception/Qualité sur 100)
    'securite':            {'min': 20,    'max': 100,    'poids': 0.10},
    'routes':              {'min': 0,     'max': 100,    'poids': 0.07},
    'qualite_routes':      {'min': 0,     'max': 100,    'poids': 0.03},
    'transport':           {'min': 10,    'max': 100,    'poids': 0.05},
    'dechets':             {'min': 0,     'max': 100,    'poids': 0.05},

    # ÉPANOUISSEMENT (Échelle : Perception sur 100)
    'education':           {'min': 30,    'max': 100,    'poids': 0.05},
    'loisir':              {'min': 0,     'max': 100,    'poids': 0.02},
    'nourriture':          {'min': 40,    'max': 100,    'poids': 0.02}
}

# Calcul des scores pour chaque colonne
for col, param in config.items():
    # 1. On soustrait le minimum et on divise par la plage (max-min)
    df[f'score_{col}'] = (df[col] - param['min']) / (param['max'] - param['min'])
    
    # 2. On clip : tout ce qui est < 0 devient 0, tout ce qui est > 1 devient 1
    df[f'score_{col}'] = df[f'score_{col}'].clip(0, 1)

# Calcul de l'indice final (Somme pondérée)
df['IBH'] = sum(df[f'score_{col}'] * param['poids'] for col, param in config.items()) * 100

ibh_s = np.array(df['IBH'])

n, bins, _ = plt.hist(df['IBH'], bins=10, range=(0, 100), edgecolor='black')
for i in range(len(n)):
    print(f"Tranche {bins[i]:.0f}-{bins[i+1]:.0f}% : {int(n[i])} familles")

plt.xlabel("IBH (%)")
plt.ylabel("Nombre de familles")
plt.show()

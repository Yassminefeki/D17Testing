# lancer_plusieurs_tests.py
import subprocess
import time

comptes = []
with open("comptes.csv", encoding="utf-8") as f:
    next(f)  # skip header
    for line in f:
        user, pwd = line.strip().split(",")
        comptes.append((user, pwd))

print(f"Lancement de {len(comptes)} tests en parallèle...")

processes = []
for username, password in comptes[:100]:  # max 100 en même temps = safe
    cmd = f'python d17_rush_hour.py "{username}" "{password}"'
    p = subprocess.Popen(cmd, shell=True)
    processes.append(p)
    time.sleep(1)  # 1 seconde entre chaque lancement

print("Tous les tests lancés. Attente de fin...")
for p in processes:
    p.wait()

print("TOUS LES TESTS TERMINÉS !")
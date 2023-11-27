# mapping.py
import pandas as pd
import json
import subprocess
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Pfad zur Ihrer Excel-Datei
excel_path = '_Kommunenerhebung - 2020 - gesamt.xlsx'

# Pfad zur JSON-Datei
json_path = 'url_to_name_mapping.json'

# Excel-Datei laden
df = pd.read_excel(excel_path)

# Mapping Dictionary erstellen
url_to_name_mapping = {}

# Spalten überprüfen und Mapping erstellen
if 'A_Webadr' in df.columns and 'A_Kom' in df.columns:
    for index, row in df.iterrows():
        url = row['A_Webadr'] if pd.notna(row['A_Webadr']) else ''
        name = row['A_Kom']
        url_to_name_mapping[url] = name

# Mapping in JSON-Datei schreiben
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(url_to_name_mapping, json_file)

print(f"Mapping wurde in {json_path} gespeichert.")



# Pfad zur Ihrer Excel-Datei
excel_path = '_Kommunenerhebung - 2020 - gesamt.xlsx'

# Excel-Datei laden
df = pd.read_excel(excel_path)

# Überprüfen Sie sicherheitshalber, ob die Spalte 'A_Webadr' existiert
if 'A_Webadr' in df.columns:
    for url in df['A_Webadr']:
        # Befehl zusammensetzen
        command = [
                    'docker', 'run', '--rm',
                    '-v', f"{os.getcwd()}:/sitespeed.io",
                    'sitespeedio/sitespeed.io',
                    url, '-b', 'firefox',
                    '--visualMetrics', 'false', '--video', 'false'
                ]
        # Befehl ausführen
        process = subprocess.run(command, shell=True)
        print(f"SiteSpeed.io Analyse für {url} wurde ausgeführt.")
else:
    print("Die Spalte 'A_Webadr' wurde nicht in der Excel-Datei gefunden.")



# Pfad zum Hauptordner
main_dir = 'sitespeed-result'

# Mapping aus JSON-Datei laden
with open('url_to_name_mapping.json', 'r', encoding='utf-8') as json_file:
    mapping = json.load(json_file)

# Dictionary für gesammelte Daten
collected_data = []

# Domain-Name aus URL extrahieren und Mapping anpassen
domain_to_name = {urlparse(url).netloc: name for url, name in mapping.items()}

# Durch jeden Domain-Ordner iterieren
for domain in os.listdir(main_dir):
    domain_path = os.path.join(main_dir, domain)
    if os.path.isdir(domain_path):
        # Neuesten Unterordner finden
        latest_subfolder = max([os.path.join(domain_path, d) for d in os.listdir(domain_path)], key=os.path.getmtime)
        html_file = os.path.join(latest_subfolder, 'index.html')

        # HTML-Datei einlesen und analysieren
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                extracted_data = {}
                for summary in soup.find_all('div', class_='summarybox'):
                    title = summary.contents[0].strip()
                    number_div = summary.find('div', class_='summarynumber')
                    number = number_div.contents[0].strip() if number_div.contents else 'N/A'
                    formatted_title = 'sitespeed_' + '_'.join(title.split())
                    extracted_data[formatted_title] = number

                # Name aus Mapping hinzufügen
                name = domain_to_name.get(domain, 'Unbekannt')
                extracted_data['Name'] = name
                collected_data.append(extracted_data)

# Ergebnisse in eine Excel-Tabelle schreiben
df = pd.DataFrame(collected_data)
df.to_excel('gesammelte_daten.xlsx', index=False)
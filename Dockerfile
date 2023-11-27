# Verwenden des offiziellen Python-Images als Basis
FROM python:3.8-slim

# Arbeitsverzeichnis im Container festlegen
WORKDIR /usr/src/app

# Abhängigkeiten installieren
# Hinweis: pandas und openpyxl (für das Lesen von Excel-Dateien) müssen installiert sein
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie Ihre Skripte und die Excel-Datei in das Container-Verzeichnis
COPY . .

# Ausführung der Skripte beim Start des Containers
CMD ["python", "./mapping.py"]
import os

# Umgebungsvariable PATH auslesen und ausgeben
path = os.environ.get("PATH")

if path:
    print("PATH:", path)
else:
    print("Umgebungsvariable PATH nicht gefunden.")

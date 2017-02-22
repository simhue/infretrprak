# infretrprak
Projekt für die Veranstaltung Fortgeschrittene Methoden des Information Retrieval http://asv.informatik.uni-leipzig.de/de/courses/215

Das Projekt beinhaltet die Entwicklung eines Programms, welches die semantische Ähnlichkeit aus einer Menge von Sätzen vergleicht.

# Anleitung

Damit das Skript reibungslos laufen kann, muss ein Linuxbetriebssystem mit einem installiertem
Python-2.7-Paket vorhanden sein. Die Dateien `run.sh` und `main.py` gemeinsam in einen beliebigen
Ordner (z.B. das Home-Verzeichnis des aktuellen Benutzers) ablegen. Für den Export der inversen
Liste werden Zugangsdaten für die MySQL-Zieldatenbank benötigt. Mit einem Texteditor `main.py`
öffnen und in die Zeilen
```python
# DB connection information
# DB host
host = ’localhost’
# DB user
user = ’dbuser’
# DB password
passwd = ’password’
# Name of used DB
dbName = ’deu_mixed_2011’
```
die Daten der benutzten Datenbankverbindung eintragen. Optional können die Konfigurationsvaria-
blen verändert werden.

__wordIdBoundary__ Jede Wort-ID, die kleiner oder gleich diesem Wert ist, wird ignoriert. Die Höhe wirkt
wirkt sich auf die Endqualität und auf die Gesamtlaufzeit aus. Je höher dieser Wert ist, um
so mehr potentielle Kandidaten werden ignoriert, aber die Laufzeit wird verringert.

__countOfWords__ Die Anzahl der seltensten Wort-IDs pro Satz, die zum Vergleich benutzt werden. Die
Sätze, die weniger Wörter besitzen als dieser Wert, werden ignoriert. Je höher dieser Wert
ist, um so größer ist die Qualität der Ergebnisse, aber die Gesamtlaufzeit erhöht sich, da die
Anzahl der Vergleiche steigt.

__countOfSentences__ Die Anzahl der Sätze, die verarbeitet werden sollen. -1 zeigt an, dass alle Sätze
in der Exportdatei verarbeitet werden.

Die Datei speichern und den Editor schließen. Ein Terminal öffnen und zum Verzeichnis navigieren in
dem `run.sh` liegt. Das Skript wird mit dem Kommando `./run.sh` gestartet.
Nachdem das Skript erfolgreich beendet ist, liegen in dem selben Verzeichnis drei neue Textdateien.
Die Exportdatei (benannt nach dem Namen der Datenbank) beinhaltet alle Satz-ID/Wort-ID-Paare
aus der inversen Liste. Wenn ein neuer Export erstellt werden soll, muss diese Datei gelöscht werden.
In der Datei `sorted-counted-pairs` liegen aufsteigend sortiert die gezählten Satzpaare im Format:
```
  AnzahlGemeinsamerWoerter Satz-ID1 Satz-ID2
```
In der Datei `sentences.txt` sind die Satzpaare als Klartext zur Auswertung aufgelistet.

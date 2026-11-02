import csv

FILE = "dati/netflix-film-2023-2025.csv"


def converti_durata(testo_durata):

  if not testo_durata or testo_durata == "NA":
    return 0

  ore = 0
  minuti = 0
  parti = testo_durata.split()

  for p in parti:
    if p.endswith("H"):
      ore = int(p.rstrip("H"))
    elif p.endswith("M"):
      minuti = int(p.rstrip("M"))

  return (ore * 60) + minuti

def carica(nomefile):
  dati = []
  scartate = 0

  with open(nomefile, "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    
    for riga in reader:
      if (riga["runtime"] == "NA" or riga["views"] == "NA" or riga["hours_viewed"] == "NA"):
        scartate += 1
        continue
      
      riga["runtime_minuti"] = converti_durata(riga["runtime"])
      riga["hours_viewed"] = float(riga["hours_viewed"])
      riga["views"] = float(riga["views"])

      dati.append(riga)

  return dati, scartate
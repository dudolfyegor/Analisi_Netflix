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

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

def domanda1(dati):
  righe_per_report = {}
  film_per_report = {}

  for riga in dati:
    rep = riga["report"]
    titolo = riga["title"]

    righe_per_report[rep] = righe_per_report.get(rep, 0) + 1

    if titolo not in film_per_report:
      film_per_report[titolo] = set()
    film_per_report[titolo].add(rep)

  film_unici = set(film_per_report.keys())

  film_sempre_presenti = [
      t for t, semestri in film_per_report.items() if len(semestri) == 4
  ]

  return {
      "righe_per_report": righe_per_report,
      "totale_film_unici": len(film_unici),
      "film_in_tutti_i_report": len(film_sempre_presenti),
  }

def domanda2(dati):
  subset = [r for r in dati if r["report"] == "2025Jan-Jun"]

  if not subset:
    return "Nessun dato trovato per questo report."

  durate = [r["runtime_minuti"] for r in subset]

  minimo = min(durate)
  massimo = max(durate)
  media = round(sum(durate) / len(durate), 2)

  film_lungo = ""
  for r in subset:
    if r["runtime_minuti"] == massimo:
      film_lungo = r["title"]
      break

  return {
      "min_minuti": minimo,
      "max_minuti": massimo,
      "media_minuti": media,
      "film_piu_lungo": film_lungo,
  }
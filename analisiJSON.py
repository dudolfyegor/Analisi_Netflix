import csv
import json
from pathlib import Path

FILE = Path("netflix-film-2023-2025.json")


def converti_durata(testo_durata):
    if not testo_durata or str(testo_durata).strip().upper() in {"NA", "N/A", ""}:
        return 0

    ore = 0
    minuti = 0
    for parte in str(testo_durata).strip().upper().split():
        if parte.endswith("H") and parte[:-1].isdigit():
            ore = int(parte[:-1])
        elif parte.endswith("M") and parte[:-1].isdigit():
            minuti = int(parte[:-1])

    return (ore * 60) + minuti


def carica(nomefile):
    dati = []
    scartate = 0

    with open(nomefile, "r", encoding="utf-8") as f:
        contenuto = json.load(f)

    if not isinstance(contenuto, list):
        raise ValueError("Il file JSON deve contenere una lista di oggetti.")

    for riga in contenuto:
        if not isinstance(riga, dict):
            scartate += 1
            continue

        runtime = riga.get("runtime")
        views = riga.get("views")
        hours_viewed = riga.get("hours_viewed")

        if runtime in (None, "", "NA") or views in (None, "", "NA") or hours_viewed in (None, "", "NA"):
            scartate += 1
            continue

        try:
            hours_val = float(hours_viewed)
            views_val = float(views)
        except (ValueError, TypeError):
            scartate += 1
            continue

        record = dict(riga)
        record["runtime_minuti"] = converti_durata(runtime)
        record["hours_viewed"] = hours_val
        record["views"] = views_val
        dati.append(record)

    return dati, scartate


def domanda1(dati):
    righe_per_report = {}
    film_per_report = {}

    for riga in dati:
        rep = riga.get("report", "Sconosciuto")
        titolo = riga.get("title", "")

        righe_per_report[rep] = righe_per_report.get(rep, 0) + 1
        film_per_report.setdefault(titolo, set()).add(rep)

    numero_report = len(righe_per_report)
    film_sempre_presenti = [
        titolo
        for titolo, semestri in film_per_report.items()
        if numero_report > 0 and len(semestri) == numero_report
    ]

    return {
        "righe_per_report": righe_per_report,
        "totale_film_unici": len(film_per_report),
        "numero_report_considerati": numero_report,
        "film_in_tutti_i_report": len(film_sempre_presenti),
    }


def domanda2(dati, report_target="2025Jan-Jun"):
    subset = [r for r in dati if r.get("report") == report_target]
    if not subset:
        return f"Nessun dato trovato per il report '{report_target}'."

    durate = [r["runtime_minuti"] for r in subset]
    minimo = min(durate)
    massimo = max(durate)
    media = round(sum(durate) / len(durate), 2)

    film_lungo = next(
        (r.get("title", "") for r in subset if r["runtime_minuti"] == massimo),
        "",
    )

    return {
        "min_minuti": minimo,
        "max_minuti": massimo,
        "media_minuti": media,
        "film_piu_lungo": film_lungo,
    }


def domanda3(dati, report_target="2025Jan-Jun"):
    views_per_report = {}
    max_views_per_report = {}

    for riga in dati:
        rep = riga.get("report", "Sconosciuto")
        v = riga["views"]
        titolo = riga.get("title", "")

        views_per_report[rep] = views_per_report.get(rep, 0.0) + v
        if rep not in max_views_per_report or v > max_views_per_report[rep]["views"]:
            max_views_per_report[rep] = {"title": titolo, "views": v}

    subset_2025 = [r for r in dati if r.get("report") == report_target]
    top_10 = sorted(subset_2025, key=lambda x: x["views"], reverse=True)[:10]

    return {
        "views_per_report": views_per_report,
        "piu_visto_per_report": max_views_per_report,
        "top_10_2025": top_10,
    }


def scrivi_risultati(dati_d3, output_path="risultati.csv"):
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Report", "Film Piu Visto", "Visualizzazioni Totali"])
        for rep, views in dati_d3["views_per_report"].items():
            film_top = dati_d3["piu_visto_per_report"][rep]["title"]
            writer.writerow([rep, film_top, views])


def domanda_engagement(dati, top_n=5):
    film_engagement = []

    for riga in dati:
        views = riga["views"]
        if views > 0:
            ore_per_view = riga["hours_viewed"] / views
            film_engagement.append(
                {
                    "title": riga.get("title", ""),
                    "report": riga.get("report", ""),
                    "ore_medie_per_view": round(ore_per_view, 2),
                }
            )

    film_engagement.sort(key=lambda x: x["ore_medie_per_view"], reverse=True)
    return film_engagement[:top_n]


if __name__ == "__main__":
    dati, scartate = carica(FILE)
    print(f"Righe caricate: {len(dati)} | Scartate: {scartate}")

    ris_d1 = domanda1(dati)
    ris_d2 = domanda2(dati)
    ris_d3 = domanda3(dati)
    ris_eng = domanda_engagement(dati)

    scrivi_risultati(ris_d3)
    print("Domanda 1:", ris_d1)
    print("Domanda 2:", ris_d2)
    print("Top 10 2025Jan-Jun:", [r.get("title") for r in ris_d3["top_10_2025"]])
    print("Top 5 engagement:", ris_eng)
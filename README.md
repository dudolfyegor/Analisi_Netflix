# Analisi dati Netflix 2023-2025
Questo è il nostro progetto di informatica dove abbiamo analizzato i file dei dati di Netflix (dal 2023 al 2025). L'obiettivo era pulire i dati, fare un po' di calcoli sulle visualizzazioni e sulle durate dei film, e salvare i risultati principali. Abbiamo fatto tutto lavorando in gruppo con Git e i branch per non incasinarci il codice.
## Chi ha fatto cosa
Abbiamo diviso il lavoro usando i branch su Git (feature/carica-e-domande e feature/domanda3-e-risultati) e poi abbiamo unito tutto sul main con le Pull Request.
* Lucia Enrico: si è occupato di caricare il file CSV, ignorare i dati sbagliati e fare i calcoli delle prime due domande (conteggi sui semestri e durate dei film del 2025).
* Dolud Yegor: ha fatto la parte della domanda 3 (visualizzazioni totali e top 10), la scrittura del file CSV di output e la domanda extra sull'engagement.
## Come abbiamo pulito i dati
Prima di fare qualsiasi calcolo, la funzione carica() legge il file dati/netflix-film-2023-2025.csv e fa un po' di pulizia:
* Legge il file in UTF-8 per non avere problemi con i caratteri speciali.
Punto elenco Salta le righe con i valori "NA" nelle colonne della durata, delle views o delle ore viste. In totale abbiamo scartato 12 righe perche non erano valide.
* Converte la durata da testo (tipo "1H 30M") in un numero intero di minuti, cosi possiamo farci le medie e i confronti facilmente.
## Cosa fa lo script e i risultati
Il programma analisi.py calcola queste cose in ordine:
1. Domanda 1: conta quante righe ci sono per ogni semestre, quanti film unici ci sono in tutto il file e trova quali film sono rimasti in classifica in tutti e 4 i report semestrali.
2. Domanda 2: prende solo i dati del primo semestre 2025 (2025Jan-Jun) e trova il film piu corto, quello piu lungo, e fa la media della durata in minuti di tutti i film.
3. Domanda 3: somma tutte le visualizzazioni per ogni report, trova il film piu visto di ogni semestre e prende i primi 10 film piu visti del 2025.
4. Esportazione CSV: prende i dati della Domanda 3 e li salva automaticamente in un nuovo file chiamato risultati.csv.
5. Domanda Extra (Engagement): calcola quante ore di visione fa in media un film per ogni singola visualizzazione. 

F1 Data Analytics Pipeline
Descrizione del Progetto
Questo progetto nasce con l'obiettivo di creare un sistema integrato per l'estrazione e l'analisi dei dati della Formula 1. Il sistema utilizza Python come strumento di acquisizione e processamento dei dati (Data Ingestion) e il C++ come motore di calcolo per l'analisi statistica e prestazionale.


Architettura del Sistema
1. Modulo di Estrazione (Python)
Il modulo Python gestisce l'interazione con l'utente e il recupero dei dati dai server tramite la libreria fastf1.


Data Extractor: Una classe dedicata si occupa di caricare i dati della sessione, gestire la cache e convertire i formati temporali complessi (timedelta) in formati numerici semplici (secondi) compatibili con il C++.

Storage: I dati vengono esportati in file CSV organizzati in una struttura di cartelle gerarchica: dati_csv/anno/gara/sessione/.

2. Modulo di Analisi (C++)
Il modulo C++ rappresenta il nucleo computazionale del progetto.

Parser CSV: Funzioni dedicate alla lettura dei file generati da Python e alla mappatura dei dati in strutture (struct) o classi C++.

Analisi: Implementazione di algoritmi per il calcolo del passo gara, il degrado degli pneumatici, l'analisi delle zone di frenata e la comparazione prestazionale tra piloti.

Struttura dei Dati
I file CSV esportati seguono una formattazione standard per facilitare il parsing:

giri.csv: Contiene informazioni su tempi sul giro, settori e mescole utilizzate.

telemetria.csv: (Opzionale) Contiene dati ad alta frequenza su velocità, marce e utilizzo dei pedali.

Requisiti
Python 3.x

Libreria fastf1

Libreria pandas

Compilatore C++ (supporto a C++11 o superiore)
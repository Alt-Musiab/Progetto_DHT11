# Gruppo :
- Butt Mohammad Musiab
- Musaku Kevin
- Bussi Lorenzo

## Sistema di Monitoraggio per l'Efficienza Energetica

Il nostro progetto crea un sistema completo per monitorare la temperatura e l'umidità all'interno di un ambiente. L'obiettivo è quello di aiutare a ridurre i consumi energetici e promuovere comportamenti più sostenibili attraverso l'analisi dei dati raccolti.

### Architettura del Sistema

Il nostro sistema si basa sul paradigma Produttore-Consumatore.

- **Produttore (Arduino):** utilizza sensori fisici (DHT11) per raccogliere dati sulla temperatura e l'umidità e li trasforma in segnali digitali.

- **Consumatore (Python):** elabora i dati, li salva in un file CSV e li visualizza in tempo reale tramite un'interfaccia grafica (Dear PyGui).

### Relazione Tecnica: Strategie di Sincronizzazione

La sincronizzazione tra i processi è fondamentale per il nostro progetto. Abbiamo adottato tre strategie principali:

1. **Codifica Senza Blocchi (Delay-less Coding):**

- Abbiamo usato la funzione millis() al posto del classico delay() per evitare che l'unità di acquisizione si “congeli” durante l'attesa del campionamento.

- Funzionamento: Arduino controlla se sono trascorsi 2 secondi; se sì, esegue la lettura e invia i dati, altrimenti continua il loop.

2. **Gestione dei Thread (Multithreading):**

- L'applicazione Python è articolata su thread separati per evitare rallentamenti della GUI:

- **Thread di Lettura:** monitora la porta seriale in background.

- **Thread Principale (GUI):** gestisce il rendering del grafico e l'interazione con l'utente.

3. **Buffer di Memoria e Code (Queue):**

- La comunicazione tra il thread di lettura e la GUI avviene tramite una coda che funge da buffer.

- Sincronizzazione: i dati vengono “parcheggiati” nella coda e prelevati dalla GUI quando è pronta.

- Integrità: previene la perdita di pacchetti dati in caso di picchi di carico della CPU o rallentamenti grafici.

### Feedback Hardware e Suggerimenti Utente

Il sistema fornisce feedback tramite LED fisici e indicatori testuali sulla dashboard:

- **Stato LED / Soglia Temperatura / Suggerimento GUI:**

- **Freddo/Stand-by:** 🔵 Blu / < 18°C / “Temperatura bassa: isolare l'ambiente"

- **Comfort/Eco:** 🟢 Verde / 18°C - 25°C / “Efficienza energetica ottimale"

- **Alert/Critico:** 🔴 Rosso / > 25°C / “Riscaldamento eccessivo: aprire le finestre"

### Gestione Dati

Il sistema effettua un campionamento periodico e salva ogni misura in un file `monitoraggio_energetico.csv` con le seguenti colonne:

- **timestamp:** Orario esatto della rilevazione.

- **temperatura:** Valore in gradi Celsius.

- **umidità:** Valore percentuale.

Questo storico permette un'analisi a lungo termine del microclima interno per identificare sprechi energetici ricorrenti.

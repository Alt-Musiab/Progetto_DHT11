# Sistema di Monitoraggio Ambientale con Arduino e Python

## UdA - Sostenibilità Ambientale (TSPIT)

Questo progetto realizza un sistema di **monitoraggio ambientale** capace di rilevare **temperatura e umidità** attraverso un sensore **DHT11** collegato ad **Arduino**.

I dati raccolti vengono inviati tramite **comunicazione seriale** a un'applicazione **Python** che li elabora, li visualizza in **tempo reale** tramite interfaccia grafica e li salva in uno **storico CSV** per analisi successive.

L'obiettivo del progetto è promuovere un **uso consapevole dell'energia** attraverso l'analisi dei parametri ambientali interni.

---

# Architettura del Sistema

Il progetto implementa il paradigma **Produttore - Consumatore**.

### Produttore

Arduino legge i dati dal sensore DHT11 e li invia periodicamente al computer tramite **porta seriale**.

### Consumatori

L'applicazione Python riceve ed elabora i dati attraverso:

* **Thread di lettura seriale**
* **Coda (queue) come buffer**
* **Interfaccia grafica in Dear PyGui**

Questo permette di evitare blocchi dell'interfaccia e garantire la sincronizzazione tra i processi.

---

# Hardware Utilizzato

* Arduino
* Sensore **DHT11**
* LED Blu
* LED Verde
* LED Rosso
* Resistenze
* Breadboard
* Cavi jumper

---

# Logica dei LED

I LED indicano lo stato ambientale in base alla temperatura:

| Stato        | Temperatura | Significato                 |
| ------------ | ----------- | --------------------------- |
| 🔵 LED Blu   | < 18°C      | Ambiente freddo             |
| 🟢 LED Verde | 18°C - 25°C | Comfort energetico          |
| 🔴 LED Rosso | > 25°C      | Possibile spreco energetico |

---

# Comunicazione Serial

Arduino invia i dati nel formato:

```
temperatura,umidità
```

Esempio:

```
22.4,56
```

Ogni pacchetto termina con **newline** per permettere la sincronizzazione della lettura.

---

# Funzionalità dell'Applicazione Python

L'applicazione desktop realizzata con **Dear PyGui** permette di:

* visualizzare **temperatura e umidità in tempo reale**
* mostrare **messaggi di stato energetico**
* visualizzare **grafico della temperatura**
* salvare automaticamente i dati in un file **CSV**

---

# Campionamento Dati

I dati vengono acquisiti a intervalli regolari e salvati in un file CSV con la seguente struttura:

| timestamp | temperatura | umidità |
| --------- | ----------- | ------- |

Esempio:

```
12:30:05,22.4,56
12:30:07,22.6,55
```

Questo consente di mantenere uno **storico delle misurazioni** per analisi successive.

---

# Tecniche di Sincronizzazione Utilizzate

Per garantire il corretto funzionamento del sistema sono state utilizzate diverse tecniche:

### millis() su Arduino

Permette di eseguire il campionamento senza utilizzare `delay()` evitando il blocco del microcontrollore.

### Threading in Python

La lettura della porta seriale avviene su **un thread separato** per non rallentare l'interfaccia grafica.

### Queue (Buffer)

I dati ricevuti vengono inseriti in una **coda condivisa** tra:

* thread di comunicazione seriale
* logica dell'interfaccia grafica

Questo implementa il paradigma **Produttore-Consumatore**.

---

# Struttura del Repository

```
arduino/
codice Arduino per la lettura del sensore e gestione dei LED

python/
applicazione Python con GUI e gestione dati

data/
file CSV di esempio

requisiti.txt
librerie Python necessarie

README.md
documentazione del progetto
```

---

# Installazione

Clonare il repository:

```
git clone https://github.com/Alt-Musiab/Progetto_DHT11.git
```

Installare le dipendenze:

```
pip install -r requirements.txt
```

---

# Obiettivo Didattico

Il progetto dimostra l'integrazione tra:

* sistemi **embedded**
* **comunicazione seriale**
* **programmazione concorrente**
* **visualizzazione dati**

per realizzare un sistema di **monitoraggio ambientale intelligente**.

---

# Autori

Progetto sviluppato da:

* **Butt Mohammad Musiab**
* **Musaku Kevin**
* **Bussi Lorenzo**

per la materia **TSPIT**.

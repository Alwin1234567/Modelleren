# Modelleren

## Doel van het Programma
Dit programma is ontworpen om optimale routes te berekenen voor het halen en brengen van instrumentensets voor GreenCycl.

## Installatie van Graphhopper
Volg de onderstaande stappen om Graphhopper te installeren:

1. Download de gewenste kaart van [Geofabrik](https://download.geofabrik.de/europe/netherlands.html).
2. Download de GraphHopper jar van [GraphHopper Releases](https://github.com/graphhopper/graphhopper/releases/tag/9.1).
3. Plaats zowel de gedownloade kaart als de GraphHopper jar in de [`graphhopper`](python/graphhopper) map.
4. Graphhopper vereist java developmentkit 23 (JDK 23) deze is te downloaden op de [oracle website](https://www.oracle.com/java/technologies/downloads/#jdk23-windows).

Nu bent u klaar om gebruik te maken van Graphhopper.

## Aanpassen van Instellingen
De instellingen van het programma kunnen worden aangepast in het bestand [`constants.py`](python/source/constants/constants.py).

## Data Laden
De data wordt geladen vanuit de map [`locations_data`](python/locations_data). Zorg ervoor dat uw gegevensbestanden in deze map staan voordat u het programma uitvoert.

## Opslag van Resultaten
De resultaten van het programma worden opgeslagen in de map [`results`](python/results). Controleer deze map na het uitvoeren van het programma om de resultaten te bekijken.

## Installatie van Vereiste Bibliotheken
Volg de onderstaande stappen om de vereiste bibliotheken te installeren in een virtuele omgeving:

1. Maak een virtuele omgeving aan:
    ```sh
    cd path/to/modelleren/python/folder
    python -m venv venv
    ```
2. run [`install_requirements.bat`](python/install_requirements.bat)

## Hyper parameters tunen
In de map [`source/flow`](python/source/flow) staat [`hyperparameter_tunen.py`](python/source/flow/hyperparameter_tunen.py) U kunt de hyperparameters voor de hitte functie van simuated anealing bepalen door dit bestand uit te voeren.

## Het Programma Uitvoeren
In de hoofdmap bevindt zich het bestand [`run_alles.py`](python/run_alles.py). U kunt het programma uitvoeren door dit bestand te starten.

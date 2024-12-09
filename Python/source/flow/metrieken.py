from source.locations import Hub
from source.constants import Constants
from source.transport import Route
from datetime import time, timedelta, datetime
from warnings import warn
import pandas as pd
from source.constants import Constants
import os

class Metrieken:
    def __init__(self, hubs: list[Hub]) -> None:
        self._hubs = hubs
        self._alle_routes: list[Route] = []
        # lijsten met metrieken voor elke iteratie aanmaken
        self._benodigde_voertuigen: list[int] = []
        self._aantal_routes: list[int] = []
        self._aantal_kilometers: list[float] = []
        self._aantal_werkuren: list[float] = []
        self._dagdienst_uren: list[float] = []
        self._avonddienst_uren: list[float] = []
        self._nachtdienst_uren: list[float] = []
        self._wachttijd_uren: list[float] = []
        self._kilometerkosten: list[float] = []
        self._personeelskosten: list[float] = []
        self._totale_kosten: list[float] = []
        self._uitloopmarges = []
        self._percentage_uitloopmarge: list[float] = []
        self.add_iteratie()
    
    def alle_routes(self) -> None:
        # alle routes samenvoegen
        alle_routes = []
        for hub in self._hubs:
            alle_routes.extend(hub.routes)
        self._alle_routes = alle_routes

    def add_iteratie(self) -> None:
        self.alle_routes()

        self._benodigde_voertuigen.append(sum([len(hub.autos) for hub in self._hubs]))
        self._aantal_routes.append(len(self._alle_routes))
        self._aantal_kilometers.append(sum([hub.gereden_kilometers for hub in self._hubs]))
        aantal_werkuren = sum([hub.totale_tijd for hub in self._hubs])/60
        self._aantal_werkuren.append(aantal_werkuren) # totale tijd is in minuten
        self._wachttijd_uren.append(sum([hub.totale_wachttijd for hub in self._hubs])/60) # totale wachttijd is in minuten

        dagdienst_uren, avonddienst_uren, nachtdienst_uren = self.uren_per_period(self._alle_routes)
        self._dagdienst_uren.append(dagdienst_uren)
        self._avonddienst_uren.append(avonddienst_uren)
        self._nachtdienst_uren.append(nachtdienst_uren)
        if round(sum([dagdienst_uren, avonddienst_uren, nachtdienst_uren]), 0) != round(aantal_werkuren, 0):
            warn("het aantal uren dagdienst, avonddienst en nachtdienst samen zijn niet gelijk aan het totaal aantal werkuren", RuntimeWarning)

        totale_kilometerkosten = sum([hub.kilometerkosten for hub in self._hubs])
        totale_personeelskosten = sum([hub.personeelskosten for hub in self._hubs])
        self._kilometerkosten.append(totale_kilometerkosten)
        self._personeelskosten.append(totale_personeelskosten)
        self._totale_kosten.append(sum([totale_kilometerkosten, totale_personeelskosten]))
        
        
    def metrieken_to_csv(self) -> None:
        """
        Sla de eigenschappen van de Metrieken class op in een CSV-bestand.

        Parameters:
            None
        """
        # percentage_uitloopmarge verlengen tot lengte andere lijsten
        opvullen = [0] * (len(self._benodigde_voertuigen) - len(self._percentage_uitloopmarge))
        if len(self._benodigde_voertuigen) > len(self._percentage_uitloopmarge):
            percentage_uitloopmarge = self._percentage_uitloopmarge
            percentage_uitloopmarge.extend(opvullen)
            uitloopmarge = self._uitloopmarges
            uitloopmarge.extend(opvullen)
        else:
            percentage_uitloopmarge = self._percentage_uitloopmarge[:len(self._benodigde_voertuigen)]
            uitloopmarge = self._uitloopmarges[:len(self._benodigde_voertuigen)]
            warn("Er zijn meer uitloopmarges berekend dan iteraties toegevoegd, dus niet alle uitloopmarges in excel opgeslagen", RuntimeWarning)

        # Create a dictionary of properties
        data = {
            'benodigde_voertuigen': self._benodigde_voertuigen,
            'aantal_routes': self._aantal_routes,
            'aantal_kilometers': self._aantal_kilometers,
            'aantal_werkuren': self._aantal_werkuren,
            'dagdienst_uren': self._dagdienst_uren,
            'avonddienst_uren': self._avonddienst_uren,
            'nachtdienst_uren': self._nachtdienst_uren,
            'wachttijd_uren': self._wachttijd_uren,
            'kilometerkosten': self._kilometerkosten,
            'personeelskosten': self._personeelskosten,
            'totale_kosten': self._totale_kosten, 
            'uitloop_(minuten)': uitloopmarge,
            'percentage_uitloopmarge': percentage_uitloopmarge
        }

        # Create a DataFrame from the dictionary
        df = pd.DataFrame(data)

        # Define the base file name and folder
        folder = Constants.RESULTS_PATH
        base_name = "metrieken"
        extension = ".csv"
        number = 1

        # Check if the file already exists and add a count if it does
        while os.path.exists(os.path.join(folder, f"{base_name}_{number}{extension}")):
            number += 1
        file_path = os.path.join(folder, f"{base_name}_{number}{extension}")

        # Write the DataFrame to a CSV file
        with open(file_path, 'w') as f:
            f.write('sep=;\n')
            f.close()

        df.to_csv(file_path, index=False, sep=';', mode='a')

    
    @property
    def alle_metrieken(self) -> tuple[list[int], list[int], list[float], list[float], list[float], list[float], list[float], list[float], list[float], list[float], list[float]]:
        return self._benodigde_voertuigen, self._aantal_routes, self._aantal_kilometers, self._aantal_werkuren, self._dagdienst_uren, self._avonddienst_uren, self._nachtdienst_uren, self._wachttijd_uren, self._kilometerkosten, self._personeelskosten, self._totale_kosten

    @property
    def benodigde_voertuigen(self) -> list[int]:
        return self._benodigde_voertuigen
    
    @property
    def aantal_routes(self) -> list[int]:
        return self._aantal_routes
    
    @property
    def aantal_kilometers(self) -> list[float]:
        return self._aantal_kilometers
    
    @property
    def aantal_werkuren(self) -> list[float]:
        return self._aantal_werkuren
    
    @property
    def aantal_uren_per_periode(self) -> tuple[list[float], list[float], list[float]]:
        """
        aantal uren dagdienst, avonddienst en nachtdienst in de hele planning
        """
        return self._dagdienst_uren, self._avonddienst_uren, self._nachtdienst_uren
    
    @property
    def wachttijd_uren(self) -> list[float]:
        return self._wachttijd_uren
    
    @property
    def kosten(self) -> tuple[list[float], list[float], list[float]]:
        """
        kilometer-, personeelskosten en totale kosten van de hele planning
        """
        return self._kilometerkosten, self._personeelskosten, self._totale_kosten
    
    @property
    def uitloopmarge_histogram(self) -> list[float]:
        """
        percentage taken per uitloopmarge
        """
        for uitloopmarge in range(0, 122, 2):
            self.percentage_uitloopmarge(uitloopmarge)
    
    def percentage_uitloopmarge(self, uitloopmarge: float):
        """
        Geeft het percentage van de taken dat een uitloop van meer dan de uitloopmarge heeft.

        Properties:
            uitloopmarge (float): Aantal minuten uitloop.
        """
        self.alle_routes()
        aantal_uitloopmarge: int = 0
        for route in self._alle_routes:
            for taak in route.taken:
                uitloop = float(taak.tijdslot.eindtijd - taak.eindtijd_taak)
                if uitloop >= uitloopmarge:
                    # taak heeft uitloop van meer dan uitloopmarge
                    aantal_uitloopmarge += 1
        totaal_aantal_taken = sum([len(route.taken) for route in self._alle_routes])
        self._uitloopmarges.append(uitloopmarge)
        self._percentage_uitloopmarge.append((aantal_uitloopmarge/totaal_aantal_taken) * 100)
    
    def uren_per_period(self, route_lijst: list[Route]) -> tuple[float, float, float]:
        """
        Geeft totaal aantal uren dagdienst, avonddienst en nachtdienst in de meegegeven routes
        """
        dagdienst = 0
        avonddienst = 0
        nachtdienst = 0
        
        def is_within_period(time_period: tuple[time], check_time: time) -> bool:
            start, end = time_period
            if start <= end:
                return start <= check_time < end
            else:
                return start <= check_time or check_time < end
        
        def get_period(start: time) -> str:
            """
            Get the period of the day based on the start time.

            Parameters:
                start (time): The start time.

            Returns:
                str: The period of the day ('dag', 'avond', 'nacht').
            """
            if is_within_period(Constants.TIJD_DAG, start):
                return "dag"
            elif is_within_period(Constants.TIJD_AVOND, start):
                return "avond"
            elif is_within_period(Constants.TIJD_NACHT, start):
                return "nacht"
            else:
                raise ValueError("Invalid start time")

        def get_duration(period: str, start: time) -> timedelta:
            """
            Get the duration from the given start time to the end of the specified period.

            Parameters:
                period (str): The period ('dag', 'avond', 'nacht').
                start (time): The start time.

            Returns:
                timedelta: The duration from the start time to the end of the period.
            """
            today = datetime.today()
            
            if period == "dag":
                period_end = Constants.TIJD_DAG[1]
            elif period == "avond":
                period_end = Constants.TIJD_AVOND[1]
            elif period == "nacht":
                period_end = Constants.TIJD_NACHT[1]
            else:
                raise ValueError("Invalid period")

            start_dt = datetime.combine(today, start)
            period_end_dt = datetime.combine(today, period_end)

            # Handle periods that go through midnight
            if period_end < start:
                period_end_dt += timedelta(days=1)

            return period_end_dt - start_dt
        
        # def uren_per_period(self, route: Route) -> None:
            # start_time = route.start_tijd.tijd
        for route in route_lijst:
            duration = route.total_time
            current_time = route.start_tijd.tijd
            remaining_duration = timedelta(minutes=duration)
            
            while remaining_duration > timedelta():
                period = get_period(current_time)
                time_in_period = min(get_duration(period, current_time), remaining_duration)
                if period == "dag":
                    dagdienst += (time_in_period.total_seconds()/(60*60))
                elif period == "avond":
                    avonddienst += (time_in_period.total_seconds()/(60*60))
                elif period == "nacht":
                    nachtdienst += (time_in_period.total_seconds()/(60*60))
                # overige tijd bepalen
                remaining_duration = max(remaining_duration - time_in_period, timedelta())
                current_time = (datetime.combine(datetime.today(), current_time) + time_in_period).time()
        
        return dagdienst, avonddienst, nachtdienst

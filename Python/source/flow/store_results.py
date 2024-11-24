import pandas as pd
from typing import List
from source.locations import Hub
from source.constants import Constants
import os

def store_results(hubs: List[Hub]) -> None:
    """
    Sla de resultaten op in een bestand.

    Parameters:
        hubs (List[Hub]): Een lijst met hubs.
    """
    # decide file name based on existing files present
    folder = Constants.RESULTS_PATH
    name = "routes"
    number = 1
    while f"{folder}/{name}_{number}.xlsx" in os.listdir(folder):
        number += 1
    file_name = f"{folder}/{name}_{number}.xlsx"

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    for hub in hubs:
        # Create a DataFrame to store the routes for the current hub
        data = []

        for auto_number, auto in enumerate(hub.autos, start=1):
            auto_number = auto_number
            for route in auto.routes:
                for taak in route.taken:
                    row = [taak.tijdslot.starttijd.dag,
                           auto_number,
                           hub.name,
                           route.start_tijd.time,
                           "->"]
                    for taak in route.taken:
                        row.extend([
                            taak.begintijd_taak.time,
                            taak.ziekenhuis.name,
                            taak.eindtijd_taak.time,
                            "->"
                        ])
                    row.extend([
                        route.eind_tijd
                    ])
                    data.append(row)

        # Create a DataFrame from the data
        df = pd.DataFrame(data)
        df.sort_values(axis=0, by=[0,2], ascending=True)

        # Write the DataFrame to the Excel file
        df.to_excel(writer, sheet_name=hub.name, index=False, header=['startdag route', 'auto nummer'])

    # Save the Excel file
    writer.save()
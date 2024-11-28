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
    while f"{name}_{number}.xlsx" in os.listdir(folder):
        number += 1
    file_name = os.path.join(folder, f"{name}_{number}.xlsx")

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    for hub in hubs:
        # Create a DataFrame to store the routes for the current hub
        data = []

        for auto_number, auto in enumerate(hub.autos, start=1):
            auto_number = auto_number
            for route in auto.routes:
                row = [route.start_tijd.dag,
                        auto_number,
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
                    route.eind_tijd.time
                ])
                data.append(row)
        
        # Determine the maximum length of the rows
        max_length = max(len(row) for row in data)

        # Create headers for the first two columns and None for the rest
        header = ['startdag route', 'auto nummer', "vertrektijd"] + [None] * (max_length - 3)

        # Pad rows with None to ensure they all have the same length
        for row in data:
            row.extend([None] * (max_length - len(row)))

        # Create a DataFrame from the data
        df = pd.DataFrame(data)
        df.sort_values(axis=0, by=[0,1,2], ascending=True)

        # Write the DataFrame to the Excel file
        df.to_excel(writer, sheet_name=hub.name, index=False, header=header)

    # Save the Excel file
    writer.close()
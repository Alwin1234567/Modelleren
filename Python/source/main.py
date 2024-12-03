from flow import Create_locations, Metrieken, Verbeteringen, store_results

def run():
    creator = Create_locations()
    hubs = creator.hubs
    metrieken = Metrieken(hubs)
    verbeteringen = Verbeteringen(hubs, initial_heat=0.5, cooling_interval=5, metrieken=metrieken)
    verbeteringen.verbeteringen()
    metrieken.metrieken_to_csv()
    store_results(hubs)

if __name__ == "__main__":
    run()

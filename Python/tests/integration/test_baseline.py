from source.flow import Create_locations, Metrieken
import pytest
from source.structures import Cost
from source.transport import Route

def test_baseline():
    # Arrange
    create_locations = Create_locations()
    totale_kosten = 0.0
    for hub in create_locations.hubs:
        taken = [taak for route in hub.routes for taak in route.taken]
        distances = hub._distances
        for taak in taken:
            # rij kosten heen
            distance_time_heen = distances.get_distance_time(start = hub, end = taak.ziekenhuis)
            start_time_heen = taak.tijdslot.starttijd - distance_time_heen.time
            totale_kosten += distance_time_heen.cost(start_time_heen.time, taak.ziekenhuis.voorkeur_bak_kar)
            # tijd kosten bij ziekenhuis
            taak_duur = taak.laadtijd
            totale_kosten += Cost.calculate_cost_time(start_time_heen.time, float(taak_duur))
            # rij kosten terug
            distance_time_terug = distances.get_distance_time(start = taak.ziekenhuis, end = hub)
            start_time_terug = taak.tijdslot.starttijd + taak_duur
            totale_kosten += distance_time_terug.cost(start_time_terug.time, taak.ziekenhuis.voorkeur_bak_kar)
    print(f"Totale kosten: {totale_kosten}")

def test_baseline_metrieken():
    # Arrange
    create_locations = Create_locations()
    metrieken = Metrieken(create_locations.hubs)
    
    for hub in create_locations.hubs:
        print('hub:', hub.name)
        taken = [taak for route in hub.routes for taak in route.taken]
        taken_copy = taken.copy()
        distances = hub._distances
        # alle huidige routes uit hub verwijderen
        routes_copy = hub.routes.copy()
        for route in routes_copy:
            hub.remove_route(route)
        # alle taken in eigen route plaatsen
        for taak in taken_copy:
            route = Route(hub, distances)
            # taak starttijd aan begin tijdslot
            taak.set_begintijd_taak(taak.tijdslot.starttijd)
            route.add_taak(taak)
            hub.add_route(route)
        # auto's vullen
        hub.fill_autos()

    # metrieken maken voor nieuwe oplossing
    uitlooptijden = [10, 20, 30, 60, 120, 180]
    for _ in range(len(uitlooptijden)):
            metrieken.add_iteratie()
    for uitloop in uitlooptijden:
        metrieken.percentage_uitloopmarge(uitloop)
    metrieken.metrieken_to_csv()
            

if __name__ == '__main__':
    pytest.main()

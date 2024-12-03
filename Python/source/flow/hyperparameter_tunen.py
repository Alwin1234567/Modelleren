import optuna
from .verbeteringen import Verbeteringen
from .create_locations import Create_locations
from copy import deepcopy

def run_optuna():
    # Create the initial hubs once
    create_locations = Create_locations()
    initial_hubs = deepcopy(create_locations.hubs)

    # Define the objective function
    def objective(trial):
        # Suggest values for initial_heat and heat_reduction
        initial_heat = trial.suggest_float('initial_heat', 0.1, 1.0)
        heat_reduction = trial.suggest_int('heat_reduction', 1, 200)
        
        # Use deepcopy to create a fresh copy of the initial hubs
        hubs = deepcopy(initial_hubs)
        
        # Create an instance of Verbeteringen with the suggested parameters
        verbeteringen = Verbeteringen(hubs, initial_heat=initial_heat, heat_reduction=heat_reduction)
        
        # Run the verbeteringen method
        verbeteringen.verbeteringen()
        
        # Define a metric to optimize (e.g., total cost of all hubs)
        total_cost = sum(hub.cost for hub in verbeteringen.hubs)
        
        return total_cost

    # Create a study and optimize the objective function
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=100)

    # Print the best parameters
    print(f"Best parameters: {study.best_params}")
    print(f"Best value: {study.best_value}")

if __name__ == '__main__':
    run_optuna()
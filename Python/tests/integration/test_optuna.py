from source.flow import hyperparameter_tunen
import pytest

def test_optuna():
    hyperparameter_tunen.run_optuna()

if __name__ == '__main__':
    pytest.main()

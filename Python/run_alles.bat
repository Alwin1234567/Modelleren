@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Run the Python script
python run_alles.py

REM Deactivate the virtual environment
deactivate
@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Ensure pip-tools is installed
pip install pip-tools

REM Sync the libraries with requirements.txt
pip-sync requirements.txt

REM Deactivate the virtual environment
deactivate

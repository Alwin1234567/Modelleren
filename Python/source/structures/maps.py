import subprocess
from pathlib import Path
import atexit
import requests
import psutil
import time
from source.constants import Constants

class Maps:
    _instance = None
    _process = None
    _enabled = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Maps, cls).__new__(cls)
        return cls._instance

    @classmethod
    def enable_maps(cls):
        """
        Schakel de routemaker in door een subprocess te starten.
        """
        if not cls._enabled:
            cls._process = subprocess.Popen(
                ["java", "-Ddw.graphhopper.datareader.file=netherlands-latest.osm.pbf", "-jar", "graphhopper-web-9.1.jar", "server", "config.yml"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,  # Use creationflags for Windows
                cwd=Constants.GRAPHHOPPER_PATH  # Stel de werkmap in
            )
            cls._enabled = True
            print("Maps enabled")

            # Register the cleanup function to be called on script exit
            atexit.register(cls.cleanup)

            # Wait for the service to come online
            start_time = time.time()
            while time.time() - start_time < Constants.STARTUP_WAIT_TIME:
                try:
                    response = requests.get("http://localhost:8989")
                    if response.status_code == 200:
                        print("Maps service is online")
                        return
                except requests.ConnectionError:
                    pass
                time.sleep(0.5)  # Wait for 0.5 seconds before retrying

            print(f"Maps service did not come online within {Constants.STARTUP_WAIT_TIME} seconds")
            cls.disable_maps()  # Clean up if the service did not start

    @classmethod
    def disable_maps(cls):
        """
        Schakel de kaarten uit door het subprocess te stoppen.
        """
        if cls._enabled and cls._process is not None:
            try:
                parent = psutil.Process(cls._process.pid)
                for child in parent.children(recursive=True):
                    try:
                        child.terminate()
                    except psutil.NoSuchProcess:
                        pass
                parent.terminate()
                gone, still_alive = psutil.wait_procs(parent.children(recursive=True), timeout=5)
                for p in still_alive:
                    try:
                        p.kill()
                    except psutil.NoSuchProcess:
                        pass
                parent.wait(5)
            except psutil.NoSuchProcess:
                pass
            finally:
                cls._process = None
                cls._enabled = False
            print("Maps disabled")

    @classmethod
    def cleanup(cls):
        """
        Cleanup function to terminate the subprocess on script exit.
        """
        if cls._enabled and cls._process is not None:
            try:
                parent = psutil.Process(cls._process.pid)
                for child in parent.children(recursive=True):
                    try:
                        child.terminate()
                    except psutil.NoSuchProcess:
                        pass
                parent.terminate()
                gone, still_alive = psutil.wait_procs(parent.children(recursive=True), timeout=5)
                for p in still_alive:
                    try:
                        p.kill()
                    except psutil.NoSuchProcess:
                        pass
                parent.wait(5)
            except psutil.NoSuchProcess:
                pass
            finally:
                cls._process = None
                cls._enabled = False
            print("Maps cleaned up")

    @classmethod
    def is_enabled(cls):
        """
        Controleer of de kaarten zijn ingeschakeld door een ping naar localhost:8989.

        Returns:
            bool: True als de kaarten zijn ingeschakeld en reageren, anders False.
        """
        try:
            response = requests.get("http://localhost:8989")
            return response.status_code == 200
        except requests.ConnectionError:
            return False

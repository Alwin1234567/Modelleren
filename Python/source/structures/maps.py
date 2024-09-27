import subprocess
import os
import signal

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
            # Bepaal de juiste werkmap
            root_folder = os.path.dirname(os.path.abspath(__file__))
            graphhopper_folder = os.path.join(root_folder, '..', 'graphhopper')

            cls._process = subprocess.Popen(
                ["java", "-Ddw.graphhopper.datareader.file=netherlands-latest.osm.pbf", "-jar", "graphhopper-web-9.1.jar", "server", "config.yml"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,
                cwd=graphhopper_folder  # Stel de werkmap in
            )
            cls._enabled = True
            print("Maps enabled")

    @classmethod
    def disable_maps(cls):
        """
        Schakel de kaarten uit door het subprocess te stoppen.
        """
        if cls._enabled and cls._process is not None:
            os.killpg(os.getpgid(cls._process.pid), signal.SIGTERM)
            cls._process = None
            cls._enabled = False
            print("Maps disabled")

    @classmethod
    def is_enabled(cls):
        """
        Controleer of de kaarten zijn ingeschakeld.

        Returns:
            bool: True als de kaarten zijn ingeschakeld, anders False.
        """
        return cls._enabled

# Usage
# Maps.enable_maps()
# print(Maps.is_enabled())  # Output: True

# Maps.disable_maps()
# print(Maps.is_enabled())  # Output: False
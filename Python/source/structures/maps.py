import subprocess
import os
import signal

class Maps:
    _instance = None
    _process = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Maps, cls).__new__(cls)
            cls._instance.value = False
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance.value

    @classmethod
    def set_instance(cls, value):
        if value not in [True, False]:
            raise ValueError("Maps_active can only be True or False")
        if cls._instance is None:
            cls._instance = cls()
        cls._instance.value = value

    @classmethod
    def enable_maps(cls):
        """
        Schakel de routemaker in door een subprocess te starten.
        """
        if cls._process is None:
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
            cls.set_instance(True)
            print("Maps enabled")

    @classmethod
    def disable_maps(cls):
        """
        Schakel de kaarten uit door het subprocess te stoppen.
        """
        if cls._process is not None:
            os.killpg(os.getpgid(cls._process.pid), signal.SIGTERM)
            cls._process = None
            cls.set_instance(False)
            print("Maps disabled")

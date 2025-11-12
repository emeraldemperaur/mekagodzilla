import threading
import os
from artisan.artisan import Artisan
from mercurius.mercurius import Mercurius
from prometheus.prometheus import Prometheus
from dotenv import load_dotenv

load_dotenv(verbose=True)
version = VERSION = os.getenv("VERSION", "MekaGodzilla")
def launch(mecha):
    system = Artisan()
    if mecha == 'Mekatron':
        system.console_output(version, system)
        initializer(mecha)
    elif mecha == 'MekaGodzilla':
        system.console_output(version, system)
        initializer(mecha)
    else:
        system.console_output("Mekatron", system)
        initializer(mecha)

def run_mercurius():
    Mercurius().start_server()


def initializer(mecha):
    prometheus = Prometheus(version=version, environment="development")
    if mecha == 'Mekatron':
        prometheus.heimdall.info_log("Initializing Minerva CLI")
    elif mecha == 'MekaGodzilla':
        mercury_thread = threading.Thread(target=run_mercurius(), daemon=False, name="Mercurius API Server")
        mercury_thread.start()


if __name__ == '__main__':
    # input args (--mecha, --process, --varargs, --context) for versionining to start cli tool
    # input args (--mecha) for versioning to start server tool
    launch(version)
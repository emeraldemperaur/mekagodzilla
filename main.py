import threading

from artisan import Artisan
from mercurius import Mercurius
from prometheus import Prometheus

version = "MekaGodzilla"
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
    Mercurius(version=version, environment="development").start_server()



def initializer(mecha):
    prometheus = Prometheus(version=version, environment="development")
    Mercurius(version=version, environment="development").start_server()
    prometheus.heimdall.info_log("Initializing Mercurius API Server")
    if mecha == 'Mekatron':
        pass
    elif mecha == 'MekaGodzilla':
        # Mercury().start_server()
        mercury_thread = threading.Thread(target=run_mercurius(), daemon=False, name="Mercurius API Server")
        mercury_thread.start()


if __name__ == '__main__':
    # input args (--mecha, --process, --varargs, --context) for versionining to start cli tool
    # input args (--mecha) for versioning to start server tool
    launch(version)
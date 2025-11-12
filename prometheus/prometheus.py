# Base User Interface Interactions
from artificer.artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW
from artisan.artisan import Artisan
from imhotep.imhotep import Imhotep
from heimdall.heimdall import Heimdall
from mercurius.mercurius import Mercurius
from mercury.mercury import Mercury
from minerva.minerva import Minerva
from moneta.moneta import Moneta
from remus.remus import Remus
from romulus.romulus import Romulus
from securitas.securitas import Securitas
from soteria.soteria import Soteria
from trulioome.trulioome import TruliooME

class Prometheus:
    _instance = None
    _artisan = Artisan()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Prometheus, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, version, environment):
        if not hasattr(self, '_initialized'):
            print(F"\n{ASCI_BLUE}{ASCI_ARROW} Prometheus Initialized{ASCI_RESET}")
            self.heimdall = Heimdall()
            Heimdall.init_log()
            self.artisan = Artisan()
            self.heimdall.info_log(F"Prometheus Initialized::{self.artisan.userid}")
            self.imhotep = Imhotep(self.heimdall)
            self.mercurius = Mercurius()
            self.heimdall.info_log(F"Mercurius API Server Activated::{self.artisan.platform}")
            self.mercurius.init_log()
            self.mercury = Mercury()
            self.mercury.init_log(ASCI_BLUE, ASCI_ARROW, " Initialized")
            self.minerva = Minerva(self.heimdall)
            self.moneta = Moneta(self.heimdall)
            self.remus = Remus(self.heimdall)
            self.romulus = Romulus(self.heimdall)
            self.securitas = Securitas(self.heimdall)
            self.soteria = Soteria(self.heimdall)
            self.trulioome = TruliooME(self.heimdall)
            self._initialized = True


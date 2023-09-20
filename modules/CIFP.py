from modules.CIFPAirport import CIFPAirport
from modules.FileHandler import FileHandler

# CIFP Data
NAVDATA_DIR = "./navdata"
CIFP_FILENAME = "FAACIFP18"
CIFP_PATH = f"{NAVDATA_DIR}/{CIFP_FILENAME}"
# Navdata Dirs
AIRPORT_DIR = f"{NAVDATA_DIR}/airports"
VOR_DIR = f"{NAVDATA_DIR}/vors"
FIX_DIR = f"{NAVDATA_DIR}/fixes"
# CIFP Line Definitions
CIFP_AIRPORT_PREFIX = "SUSAP"
CIFP_NAVAID_PREFIX = "SUSAD"
CIFP_FIX_PREFIX = "SUSAE"


class CIFP:
    def __init__(self):
        self.airportsToParse = []
        self.checkDirectories()

    def checkDirectories(self):
        fh = FileHandler()
        fh.checkDir(AIRPORT_DIR)
        fh.checkDir(VOR_DIR)
        fh.checkDir(FIX_DIR)

    def checkForAirports(self, airports):
        fh = FileHandler()
        if airports:
            for airport in airports:
                airportFile = f"{AIRPORT_DIR}/{airport}.json"
                if not fh.checkFile(airportFile):
                    self.airportsToParse.append(airport)
        if self.airportsToParse:
            self.parseAirports()

    def parseAirports(self):
        fh = FileHandler()
        if fh.checkFile(CIFP_PATH):
            with open(CIFP_PATH) as cifpFile:
                cifpData = cifpFile.readlines()
                for airport in self.airportsToParse:
                    airportFile = f"{AIRPORT_DIR}/{airport}.json"
                    airportLines = []
                    airportLine = f"{CIFP_AIRPORT_PREFIX} {airport.ljust(4,' ')}"
                    for line in cifpData:
                        if line.startswith(airportLine):
                            airportLines.append(line)
                    cifpAirport = CIFPAirport(airport, airportLines)
                    cifpAirport.toJsonFile(airportFile)

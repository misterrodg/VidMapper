from modules.CIFPAirport import CIFPAirport
from modules.CIFPFix import CIFPFix
from modules.CIFPRestrictive import CIFPRestrictive
from modules.CIFPVOR import CIFPVOR
from modules.FileHandler import FileHandler

# CIFP Data
NAVDATA_DIR = "./navdata"
CIFP_FILENAME = "FAACIFP18"
CIFP_PATH = f"{NAVDATA_DIR}/{CIFP_FILENAME}"
# Navdata Dirs
AIRPORT_DIR = f"{NAVDATA_DIR}/airports"
VOR_DIR = f"{NAVDATA_DIR}/vors"
FIX_DIR = f"{NAVDATA_DIR}/fixes"
RESTRICTIVE_DIR = f"{NAVDATA_DIR}/restrictive"
# CIFP Line Definitions
CIFP_AIRPORT_PREFIX = "SUSAP"
CIFP_NAVAID_PREFIX = "SUSAD"
CIFP_FIX_PREFIX = "SUSAE"
CIFP_RESTRICTIVE_PREFIX = "SUSAU"


class CIFP:
    def __init__(self):
        self.airportsToParse = []
        self.fixesToParse = []
        self.vorsToParse = []
        self.restrictiveToParse = []
        self.checkDirectories()

    def checkForFile(self):
        result = True
        fh = FileHandler()
        if not fh.checkFile(CIFP_PATH):
            result = False
            print(
                f"Unable to find CIFP file at {CIFP_PATH}. Please ensure it is downloaded and in the {NAVDATA_DIR} directory."
            )
        return result

    def checkDirectories(self):
        fh = FileHandler()
        fh.checkDir(AIRPORT_DIR)
        fh.checkDir(VOR_DIR)
        fh.checkDir(FIX_DIR)
        fh.checkDir(RESTRICTIVE_DIR)

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

    def checkForFixes(self, fixes):
        fh = FileHandler()
        if fixes:
            for fix in fixes:
                fixFile = f"{FIX_DIR}/{fix}.json"
                if not fh.checkFile(fixFile):
                    self.fixesToParse.append(fix)
        if self.fixesToParse:
            self.parseFixes()

    def parseFixes(self):
        with open(CIFP_PATH) as cifpFile:
            cifpData = cifpFile.readlines()
            for fix in self.fixesToParse:
                fixFile = f"{FIX_DIR}/{fix}.json"
                fixLine = f"{CIFP_FIX_PREFIX}AENRT   {fix}"
                for line in cifpData:
                    if line.startswith(fixLine):
                        cifpFix = CIFPFix(fix, line)
                        cifpFix.toJsonFile(fixFile)

    def checkForVORs(self, vors):
        fh = FileHandler()
        if vors:
            for vor in vors:
                vorFile = f"{VOR_DIR}/{vor}.json"
                if not fh.checkFile(vorFile):
                    self.vorsToParse.append(vor)
        if self.vorsToParse:
            self.parseVORs()

    def parseVORs(self):
        with open(CIFP_PATH) as cifpFile:
            cifpData = cifpFile.readlines()
            for vor in self.vorsToParse:
                vorFile = f"{VOR_DIR}/{vor}.json"
                vorLine = f"{CIFP_NAVAID_PREFIX}        {vor}"
                for line in cifpData:
                    if line.startswith(vorLine):
                        cifpVor = CIFPVOR(vor, line)
                        cifpVor.toJsonFile(vorFile)

    def checkForRestrictive(self, restrictive):
        fh = FileHandler()
        if restrictive:
            for rest in restrictive:
                restrictiveFile = f"{RESTRICTIVE_DIR}/{rest}.json"
                if not fh.checkFile(restrictiveFile):
                    self.restrictiveToParse.append(rest)
        if self.restrictiveToParse:
            self.parseRestrictive()

    def parseRestrictive(self):
        with open(CIFP_PATH) as cifpFile:
            cifpData = cifpFile.readlines()
            for rest in self.restrictiveToParse:
                restFile = f"{RESTRICTIVE_DIR}/{rest}.json"
                restLines = []
                restLine = f"{CIFP_RESTRICTIVE_PREFIX}"
                for line in cifpData:
                    if line.startswith(restLine) and line[8:19].strip() == rest:
                        restLines.append(line)
                        cifpRest = CIFPRestrictive(rest, restLines)
                        cifpRest.toJsonFile(restFile)

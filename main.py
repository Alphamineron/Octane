from ChipOps import importer
from ChipOps.dfh import JSON
import parser_Browser as pB

from config import CHIPS_JSON, initCONFIG
from utils.spinner import Spinner

initCONFIG()
JSON.storeObjects(CHIPS_JSON, importer.generateChipImports())
print("\n", len(JSON.loadObjects(CHIPS_JSON)), "Objects loaded")
pB.TreeOctane.to_JSON()

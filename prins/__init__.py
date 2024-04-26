import os
import logging
from datetime import datetime

## Init global variables

prinsPath = os.path.normpath(__file__)
projectDepth = prinsPath.split("\\").index("PRINS")

__PROJECTPATH__ = os.path.normpath("\\".join(prinsPath.split("\\")[:projectDepth]))
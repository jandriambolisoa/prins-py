#
# A Prins User is an object that represents an user.
# Like items, they have a folder and an id.json file.
# 

from .base      import PrinsObject
from .utils     import PathFinder

import os
import json

#
# PrinsUser is the base class for users
#

class PrinsUser(PrinsObject):

    """Base class for any 'Prins User'
    """

    def __init__(self, projectRoot) -> None:
        super().__init__(projectRoot)

        self.id = None
        self.aliases = []
        self.rank = None

    @classmethod
    def get(cls):
        pass

    @classmethod
    def getFromAlias(cls):
        pass

    @classmethod
    def create(cls):
        pass
        
    @classmethod
    def delete(cls):
        pass

    def addAlias(self):
        pass

    def removeAlias(self):
        pass

    def setRank(self):
        pass

    def promote(self):
        pass

    def downgrade(self):
        pass

    @classmethod
    def search(cls):
        pass

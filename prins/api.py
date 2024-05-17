#
# This file contains the different objects
# available in the prins api and handles
# the log system.
#

from typing         import Any

from .core.items     import Asset as pAsset
from .core.items     import Show as pShow
from .core.items     import Episode as pEpisode
from .core.items     import Sequence as pSequence
from .core.items     import Shot as pShot

from .core.tags      import Category
from .core.tags      import Task
from .core.tags      import Status
from .core.tags      import Rank

from .core.users     import User as pUser

from prins.engine.logger    import PrinsLogger
from prins.engine.auth      import Gatekeeper

# Reimplement objects with log system
# TODO complete permissions system with
# an encrypted permission list

class Asset (pAsset, PrinsLogger):
    """
    def __getattribute__(self, name: str) -> Any:
        # Log and permission system 
        if not Gatekeeper.authorized(self.__class__.__name__, name):
            super()._log(2, "%s %s, permission failed"%(self.__class__.__name__, name))
            raise PermissionError("Unauthorized action.")
        
        super()._log(1, "%s %s"%(self.__class__.__name__, name))
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str) -> Any:
        super()._log(3, "%s %s, failed"%(self.__class__.__name__, name))"""


class Show (pShow, PrinsLogger):

    def __getattribute__(self, name: str) -> Any:
        # Log and permission system 
        if not Gatekeeper.authorized(self.__class__.__name__, name):
            super()._log(2, "%s %s, permission failed"%(self.__class__.__name__, name))
            raise PermissionError("Unauthorized action.")
        
        super()._log(1, "%s %s"%(self.__class__.__name__, name))
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str) -> Any:
        super()._log(3, "%s %s, failed"%(self.__class__.__name__, name))



class Episode (pEpisode, PrinsLogger):

    def __getattribute__(self, name: str) -> Any:
        # Log and permission system 
        if not Gatekeeper.authorized(self.__class__.__name__, name):
            super()._log(2, "%s %s, permission failed"%(self.__class__.__name__, name))
            raise PermissionError("Unauthorized action.")
        
        super()._log(1, "%s %s"%(self.__class__.__name__, name))
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str) -> Any:
        super()._log(3, "%s %s, failed"%(self.__class__.__name__, name))



class Sequence (pSequence, PrinsLogger):

    def __getattribute__(self, name: str) -> Any:
        # Log and permission system 
        if not Gatekeeper.authorized(self.__class__.__name__, name):
            super()._log(2, "%s %s, permission failed"%(self.__class__.__name__, name))
            raise PermissionError("Unauthorized action.")
        
        super()._log(1, "%s %s"%(self.__class__.__name__, name))
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str) -> Any:
        super()._log(3, "%s %s, failed"%(self.__class__.__name__, name))



class Shot (pShot, PrinsLogger):

    def __getattribute__(self, name: str) -> Any:
        # Log and permission system 
        if not Gatekeeper.authorized(self.__class__.__name__, name):
            super()._log(2, "%s %s, permission failed"%(self.__class__.__name__, name))
            raise PermissionError("Unauthorized action.")
        
        super()._log(1, "%s %s"%(self.__class__.__name__, name))
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str) -> Any:
        super()._log(3, "%s %s, failed"%(self.__class__.__name__, name))


class User (pUser, PrinsLogger):

    def __getattribute__(self, name: str) -> Any:
        # Log and permission system 
        if not Gatekeeper.authorized(self.__class__.__name__, name):
            super()._log(2, "%s %s, permission failed"%(self.__class__.__name__, name))
            raise PermissionError("Unauthorized action.")
        
        super()._log(1, "%s %s"%(self.__class__.__name__, name))
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str) -> Any:
        super()._log(3, "%s %s, failed"%(self.__class__.__name__, name))


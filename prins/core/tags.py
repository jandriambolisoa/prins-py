from .base import PrinsObject
import os
import yaml

#
# PrinsTag is the base class for tags
# Users should not interact with tags.
# They are defined in separate yaml files.
#

class PrinsTag(PrinsObject):

    """Base class for any 'Prins Tag'
    """

    def __init__(self) -> None:
        root = None
        super().__init__(root)

        self.id = None

    def asString(self):
        """Returns the string version of an item variable

        :param kValue: Key value
        :type kValue: int
        :return: The key as a text
        :rtype: string
        """
        # Import labels yaml file as a dict
        folderpath, filename = os.path.split(os.path.normpath(__file__))
        labelsPath = os.path.join(folderpath, "labels.yml")
        with open(labelsPath, "r") as f:
            labels = yaml.safe_load(f)

        return labels[self.__class__.__name__].get(self.id, "Unknown")
    
    def asInt(self, label):
        """Returns the int version of an item label

        :param label: The label
        :type label: str
        :return: The label as a int
        :rtype: int
        """
        # Import labels yaml file as a dict
        folderpath, filename = os.path.split(os.path.normpath(__file__))
        labelsPath = os.path.join(folderpath, "labels.yml")
        with open(labelsPath, "r") as f:
            labels = yaml.safe_load(f)

        # Inverse the dict
        inv_dict = {v: k for k, v in labels[self.__class__.__name__].items()}

        return inv_dict[label]
    
    @classmethod
    def _listKeys(cls):
        """Returns a list of every item's attribute

        :return: Every item's attr
        :rtype: list(str,)
        """
        allKeys = []
        classAsDict = cls.__dict__

        for key in list(classAsDict.keys()):
            if "k" in key[0]:
                allKeys.append(key)

        return allKeys
    
    @classmethod
    def _listValues(cls):
        """Returns a list of every item's attribute's value

        :return: Every item's attr value
        :rtype: list(int,)
        """
        allValues = []
        allKeys = cls._listKeys()
        classAsDict = cls.__dict__

        for key in allKeys:
            allValues.append(classAsDict[key])

        return allValues
    
#
# Differents tags are :
#   - Status
#   - Task
#   - Category
#   - Rank
#

class Category(PrinsTag):
    
    # Asset
    kNone = 0
    kProp = 1
    kCharacter = 2
    kEnv = 3
    kAnimal = 4
    kNature = 5
    kVehicle = 6

    # Show
    kShort = 91 
    kSeries = 92 
    kFeature = 93 

    def __init__(self):
        super().__init__()


class Task(PrinsTag):

    # Asset  
    kNone = 0 
    kModeling = 1 
    kTexturing = 2 
    kRigging = 3 
    kShading = 4 
    kSetDressing = 5 
    kDesign = 6

    # Shot
    kAnimation = 51
    kLighting = 52
    kFX = 53
    kCFX = 54
    kCompositing = 55
    kPreviz = 56

    kTesting = 99

    def __init__(self):
        super().__init__()


class Status(PrinsTag):

    kNone = 0

    kAssetStandBy = 11
    kAssetInProgress = 12
    kAssetAbort = 18
    kAssetDone = 19

    kTaskToDo = 21
    kTaskInProgress = 22
    kTaskToReview = 23
    kTaskAbort = 28
    kTaskDone = 29

    kShowStandBy = 31
    kShowInProgress = 32
    kShowAbort = 38
    kShowDone = 39

    kEpisodeStandBy = 41
    kEpisodeInProgress = 42
    kEpisodeAbort = 48
    kEpisodeDone = 49

    kSequenceStandBy = 51
    kSequenceInProgress = 52
    kSequenceAbort = 58
    kSequenceDone = 59

    kShotStandBy = 61
    kShotInProgress = 62
    kShotAbort = 68
    kShotDone = 69

    def __init__(self):
        super().__init__()


class Rank(PrinsTag):

    kAdmin = -1
    
    kNone = 0
    kArtist = 1
    kSupervisor = 2
    
    def __init__(self):
        super().__init__()


# that's all folks #
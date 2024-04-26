import os
import yaml
from datetime import datetime

import hashlib

class Gatekeeper:

    """The class responsible for permissions.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def authorized(obj, action):
        """Checks if the current user can execute the
        requested action.

        :param obj: The object doing an action
        :type obj: str
        :param action: The action name
        :type action: str
        :return: Returns an authorisation
        :rtype: bool
        """

        activeUserRank = int(os.environ.get("PRINS_AUTH_LEVEL", "0"))

        # Import labels yaml file as a dict
        # TODO Encryption things to make that yaml file readable not writable
        # + date verif on that yaml + handle wrong arg errors
        folderpath, filename = os.path.split(os.path.normpath(__file__))
        authPath = os.path.join(folderpath, "auth.yml")
        with open(authPath, "r") as f:
            authList = yaml.safe_load(f)

        if activeUserRank == -1:
            return True
        elif authList[obj][action] <= activeUserRank:
            return True
        else:
            return False
        
    
    @staticmethod
    def register(activeUser, activeRank):
        """Setup env var for this user

        :param activeUser: User name
        :type activeUser: str
        :param activeRank: User rank
        :type activeRank: int
        """
        os.environ["PRINS_ACTIVE_USER"] = activeUser
        os.environ["PRINS_AUTH_LEVEL"] = str(activeRank)


class ClefHolder:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get(input):
        """Returns a clef from the given input

        :param input: The input to create clef from
        :type input: str
        :return: The created clef
        :rtype: str
        """

        return hashlib.sha256(input.encode()).hexdigest()

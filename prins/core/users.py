#
# A Prins User is an object that represents an user.
# Like items, they have a folder and an id.json file.
# 

from .base      import PrinsObject
from .utils     import PathFinder
from .items     import PrinsItem
from .tags      import Rank

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


    @classmethod
    def create(cls, projectRoot, datas, userProperties):
        """Create the user folder.
        This method inherits the PrinsItem create method.
        This method describes a common behavior for users and
        must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param userProperties: A dictionnary containing the new user properties
        :type userProperties: dict
        :return: PrinsItem.create()
        :rtype: None
        """

        return PrinsItem.create(projectRoot, datas, userProperties)

    
    @classmethod
    def delete(cls, projectRoot, datas):
        """Delete the user folder. The pipeline aims to be
        non-destructive, instead of removing the folder it
        will rename it with a .toDelete suffix. The database
        should then be cleaned by an Admin user.
        This method inherits the PrinsItem delete method.
        This method describes a common behavior for users and
        must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :return: PrinsItem.delete()
        :rtype: None
        """

        return PrinsItem.delete(projectRoot, datas)


    @classmethod
    def get(cls, projectRoot, datas):
        """Returns the datas read from the requested User.
        This method inherits the PrinsItem get method.
        This method describes a common behavior for users and
        must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :return: The requested user properties as a dict (PrinsItem.get())
        :rtype: dict
        """

        return PrinsItem.get(projectRoot, datas)


    @classmethod
    def search(cls, projectRoot, datas):
        """Returns all the ids of existing users.
        This method inherits the PrinsItem search method.
        This method describes a common behavior for users and
        must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :return: A list of existing users (PrinsItem.search())
        :rtype: list(str,)
        """

        return PrinsItem.search(projectRoot, datas)


    def modify(self, datas, userProperties):
        """Modifies the id.json file of this user.
        This method inherits the PrinsItem modify method.
        This method describes a common behavior for users and
        must be reimplemented.

        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param itemProperties: A dictionnary containing the new user properties
        :type itemProperties: dict
        :return: The current instance (Prins.modify())
        :rtype: self
        """

        return PrinsItem.modify(self, datas, userProperties)


#
# User class inherits the PrinsUser class
#

class User(PrinsUser):

    """This class describes the User object
    in the Prins Pipeline
    """

    def __init__(self,
                 projectRoot,
                 id = None,
                 aliases = [],
                 rank = None,
                 clef = None):
        
        super().__init__(projectRoot)

        self.id = id
        self.aliases = aliases
        self.rank = rank
        self.clef = clef


    @classmethod
    def create(cls,
               projectRoot,
               id,
               aliases,
               rank,
               clef):
        """Creates a User in the Prins Pipeline.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id is the folder name in the database.
        It should be unique for the whole Prins Pipeline.
        Tips : We recommend to use camel case and avoid underscores.
        :type id: str
        :param aliases: Aliases are different names given to that user
        (e.g. Its Windows username.)
        :type aliases: list(str)
        :param rank: A rank determines the permissions of this user.
        :type rank: Rank.property
        :param clef: The clef is a hashed string used for login purposes.
        :type clef: str
        :raises TypeError: Raises an error if an argument is of the wrong type.
        :raises ValueError: Raises an error if an argument is of the wrong value.
        :return: An instance of the created User.
        :rtype: User() object
        """

        # Sanity check
        if not isinstance(projectRoot, str) or not isinstance(id, str) or not isinstance(clef, str):
            raise TypeError("projectRoot, id and clef args must be of type string")
        if not isinstance(aliases, list):
            raise TypeError("aliases arg must be a list of strings")
        if not rank in Rank._listValues():
            raise ValueError("rank arg must be a property of the Rank class")

        # Create
        datas = {
            "projectRoot" : projectRoot,
            "userId" : id
        }

        userProperties = {
            "aliases" : aliases,
            "rank" : rank,
            "clef" : clef
        }

        super().create(projectRoot, datas, userProperties)

        # Return the created asset as a Prins Asset
        return cls(projectRoot, id=id, **userProperties)


    @classmethod
    def delete(cls, projectRoot, id):
        """Append '.toDelete' to the User id (folder).
        This modification suggests that this folder is
        ready to be deleted and will no longer appear as
        an existing User. To cancel that operation, you
        have to manually remove that suffix. Prins prevents
        destructive operations and slows big decisions
        operations on purpose.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id of the User to delete
        :type id: str
        """

        datas = {
            "projectRoot" : projectRoot,
            "userId" : id
        }

        return super().delete(projectRoot, datas)
    

    @classmethod
    def get(cls, projectRoot, id):
        """Returns the requested user as a Prins User object.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id is the folder name in the database.
        :type id: str
        :return: An instance of the user you requested
        :rtype: User() object
        """

        datas = {
            "projectRoot" : projectRoot,
            "userId" : id
        }

        userProperties = super().get(projectRoot, datas)

        # Return the requested asset as a Prins Asset
        return cls(projectRoot, id=id, **userProperties)


    @classmethod
    def search(cls, projectRoot, input, searchBy="id", perfectMatch=False):
        """Returns a list of ids.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param input: User search request. Type "*" to list all Users.
        :type input: str or Rank.property
        :param searchBy: The nature of your input. Valid values are id (name),
        aliases and rank, defaults to "id"
        :type searchBy: str, optional
        :param perfectMatch: Either we are looking for
        an exact info or multiple infos, defaults to False
        :type perfectMatch: bool, optional
        :raises TypeError: Raises an error if arg is of the wrong type
        :return: The search results
        :rtype: list(str,)
        """

        if not isinstance(searchBy, str):
            raise TypeError("searchBy arg must be of type string")
        if not isinstance(perfectMatch, bool):
            raise TypeError("perfectMatch arg must be of type bool")

        datas = {
            "projectRoot" : projectRoot
        }

        allUsers = super().search(projectRoot, datas)

        if input == "*":
            return allUsers

        results = []

        # Search by ids
        if searchBy == "id" and not perfectMatch:
            results = [u for u in allUsers if input in u]
            return results
        elif searchBy == "id" and perfectMatch:
            results = [u for u in allUsers if input == u]
            return results

        # Search by another property
        ## TODO Reduce nesting
        for user in allUsers:
            datas["userId"] = user
            userProperties = super().get(projectRoot, datas)

            if searchBy == "rank":

                if input in list(userProperties[searchBy]):
                    results.append(user)

                    if perfectMatch:
                        break

            elif searchBy == "aliases":

                for alias in userProperties[searchBy]:
                    if input in alias:
                        results.append(user)
                    if perfectMatch:
                        break

        return results


    @classmethod
    def getFromAlias(cls, projectRoot, alias):
        """Returns the requested Prins User instance.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param alias: An alias of the user to find.
        :type alias: str
        :return: An instance of the user you requested
        :rtype: User() object
        """
        
        searchResult = cls.search(cls, projectRoot, alias, searchBy="aliases", perfectMatch=True)
        return cls.get(projectRoot, searchResult[0])

    def addAlias(self, alias):
        """Adds an alias to this user.

        :param alias: Name to add
        :type alias: str
        :raises TypeError: alias arg must be of type string
        :return: self
        :rtype: User() object
        """

        # Sanity check
        if not isinstance(alias, str):
            raise TypeError("alias arg must be of type string.")
        
        datas = {
            "projectRoot" : self.projectRoot,
            "userId" : self.id
        }

        self.aliases.append(alias)

        userProperties = {
            "aliases" : self.aliases,
            "rank" : self.rank,
            "clef" : self.clef
        }

        return super().modify(datas, userProperties)


    def removeAlias(self, alias):
        """Removes an alias to this user.

        :param alias: Name to remove
        :type alias: str
        :raises TypeError: alias arg must be of type string
        :return: self
        :rtype: User() object
        """

        # Sanity check
        if not isinstance(alias, str):
            raise TypeError("alias arg must be of type string.")
        
        datas = {
            "projectRoot" : self.projectRoot,
            "userId" : self.id
        }

        self.aliases.remove(alias)

        userProperties = {
            "aliases" : self.aliases,
            "rank" : self.rank,
            "clef" : self.clef
        }

        return super().modify(datas, userProperties)


    def setRank(self, rank):
        """Changes the rank of this user.

        :param alias: Name to remove
        :type alias: str
        :raises ValueError: rank arg must be of type Rank.property
        :raises ValueError: Negative ranks are priviledged ranks and can not
        be assigned this way.
        :return: self
        :rtype: User() object
        """

        # Sanity check
        if not isinstance(rank, Rank._listValues):
            raise ValueError("rank arg must be a Rank.property")
        if rank < 0:
            raise ValueError("This rank can not be assigned")
        
        datas = {
            "projectRoot" : self.projectRoot,
            "userId" : self.id
        }

        self.rank = rank

        userProperties = {
            "aliases" : self.aliases,
            "rank" : self.rank,
            "clef" : self.clef
        }

        return super().modify(datas, userProperties)


    def promote(self):
        """Promotes this user to the rank n+1

        :raises Exception: Raises an error if there is no higher rank
        :return: self
        :rtype: User() object
        """
        
        datas = {
            "projectRoot" : self.projectRoot,
            "userId" : self.id
        }

        self.rank += 1
        if not self.rank in Rank._listValues():
            self.rank -= 1
            raise Exception("This user has reached the highest rank.")
        
        userProperties = {
            "aliases" : self.aliases,
            "rank" : self.rank,
            "clef" : self.clef
        }

        return super().modify(datas, userProperties)


    def downgrade(self):
        """Downgrades this user to the rank n-1

        :raises Exception: Raises an error if there is no lower rank
        :return: self
        :rtype: User() object
        """
        
        datas = {
            "projectRoot" : self.projectRoot,
            "userId" : self.id
        }

        self.rank -= 1
        if self.rank < 0:
            self.rank += 1
            raise Exception("This user has reached the lower rank.")
        
        userProperties = {
            "aliases" : self.aliases,
            "rank" : self.rank,
            "clef" : self.clef
        }

        return super().modify(datas, userProperties)

    

#
# An item is a Prins object that is used for production and that
# exist as a folder.
# They are used to contain datas such as work and publish files.
# They are described in a id.json file inside that folder.
# Different items are :
#   - Asset
#   - Show
#   - Episode
#   - Sequence
#   - Shot
# The 'id' is the name of the folder.
# For an item to be valid and recognized by the Prins pipeline,
# it needs an id.json file.
#

from .base      import PrinsObject
from .utils     import PathFinder
from .tags      import Category
from .tags      import Status
from .tags      import Task

import os
import yaml
import json

#
# PrinsItem is the base class for items
#

class PrinsItem(PrinsObject):

    """Base class for any 'Prins Item'
    """

    def __init__(self, projectRoot) -> None:
        super().__init__(projectRoot)

    @classmethod
    def create(cls, projectRoot, datas, itemProperties):
        """Create the asset folder. This method describe a common
        behavior for items and must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param itemProperties: A dictionnary containing the new item properties
        :type itemProperties: dict
        :raises TypeError: Raises an error if arg is of the wrong type
        :raises IsADirectoryError: Raises an error if the folder already exists
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be of type string")
        if not isinstance(datas, dict) or not isinstance(itemProperties, dict):
            raise TypeError("datas and itemProperties arg must be of type dict")

        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(cls.__name__)
        finder.setTemplateName("root")
        finder.setDatas(datas)
        
        itemRoot = finder.getResult()

        finder.setTemplateName("id")

        itemId = finder.getResult()

        # Generate root folder
        if not (os.path.isdir(itemRoot)):
            os.makedirs(itemRoot)
        else:
            raise IsADirectoryError("Attempt to create folders failed.")
        
        # Generate id.json
        with open(itemId, "w") as idFile:
            json.dump(itemProperties, idFile)


    @classmethod
    def delete(cls, projectRoot, datas):
        """Delete the asset folder. The pipeline aims to be
        non-destructive, instead of removing the folder it
        will rename it with a .toDelete suffix. The database
        should then be cleaned by an Admin user.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :raises TypeError: Raises an error if arg is of the wrong type
        :raises IsADirectoryError: Raises an error if the folder does not exist
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be of type string")
        if not isinstance(datas, dict):
            raise TypeError("datas arg must be of type dict")

        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(cls.__name__)
        finder.setTemplateName("root")
        finder.setDatas(datas)

        itemRoot = finder.getResult()

        if not os.path.isdir(itemRoot):
            raise NotADirectoryError("Inexistent folder to delete.")

        # Rename this folder to suggest its deletion
        os.rename(itemRoot, "%s.toDelete"%itemRoot)


    @classmethod
    def get(cls, projectRoot, datas):
        """Returns the datas read from the requested Asset.
        This method describe a common behavior for items and
        must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :raises TypeError: Raises an error if arg is of the wrong type
        :raises Exception: Raises an error if the item has no id.json
        :return: The requested item properties as a dict
        :rtype: dict
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be of type string")
        if not isinstance(datas, dict):
            raise TypeError("datas arg must be of type dict")
        
        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(cls.__name__)
        finder.setTemplateName("id")
        finder.setDatas(datas)

        itemId = finder.getResult()

        if os.path.isfile(itemId):
            with open(itemId, "r") as f:
                idDatas = json.load(f)
        else:
            raise Exception("The requested item does not exist")
        
        return idDatas


    @classmethod
    def search(cls, projectRoot, datas):
        """Returns all the ids of an item type.
        This method describe a common behavior for items and
        must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param input: User search request
        :type input: str
        :param perfectMatch: Either we are looking for
        an exact id or multiple ids, defaults to False
        :type perfectMatch: bool, optional
        :raises TypeError: Raises an error if arg is of the wrong type
        :return: All the existing items (ids)
        :rtype: list(str,)
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be a string")
        if not isinstance(datas, dict):
            raise TypeError("datas arg must be a dict")

        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(cls.__name__)
        finder.setTemplateName("parent")
        finder.setDatas(datas)

        parentFolder = finder.getResult()
        allItems = os.listdir(parentFolder)
        
        # Exclude deleted assets
        visibleItems = [item for item in allItems if not ".toDelete" in item]

        return visibleItems

        
    @classmethod
    def getFromPath(cls, projectRoot, path):
        """Return the item as a Prins object. This method describe
        a common behavior for items and must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param path: The path to extract datas from
        :type path: str
        :raises TypeError: Raises an error if arg is of the wrong type
        :raises Exception: Raises an error if the item has no id.json
        :return: The used PathFinder instance containing datas.
        :rtype: PathFinder() object
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be of type string")
        if not isinstance(path, str):
            raise TypeError("datas arg must be of type string")
        
        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(cls.__name__)
        finder.setTemplateName("id")
        finder.update_datasFromPath(path)

        return finder


    @staticmethod
    def publish(projectRoot, datas, item, fileTemplate):
        """Returns a filepath of a publish file. This method describe
        a common behavior for items and must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param item: The type of item to look for
        :type item: str
        :param fileTemplate: The name of the file template to use
        :type fileTemplate: str
        :return: The filepath generated
        :rtype: str
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be of type string")
        if not isinstance(datas, dict):
            raise TypeError("datas arg must be of type dict")
        if not isinstance(item, str) or not isinstance(fileTemplate, str):
            raise TypeError("item and fileTemplate arg must be of type string")

        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(item)
        finder.setTemplateName("publishedFile")
        finder.setTemplateFile(fileTemplate)
        finder.setDatas(datas)

        publishedFilePath = finder.getResult()

        return publishedFilePath


    @staticmethod
    def save(projectRoot, datas, item):
        """Returns a path of a workspace. This method describe
        a common behavior for items and must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param item: The type of item to look for
        :type item: str
        :return: The path generated
        :rtype: str
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be of type string")
        if not isinstance(datas, dict):
            raise TypeError("datas arg must be of type dict")
        if not isinstance(item, str):
            raise TypeError("item arg must be of type string")

        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(item)
        finder.setTemplateName("workspace")
        finder.setDatas(datas)

        workspacePath = finder.getResult()

        return workspacePath


    @staticmethod
    def deliver(projectRoot, datas, item, fileTemplate):
        """Returns a filepath of a delivery file. This method describe
        a common behavior for items and must be reimplemented.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param item: The type of item to look for
        :type item: str
        :param fileTemplate: The name of the file template to use
        :type fileTemplate: str
        :return: The filepath generated
        :rtype: str
        """

        # Sanity check
        if not isinstance(projectRoot, str):
            raise TypeError("projectRoot arg must be of type string")
        if not isinstance(datas, dict):
            raise TypeError("datas arg must be of type dict")
        if not isinstance(item, str) or not isinstance(fileTemplate, str):
            raise TypeError("item and fileTemplate arg must be of type string")

        # Generate paths
        finder = PathFinder(projectRoot)
        finder.setTemplateType(item)
        finder.setTemplateName("deliveryFile")
        finder.setTemplateFile(fileTemplate)
        finder.setDatas(datas)

        deliveryFilepath = finder.getResult()

        return deliveryFilepath


    def modify(self, datas, itemProperties):
        """Modify the id.json file of this item. This method describe
        a common behavior for items and must be reimplemented.

        :param datas: PathFinder needed datas to generate paths
        :type datas: dict
        :param itemProperties: A dictionnary containing the new item properties
        :type itemProperties: dict
        :return: The current instance
        :rtype: self
        """

        # Generate paths
        finder = PathFinder(self.projectRoot)
        finder.setTemplateType(self.__class__.__name__)
        finder.setTemplateName("id")
        finder.setDatas(datas)

        idFilepath = finder.getResult()

        if os.path.isfile(idFilepath):
            with open(idFilepath, "w") as f:
                json.dump(itemProperties, f)

        return self


#
# Items class inherit the PrinsItem class
#

# Asset

class Asset(PrinsItem):

    """This class describes the Asset item
    in the Prins pipeline
    """
    
    def __init__(self,
                 projectRoot,
                 id = None,
                 category = [Category.kNone],
                 status = [Status.kNone],
                 showId = [],
                 description = "No description.",
                 userDatas = {}):
        
        super().__init__(projectRoot)

        self.id = id
        self.category = category
        self.status = status
        self.showId = showId
        self.description = description
        self.userDatas = userDatas

    @classmethod
    def create(cls,
               projectRoot,
               id,
               category = [Category.kProp],
               status = [Status.kAssetStandBy],
               showId = [],
               description = "No description.",
               userDatas = {}):
        """Creates an Asset in the Prins Pipeline.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id is the folder name in the database.
        It should be unique for the whole Prins Pipeline.
        Tips : We recommend to use camel case and avoid underscores.
        :type id: str
        :param category: The list of categories this item belongs to, defaults to [Category.kProp]
        :type category: list(Category.property), optional
        :param status: The production status of this item.
        For convenience this property is held in a list but must be unique,
        defaults to [Status.kAssetStandBy]
        :type status: list(Status.property), optional
        :param showId: An asset can be part of multiple shows.
        The showId arg is a list of Show().id, defaults to []
        :type showId: list(str,), optional
        :param description: A description of the item, defaults to "No description."
        :type description: str, optional
        :param userDatas: Prins items can handle arbitrary datas.
        The userDatas arg is a dict containing those, defaults to {}
        :type userDatas: dict, optional
        :raises TypeError: Raises an error if an argument is of the wrong type.
        :raises ValueError: Raises an error if an argument is of the wrong value.
        :return: An instance of the created Asset.
        :rtype: Asset() object
        """

        # Sanity check
        if not isinstance(projectRoot, str) or not isinstance(id, str) or not isinstance(description, str):
            raise TypeError("projectRoot, id and description args must be of type string")
        if not isinstance(category, list) or not isinstance(showId, list):
            raise TypeError("category and showId args must be lists")
        if not status in Status._listValues():
            raise ValueError("status arg must be a property of the Status class")
        if not isinstance(userDatas, dict):
            raise TypeError("userDatas arg must be of type dict")
        for c in category:
            if not c in Category._listValues():
                raise ValueError("category arg must contain properties of the Category class")

        # Create
        datas = {
            "projectRoot" : projectRoot,
            "assetId" : id
        }

        itemProperties = {
            "category" : category,
            "status" : status,
            "showId" : showId,
            "description" : description,
            "userDatas" : userDatas
        }

        super().create(projectRoot, datas, itemProperties)

        # Return the created asset as a Prins Asset
        return cls(projectRoot, id=id, **itemProperties)
    
    @classmethod
    def delete(cls, projectRoot, id):
        """Append '.toDelete' to the Asset id (folder).
        This modification suggests that this folder is
        ready to be deleted and will no longer appear as
        an existing Asset. To cancel that operation, you
        have to manually remove that suffix. Prins prevents
        destructive operations and slows big decisions
        operations on purpose.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id of the Asset to delete
        :type id: str
        """

        datas = {
            "projectRoot" : projectRoot,
            "assetId" : id
        }

        return super().delete(projectRoot, datas)
    

    @classmethod
    def get(cls, projectRoot, id):
        """Returns the requested asset as a Prins Asset object.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id is the folder name in the database.
        :type id: str
        :return: An instance of the asset you requested
        :rtype: Asset() object
        """

        datas = {
            "projectRoot" : projectRoot,
            "assetId" : id
        }

        itemProperties = super().get(projectRoot, datas)

        # Return the requested asset as a Prins Asset
        return cls(projectRoot, id, **itemProperties)
    

    @classmethod
    def search(cls, projectRoot, input, searchBy="id", perfectMatch=False):
        """Returns a list of ids.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param input: User search request. Type "*" to list all Assets.
        :type input: str or Status.property or Category.property
        :param searchBy: The nature of your input. Valid values are id (name),
        category, status, showId, description or userDatas, defaults to "id"
        :type searchBy: str, optional
        :param perfectMatch: Either we are looking for
        an exact info or multiple infos, defaults to False
        :type perfectMatch: bool, optional
        :raises TypeError: Raises an error if arg is of the wrong type
        :return: All the existing items (ids)
        :rtype: list(str,)
        """

        if not isinstance(searchBy, str):
            raise TypeError("searchBy arg must be of type string")
        if not isinstance(perfectMatch, bool):
            raise TypeError("perfectMatch arg must be of type bool")

        datas = {
            "projectRoot" : projectRoot
        }

        allAssets = super().search(projectRoot, datas)

        if input == "*":
            return allAssets

        results = []

        # Search by ids
        if searchBy == "id" and not perfectMatch:
            results = [a for a in allAssets if input in a]
            return results
        elif searchBy == "id" and perfectMatch:
            results = [a for a in allAssets if input == a]
            return results

        # Search by another property
        for asset in allAssets:
            datas["assetId"] = asset
            assetProperties = super().get(projectRoot, datas)

            try:
                if input in assetProperties[searchBy]:
                    results.append(asset)

                    if perfectMatch:
                        break
            except:
                # I should do smth here but... meh
                continue

        return results


    @classmethod
    def getFromPath(cls, projectRoot, path):
        """Returns the requested Prins asset instance.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param path: The path to extract datas from
        :type path: str
        :return: An instance of the asset you requested
        :rtype: Asset() object
        """

        finder = super().getFromPath(projectRoot, path)
        asset = finder.datas["assetId"]

        return cls.get(projectRoot, asset)
    
    
    def publish(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the publish filepath that will
        be passed in the function to execute.

        :param func: The function that actually publish the file to the
        generated filepath.
        :type func: function
        """
        def _publishAsset(projectRoot, id, task, version, fileTemplate):
            """A submethod that generate a filepath, and then execute
            the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being published as a string
            :type task: str
            :param version: The version published as a string
            :type version: str
            :param fileTemplate: The file template name to generate
            :type fileTemplate: str
            """

            # TODO ye.. smth has to be done here to allow
            # int as version and Task.property as task
            datas = {
                "projectRoot" : projectRoot,
                "assetId" : id,
                "task" : task,
                "version" : version
            }
            item = "Asset"

            # Generate publish filepath
            publishFilepath = super().publish(projectRoot, datas, item, fileTemplate)

            func(publishFilepath)

        return _publishAsset


    def save(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the workspace path that will
        be passed in the function to execute.

        :param func: The function that actually save the file to the
        generated workspace path.
        :type func: function
        """
        def _saveAsset(projectRoot, id, task, dcc):
            """A submethod that generate a workspace path then
            execute the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being published as a string
            :type task: str
            :param dcc: The DCC saving the file as a string
            :type dcc: str
            """

            datas = {
                "projectRoot" : projectRoot,
                "assetId" : id,
                "task" : task,
                "dcc" : dcc
            }
            item = "Asset"

            # Generate workspace path
            workspacePath = super().save(projectRoot, datas, item)

            func(workspacePath)
        
        return _saveAsset
    

    def deliver(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the delivery filepath that will
        be passed in the function to execute.

        :param func: The function that actually deliver the file to the
        generated filepath.
        :type func: function
        """
        def _deliverAsset(projectRoot, id, task, version, fileTemplate):
            """A submethod that generate a filepath, and then execute
            the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being delivered as a string
            :type task: str
            :param version: The version delivered as a string
            :type version: str
            :param fileTemplate: The file template name to generate
            :type fileTemplate: str
            """

            datas = {
                "projectRoot" : projectRoot,
                "assetId" : id,
                "task" : task,
                "version" : version
            }
            item = "Asset"

            # Generate delivery filepath
            deliveryFilepath = super().deliver(projectRoot, datas, item, fileTemplate)

            func(deliveryFilepath)

        return _deliverAsset
    

    def modify(self, value, toModify):
        """Modifies the id.json associated with this asset. First argument
        is the new value and the second the key to modify.

        :param value: The new value to set for this asset
        :type value: str or list or dict
        :param toModify: The key to edit. Valable values are
        - category : value must be list(Category.property)
        - status : value must be list(Status.property)
        - showId : value must be list(str)
        - description : value must be string
        - userDatas : value must be a dict
        :type toModify: str
        :raises ValueError: Raises an error if "toModify" arg is not an asset property.
        :return: self
        :rtype: Asset() object
        """

        datas = {
            "projectRoot" : self.projectRoot,
            "assetId" : self.id
        }

        itemProperties = {
            "category" : self.category,
            "status" : self.status,
            "showId" : self.showId,
            "description" : self.description,
            "userDatas" : self.userDatas
        }

        # Sanity check
        if not toModify in list(itemProperties.keys()):
            raise ValueError("toModify arg is not valid.")

        itemProperties[toModify] = value

        return super().modify(datas, itemProperties)
    

# Show

class Show(PrinsItem):

    """This class describes the Show item
    in the Prins pipeline
    """
    
    def __init__(self,
                 projectRoot,
                 id = None,
                 category = [Category.kNone],
                 status = [Status.kNone],
                 description = "No description.",
                 userDatas = {}):
        
        super().__init__(projectRoot)

        self.id = id
        self.category = category
        self.status = status
        self.description = description
        self.userDatas = userDatas

    @classmethod
    def create(cls,
               projectRoot,
               id,
               category = [Category.kShort],
               status = [Status.kShowStandBy],
               description = "No description.",
               userDatas = {}):
        """Creates a Show in the Prins Pipeline.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id is the folder name in the database.
        It should be unique for the whole Prins Pipeline.
        Tips : We recommend to use camel case and avoid underscores.
        :type id: str
        :param category: The list of categories this item belongs to, defaults to [Category.kShort]
        :type category: list(Category.property), optional
        :param status: The production status of this item.
        For convenience this property is held in a list but must be unique,
        defaults to [Status.kShowStandBy]
        :type status: list(Status.property), optional
        :param description: A description of the item, defaults to "No description."
        :type description: str, optional
        :param userDatas: Prins items can handle arbitrary datas.
        The userDatas arg is a dict containing those, defaults to {}
        :type userDatas: dict, optional
        :raises TypeError: Raises an error if an argument is of the wrong type.
        :raises ValueError: Raises an error if an argument is of the wrong value.
        :return: An instance of the created Show.
        :rtype: Show() object
        """

        # Sanity check
        if not isinstance(projectRoot, str) or not isinstance(id, str) or not isinstance(description, str):
            raise TypeError("projectRoot, id and description args must be of type string")
        if not isinstance(category, list):
            raise TypeError("category arg must be list")
        if not status in Status._listValues():
            raise ValueError("status arg must be a property of the Status class")
        if not isinstance(userDatas, dict):
            raise TypeError("userDatas arg must be of type dict")
        for c in category:
            if not c in Category._listValues():
                raise ValueError("category arg must contain properties of the Category class")

        # Create
        datas = {
            "projectRoot" : projectRoot,
            "showId" : id
        }

        itemProperties = {
            "category" : category,
            "status" : status,
            "description" : description,
            "userDatas" : userDatas
        }

        super().create(projectRoot, datas, itemProperties)

        # Return the created asset as a Prins Show
        return cls(projectRoot, id=id, **itemProperties)
    
    @classmethod
    def delete(cls, projectRoot, id):
        """Append '.toDelete' to the Show id (folder).
        This modification suggests that this folder is
        ready to be deleted and will no longer appear as
        an existing Show. To cancel that operation, you
        have to manually remove that suffix. Prins prevents
        destructive operations and slows big decisions
        operations on purpose.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id of the Show to delete
        :type id: str
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : id
        }

        return super().delete(projectRoot, datas)
    

    @classmethod
    def get(cls, projectRoot, id):
        """Returns the requested show as a Prins Show object.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param id: The id is the folder name in the database.
        :type id: str
        :return: An instance of the show you requested
        :rtype: Show() object
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : id
        }

        itemProperties = super().get(projectRoot, datas)

        # Return the requested asset as a Prins Show
        return cls(projectRoot, id, **itemProperties)
    

    @classmethod
    def search(cls, projectRoot, input, searchBy="id", perfectMatch=False):
        """Returns a list of ids.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param input: User search request. Type "*" to list all Shows.
        :type input: str or Status.property or Category.property
        :param searchBy: The nature of your input. Valid values are id (name),
        category, status, description or userDatas, defaults to "id"
        :type searchBy: str, optional
        :param perfectMatch: Either we are looking for
        an exact info or multiple infos, defaults to False
        :type perfectMatch: bool, optional
        :raises TypeError: Raises an error if arg is of the wrong type
        :return: All the existing items (ids)
        :rtype: list(str,)
        """

        if not isinstance(searchBy, str):
            raise TypeError("searchBy arg must be of type string")
        if not isinstance(perfectMatch, bool):
            raise TypeError("perfectMatch arg must be of type bool")

        datas = {
            "projectRoot" : projectRoot
        }

        allShows = super().search(projectRoot, datas)

        if input == "*":
            return allShows

        results = []

        # Search by ids
        if searchBy == "id" and not perfectMatch:
            results = [s for s in allShows if input in s]
            return results
        elif searchBy == "id" and perfectMatch:
            results = [s for s in allShows if input == s]
            return results

        # Search by another property
        for show in allShows:
            datas["showId"] = show
            showProperties = super().get(projectRoot, datas)

            try:
                if input in showProperties[searchBy]:
                    results.append(show)

                    if perfectMatch:
                        break
            except:
                # I should do smth here but... meh
                continue

        return results


    @classmethod
    def getFromPath(cls, projectRoot, path):
        """Returns the requested Prins show instance.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param path: The path to extract datas from
        :type path: str
        :return: An instance of the show you requested
        :rtype: Show() object
        """

        finder = super().getFromPath(projectRoot, path)
        show = finder.datas["showId"]

        return cls.get(projectRoot, show)
    
    
    def publish(func):
        raise NotImplementedError("A show can not be published.")


    def save(func):
        raise NotImplementedError("A show can not be saved.")
    

    def deliver(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the delivery filepath that will
        be passed in the function to execute.

        :param func: The function that actually deliver the file to the
        generated filepath.
        :type func: function
        """
        def _deliverShow(projectRoot, id, task, version, fileTemplate):
            """A submethod that generate a filepath, and then execute
            the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being delivered as a string
            :type task: str
            :param version: The version delivered as a string
            :type version: str
            :param fileTemplate: The file template name to generate
            :type fileTemplate: str
            """

            datas = {
                "projectRoot" : projectRoot,
                "showId" : id,
                "task" : task,
                "version" : version
            }
            item = "Show"

            # Generate delivery filepath
            deliveryFilepath = super().deliver(projectRoot, datas, item, fileTemplate)

            func(deliveryFilepath)

        return _deliverShow
    

    def modify(self, value, toModify):
        """Modifies the id.json associated with this show. First argument
        is the new value and the second the key to modify.

        :param value: The new value to set for this show
        :type value: str or list or dict
        :param toModify: The key to edit. Valable values are
        - category : value must be list(Category.property)
        - status : value must be list(Status.property)
        - description : value must be string
        - userDatas : value must be a dict
        :type toModify: str
        :raises ValueError: Raises an error if "toModify" arg is not a show property.
        :return: self
        :rtype: Show() object
        """

        datas = {
            "projectRoot" : self.projectRoot,
            "showId" : self.id
        }

        itemProperties = {
            "category" : self.category,
            "status" : self.status,
            "description" : self.description,
            "userDatas" : self.userDatas
        }

        # Sanity check
        if not toModify in list(itemProperties.keys()):
            raise ValueError("toModify arg is not valid.")

        itemProperties[toModify] = value

        return super().modify(datas, itemProperties)
    

# Episode

class Episode(PrinsItem):

    """This class describes the Episode item
    in the Prins pipeline
    """
    
    def __init__(self,
                 projectRoot,
                 parentShow = None,
                 id = None,
                 status = [Status.kNone],
                 description = "No description.",
                 userDatas = {}):
        
        super().__init__(projectRoot)

        self.id = id
        self.parentShow = parentShow
        self.status = status
        self.description = description
        self.userDatas = userDatas

    @classmethod
    def create(cls,
               projectRoot,
               parentShow,
               id,
               status = [Status.kEpisodeStandBy],
               description = "No description.",
               userDatas = {}):
        """Creates an Episode in the Prins Pipeline.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The parentShow is the show id containing this episode.
        :type parentShow: str
        :param id: The id is the folder name in the database.
        It should be unique for the whole Prins Pipeline.
        Tips : We recommend to use camel case and avoid underscores.
        :type id: str
        :param status: The production status of this item.
        For convenience this property is held in a list but must be unique,
        defaults to [Status.kShowStandBy]
        :type status: list(Status.property), optional
        :param description: A description of the item, defaults to "No description."
        :type description: str, optional
        :param userDatas: Prins items can handle arbitrary datas.
        The userDatas arg is a dict containing those, defaults to {}
        :type userDatas: dict, optional
        :raises TypeError: Raises an error if an argument is of the wrong type.
        :raises ValueError: Raises an error if an argument is of the wrong value.
        :return: An instance of the created Episode.
        :rtype: Episode() object
        """

        # Sanity check
        if not isinstance(projectRoot, str) or not isinstance(id, str) or not isinstance(description, str) or not isinstance(parentShow, str):
            raise TypeError("projectRoot, id, parentShow and description args must be of type string")
        if not status in Status._listValues():
            raise ValueError("status arg must be a property of the Status class")
        if not isinstance(userDatas, dict):
            raise TypeError("userDatas arg must be of type dict")

        # Create
        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : id
        }

        itemProperties = {
            "parentShow" : parentShow,
            "status" : status,
            "description" : description,
            "userDatas" : userDatas
        }

        super().create(projectRoot, datas, itemProperties)

        # Return the created asset as a Prins Episode
        return cls(projectRoot, id=id, **itemProperties)
    
    @classmethod
    def delete(cls, projectRoot, parentShow, id):
        """Append '.toDelete' to the Episode id (folder).
        This modification suggests that this folder is
        ready to be deleted and will no longer appear as
        an existing Episode. To cancel that operation, you
        have to manually remove that suffix. Prins prevents
        destructive operations and slows big decisions
        operations on purpose.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The id of the parent show
        :type parentShow: str
        :param id: The id of the Episode to delete
        :type id: str
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : id
        }

        return super().delete(projectRoot, datas)
    

    @classmethod
    def get(cls, projectRoot, parentShow, id):
        """Returns the requested episode as a Prins Episode object.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The id of the parent show
        :type parentShow: str
        :param id: The id is the folder name in the database.
        :type id: str
        :return: An instance of the episode you requested
        :rtype: Episode() object
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : id
        }

        itemProperties = super().get(projectRoot, datas)

        # Return the requested asset as a Prins Episode
        return cls(projectRoot, id, **itemProperties)
    

    @classmethod
    def search(cls, projectRoot, parentShow, input, searchBy="id", perfectMatch=False):
        """Returns a list of ids.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The id of the parent show
        :type parentShow: str
        :param input: User search request. Type "*" to list all Episodes.
        :type input: str or Status.property or Category.property
        :param searchBy: The nature of your input. Valid values are id (name),
        status, description or userDatas, defaults to "id"
        :type searchBy: str, optional
        :param perfectMatch: Either we are looking for
        an exact info or multiple infos, defaults to False
        :type perfectMatch: bool, optional
        :raises TypeError: Raises an error if arg is of the wrong type
        :return: All the existing items (ids)
        :rtype: list(str,)
        """

        if not isinstance(searchBy, str):
            raise TypeError("searchBy arg must be of type string")
        if not isinstance(perfectMatch, bool):
            raise TypeError("perfectMatch arg must be of type bool")

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow
        }

        allEpisodes = super().search(projectRoot, datas)

        if input == "*":
            return allEpisodes

        results = []

        # Search by ids
        if searchBy == "id" and not perfectMatch:
            results = [e for e in allEpisodes if input in e]
            return results
        elif searchBy == "id" and perfectMatch:
            results = [e for e in allEpisodes if input == e]
            return results

        # Search by another property
        for episode in allEpisodes:
            datas["episodeId"] = episode
            episodeProperties = super().get(projectRoot, datas)

            try:
                if input in episodeProperties[searchBy]:
                    results.append(episode)

                    if perfectMatch:
                        break
            except:
                # I should do smth here but... meh
                continue

        return results


    @classmethod
    def getFromPath(cls, projectRoot, path):
        """Returns the requested Prins episode instance.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param path: The path to extract datas from
        :type path: str
        :return: An instance of the episode you requested
        :rtype: Episode() object
        """

        finder = super().getFromPath(projectRoot, path)
        parentShow = finder.datas["showId"]
        episode = finder.datas["episodeId"]

        return cls.get(projectRoot, parentShow, episode)
    
    
    def publish(func):
        raise NotImplementedError("An episode can not be published.")


    def save(func):
        raise NotImplementedError("An episode can not be saved.")
    

    def deliver(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the delivery filepath that will
        be passed in the function to execute.

        :param func: The function that actually deliver the file to the
        generated filepath.
        :type func: function
        """
        def _deliverEpisode(projectRoot, parentShow, id, task, version, fileTemplate):
            """A submethod that generate a filepath, and then execute
            the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param parentShow: The id of the parent show
            :type parentShow: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being delivered as a string
            :type task: str
            :param version: The version delivered as a string
            :type version: str
            :param fileTemplate: The file template name to generate
            :type fileTemplate: str
            """

            datas = {
                "projectRoot" : projectRoot,
                "showId" : parentShow,
                "episodeId" : id,
                "task" : task,
                "version" : version
            }
            item = "Episode"

            # Generate delivery filepath
            deliveryFilepath = super().deliver(projectRoot, datas, item, fileTemplate)

            func(deliveryFilepath)

            super().deliver(projectRoot, datas, item, fileTemplate)

        return _deliverEpisode
    

    def modify(self, value, toModify):
        """Modifies the id.json associated with this episode. First argument
        is the new value and the second the key to modify.

        :param value: The new value to set for this episode
        :type value: str or list or dict
        :param toModify: The key to edit. Valable values are
        - status : value must be list(Status.property)
        - description : value must be string
        - userDatas : value must be a dict
        :type toModify: str
        :raises ValueError: Raises an error if "toModify" arg is not an episode property.
        :return: self
        :rtype: Episode() object
        """

        datas = {
            "projectRoot" : self.projectRoot,
            "showId" : self.parentShow,
            "episodeId" : self.id
        }

        itemProperties = {
            "parentShow" : self.parentShow,
            "status" : self.status,
            "description" : self.description,
            "userDatas" : self.userDatas
        }

        # Sanity check
        if not toModify in list(itemProperties.keys()):
            raise ValueError("toModify arg is not valid.")

        itemProperties[toModify] = value

        return super().modify(datas, itemProperties)
    

# Sequence

class Sequence(PrinsItem):

    """This class describes the Sequence item
    in the Prins pipeline
    """
    
    def __init__(self,
                 projectRoot,
                 parentShow = None,
                 parentEpisode = None,
                 id = None,
                 status = [Status.kNone],
                 description = "No description.",
                 userDatas = {}):
        
        super().__init__(projectRoot)

        self.id = id
        self.parentShow = parentShow
        self.parentEpisode = parentEpisode
        self.status = status
        self.description = description
        self.userDatas = userDatas

    @classmethod
    def create(cls,
               projectRoot,
               parentShow,
               parentEpisode,
               id,
               status = [Status.kSequenceStandBy],
               description = "No description.",
               userDatas = {}):
        """Creates a Sequence in the Prins Pipeline.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The parentShow is the show id containing this sequence.
        :type parentShow: str
        :param parentEpisode: The parentEpisode is the episode id containing this sequence.
        :type parentEpisode: str
        :param id: The id is the folder name in the database.
        It should be unique for the whole Prins Pipeline.
        Tips : We recommend to use camel case and avoid underscores.
        :type id: str
        :param status: The production status of this item.
        For convenience this property is held in a list but must be unique,
        defaults to [Status.kShowStandBy]
        :type status: list(Status.property), optional
        :param description: A description of the item, defaults to "No description."
        :type description: str, optional
        :param userDatas: Prins items can handle arbitrary datas.
        The userDatas arg is a dict containing those, defaults to {}
        :type userDatas: dict, optional
        :raises TypeError: Raises an error if an argument is of the wrong type.
        :raises ValueError: Raises an error if an argument is of the wrong value.
        :return: An instance of the created Episode.
        :rtype: Episode() object
        """

        # Sanity check
        if not isinstance(projectRoot, str) or not isinstance(id, str) or not isinstance(description, str) or not isinstance(parentShow, str) or not isinstance(parentEpisode, str):
            raise TypeError("projectRoot, id, parentShow and description args must be of type string")
        if not status in Status._listValues():
            raise ValueError("status arg must be a property of the Status class")
        if not isinstance(userDatas, dict):
            raise TypeError("userDatas arg must be of type dict")

        # Create
        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode,
            "sequenceId" : id
        }

        itemProperties = {
            "parentShow" : parentShow,
            "parentEpisode" : parentEpisode,
            "status" : status,
            "description" : description,
            "userDatas" : userDatas
        }

        super().create(projectRoot, datas, itemProperties)

        # Return the created asset as a Prins Sequence
        return cls(projectRoot, id=id, **itemProperties)
    
    @classmethod
    def delete(cls, projectRoot, parentShow, parentEpisode, id):
        """Append '.toDelete' to the Sequence id (folder).
        This modification suggests that this folder is
        ready to be deleted and will no longer appear as
        an existing Sequence. To cancel that operation, you
        have to manually remove that suffix. Prins prevents
        destructive operations and slows big decisions
        operations on purpose.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The id of the parent show
        :type parentShow: str
        :param parentEpisode: The parentEpisode is the episode id containing this sequence.
        :type parentEpisode: str
        :param id: The id of the Episode to delete
        :type id: str
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode,
            "sequenceId" : id
        }

        return super().delete(projectRoot, datas)
    

    @classmethod
    def get(cls, projectRoot, parentShow, parentEpisode, id):
        """Returns the requested sequence as a Prins Sequence object.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The id of the parent show
        :type parentShow: str
        :param parentEpisode: The parentEpisode is the episode id containing this sequence.
        :type parentEpisode: str
        :param id: The id is the folder name in the database.
        :type id: str
        :return: An instance of the sequence you requested
        :rtype: Sequence() object
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode,
            "sequenceId" : id
        }

        itemProperties = super().get(projectRoot, datas)

        # Return the requested asset as a Prins Sequence
        return cls(projectRoot, id, **itemProperties)
    

    @classmethod
    def search(cls, projectRoot, parentShow, parentEpisode, input, searchBy="id", perfectMatch=False):
        """Returns a list of ids.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The id of the parent show
        :type parentShow: str
        :param parentEpisode: The parentEpisode is the episode id containing this sequence.
        :type parentEpisode: str
        :param input: User search request. Type "*" to list all Sequences.
        :type input: str or Status.property
        :param searchBy: The nature of your input. Valid values are id (name),
        status, description or userDatas, defaults to "id"
        :type searchBy: str, optional
        :param perfectMatch: Either we are looking for
        an exact info or multiple infos, defaults to False
        :type perfectMatch: bool, optional
        :raises TypeError: Raises an error if arg is of the wrong type
        :return: All the existing items (ids)
        :rtype: list(str,)
        """

        if not isinstance(searchBy, str):
            raise TypeError("searchBy arg must be of type string")
        if not isinstance(perfectMatch, bool):
            raise TypeError("perfectMatch arg must be of type bool")

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode
        }

        allSequences = super().search(projectRoot, datas)

        if input == "*":
            return allSequences

        results = []

        # Search by ids
        if searchBy == "id" and not perfectMatch:
            results = [s for s in allSequences if input in s]
            return results
        elif searchBy == "id" and perfectMatch:
            results = [s for s in allSequences if input == s]
            return results

        # Search by another property
        for seq in allSequences:
            datas["episodeId"] = seq
            seqProperties = super().get(projectRoot, datas)

            try:
                if input in seqProperties[searchBy]:
                    results.append(seq)

                    if perfectMatch:
                        break
            except:
                # I should do smth here but... meh
                continue

        return results


    @classmethod
    def getFromPath(cls, projectRoot, path):
        """Returns the requested Prins sequence instance.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param path: The path to extract datas from
        :type path: str
        :return: An instance of the episode you requested
        :rtype: Episode() object
        """

        finder = super().getFromPath(projectRoot, path)
        parentShow = finder.datas["showId"]
        parentEpisode = finder.datas["episodeId"]
        sequence = finder.datas["sequenceId"]

        return cls.get(projectRoot, parentShow, parentEpisode, sequence)
    
    
    def publish(func):
        raise NotImplementedError("A sequence can not be published.")


    def save(func):
        raise NotImplementedError("A sequence can not be saved.")
    

    def deliver(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the delivery filepath that will
        be passed in the function to execute.

        :param func: The function that actually deliver the file to the
        generated filepath.
        :type func: function
        """
        def _deliverSequence(projectRoot, parentShow, parentEpisode, id, task, version, fileTemplate):
            """A submethod that generate a filepath, and then execute
            the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param parentShow: The id of the parent show
            :type parentShow: str
            :param parentEpisode: The parentEpisode is the episode id containing this sequence.
            :type parentEpisode: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being delivered as a string
            :type task: str
            :param version: The version delivered as a string
            :type version: str
            :param fileTemplate: The file template name to generate
            :type fileTemplate: str
            """

            datas = {
                "projectRoot" : projectRoot,
                "showId" : parentShow,
                "episodeId" : parentEpisode,
                "sequenceId" : id,
                "task" : task,
                "version" : version
            }
            item = "Sequence"

            # Generate delivery filepath
            deliveryFilepath = super().deliver(projectRoot, datas, item, fileTemplate)

            func(deliveryFilepath)

            super().deliver(projectRoot, datas, item, fileTemplate)

        return _deliverSequence
    

    def modify(self, value, toModify):
        """Modifies the id.json associated with this sequence. First argument
        is the new value and the second the key to modify.

        :param value: The new value to set for this sequence
        :type value: str or list or dict
        :param toModify: The key to edit. Valable values are
        - status : value must be list(Status.property)
        - description : value must be string
        - userDatas : value must be a dict
        :type toModify: str
        :raises ValueError: Raises an error if "toModify" arg is not an sequence property.
        :return: self
        :rtype: Sequence() object
        """

        datas = {
            "projectRoot" : self.projectRoot,
            "showId" : self.parentShow,
            "episodeId" : self.parentEpisode,
            "sequenceId" : self.id
        }

        itemProperties = {
            "parentShow" : self.parentShow,
            "parentEpisode" : self.parentEpisode,
            "status" : self.status,
            "description" : self.description,
            "userDatas" : self.userDatas
        }

        # Sanity check
        if not toModify in list(itemProperties.keys()):
            raise ValueError("toModify arg is not valid.")

        itemProperties[toModify] = value

        return super().modify(datas, itemProperties)
    

# Shot

class Shot(PrinsItem):

    """This class describes the Shot item
    in the Prins pipeline
    """
    
    def __init__(self,
                 projectRoot,
                 parentShow,
                 parentEpisode,
                 parentSequence,
                 id = None,
                 status = [Status.kNone],
                 description = "No description.",
                 userDatas = {}):
        
        super().__init__(projectRoot)

        self.parentShow = parentShow
        self.parentEpisode = parentEpisode
        self.parentSequence = parentSequence
        self.id = id
        self.status = status
        self.description = description
        self.userDatas = userDatas

    @classmethod
    def create(cls,
               projectRoot,
               parentShow,
               parentEpisode,
               parentSequence,
               id,
               status = [Status.kAssetStandBy],
               description = "No description.",
               userDatas = {}):
        """Creates a Shot in the Prins Pipeline.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The show id containing this shot.
        :type parentShow: str
        :param parentEpisode: The episode id containing this shot.
        :type parentEpisode: str
        :param parentSequence: The sequence id containing this shot.
        :type parentSequence: str
        :param id: The id is the folder name in the database.
        It should be unique for the whole Prins Pipeline.
        Tips : We recommend to use camel case and avoid underscores.
        :type id: str
        :param status: The production status of this item.
        For convenience this property is held in a list but must be unique,
        defaults to [Status.kAssetStandBy]
        :type status: list(Status.property), optional
        :param description: A description of the item, defaults to "No description."
        :type description: str, optional
        :param userDatas: Prins items can handle arbitrary datas.
        The userDatas arg is a dict containing those, defaults to {}
        :type userDatas: dict, optional
        :raises TypeError: Raises an error if an argument is of the wrong type.
        :raises ValueError: Raises an error if an argument is of the wrong value.
        :return: An instance of the created Shot.
        :rtype: Shot() object
        """

        # Sanity check
        if not isinstance(projectRoot, str) or not isinstance(id, str) or not isinstance(description, str) or not isinstance(parentShow, str) or not isinstance(parentEpisode, str) or not isinstance(parentSequence, str):
            raise TypeError("projectRoot, id and description args must be of type string")
        if not status in Status._listValues():
            raise ValueError("status arg must be a property of the Status class")
        if not isinstance(userDatas, dict):
            raise TypeError("userDatas arg must be of type dict")
        
        # Create
        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode,
            "sequenceId" : parentSequence,
            "shotId" : id
        }

        itemProperties = {
            "parentShow" : parentShow,
            "parentEpisode" : parentEpisode,
            "parentSequence" : parentSequence,
            "status" : status,
            "description" : description,
            "userDatas" : userDatas
        }

        super().create(projectRoot, datas, itemProperties)

        # Return the created shot as a Prins Shot
        return cls(projectRoot, id=id, **itemProperties)
    
    @classmethod
    def delete(cls, projectRoot, parentShow, parentEpisode, parentSequence, id):
        """Append '.toDelete' to the Shot id (folder).
        This modification suggests that this folder is
        ready to be deleted and will no longer appear as
        an existing Shot. To cancel that operation, you
        have to manually remove that suffix. Prins prevents
        destructive operations and slows big decisions
        operations on purpose.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The show id containing this shot.
        :type parentShow: str
        :param parentEpisode: The episode id containing this shot.
        :type parentEpisode: str
        :param parentSequence: The sequence id containing this shot.
        :type parentSequence: str
        :param id: The id of the Shot to delete
        :type id: str
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode,
            "sequenceId" : parentSequence,
            "shotId" : id
        }

        return super().delete(projectRoot, datas)
    

    @classmethod
    def get(cls, projectRoot, parentShow, parentEpisode, parentSequence, id):
        """Returns the requested shot as a Prins Shot object.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The show id containing this shot.
        :type parentShow: str
        :param parentEpisode: The episode id containing this shot.
        :type parentEpisode: str
        :param parentSequence: The sequence id containing this shot.
        :type parentSequence: str
        :param id: The id is the folder name in the database.
        :type id: str
        :return: An instance of the shot you requested
        :rtype: Shot() object
        """

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode,
            "sequenceId" : parentSequence,
            "shotId" : id
        }

        itemProperties = super().get(projectRoot, datas)

        # Return the requested asset as a Prins Asset
        return cls(projectRoot, id=id, **itemProperties)
    

    @classmethod
    def search(cls, projectRoot, parentShow, parentEpisode, parentSequence, input, searchBy="id", perfectMatch=False):
        """Returns a list of ids.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param parentShow: The show id containing this shot.
        :type parentShow: str
        :param parentEpisode: The episode id containing this shot.
        :type parentEpisode: str
        :param parentSequence: The sequence id containing this shot.
        :type parentSequence: str
        :param input: User search request. Type "*" to list all Assets.
        :type input: str or Status.property or Category.property
        :param searchBy: The nature of your input. Valid values are id (name),
        category, status, showId, description or userDatas, defaults to "id"
        :type searchBy: str, optional
        :param perfectMatch: Either we are looking for
        an exact info or multiple infos, defaults to False
        :type perfectMatch: bool, optional
        :raises TypeError: Raises an error if arg is of the wrong type
        :return: All the existing items (ids)
        :rtype: list(str,)
        """

        if not isinstance(searchBy, str):
            raise TypeError("searchBy arg must be of type string")
        if not isinstance(perfectMatch, bool):
            raise TypeError("perfectMatch arg must be of type bool")

        datas = {
            "projectRoot" : projectRoot,
            "showId" : parentShow,
            "episodeId" : parentEpisode,
            "sequenceId" : parentSequence
        }

        allShots = super().search(projectRoot, datas)

        if input == "*":
            return allShots

        results = []

        # Search by ids
        if searchBy == "id" and not perfectMatch:
            results = [s for s in allShots if input in s]
            return results
        elif searchBy == "id" and perfectMatch:
            results = [s for s in allShots if input == s]
            return results

        # Search by another property
        for shot in allShots:
            datas["shotId"] = shot
            shotProperties = super().get(projectRoot, datas)

            try:
                if input in shotProperties[searchBy]:
                    results.append(shot)

                    if perfectMatch:
                        break
            except:
                # I should do smth here but... meh
                continue

        return results


    @classmethod
    def getFromPath(cls, projectRoot, path):
        """Returns the requested Prins shot instance.

        :param projectRoot: The root path of the current project
        :type projectRoot: str
        :param path: The path to extract datas from
        :type path: str
        :return: An instance of the shot you requested
        :rtype: Shot() object
        """

        finder = super().getFromPath(projectRoot, path)
        parentShow = finder.datas["showId"]
        parentEpisode = finder.datas["episodeId"]
        parentSequence = finder.datas["sequenceId"]
        shot = finder.datas["shotId"]

        return cls.get(projectRoot, parentShow, parentEpisode, parentSequence, shot)
    
    
    def publish(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the publish filepath that will
        be passed in the function to execute.

        :param func: The function that actually publish the file to the
        generated filepath.
        :type func: function
        """
        def _publishShot(projectRoot, parentShow, parentEpisode, parentSequence, id, task, version, fileTemplate):
            """A submethod that generate a filepath, and then execute
            the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param parentShow: The show id containing this shot.
            :type parentShow: str
            :param parentEpisode: The episode id containing this shot.
            :type parentEpisode: str
            :param parentSequence: The sequence id containing this shot.
            :type parentSequence: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being published as a string
            :type task: str
            :param version: The version published as a string
            :type version: str
            :param fileTemplate: The file template name to generate
            :type fileTemplate: str
            """

            # TODO ye.. smth has to be done here to allow
            # int as version and Task.property as task
            datas = {
                "projectRoot" : projectRoot,
                "showId" : parentShow,
                "episodeId" : parentEpisode,
                "sequenceId" : parentSequence,
                "shotId" : id,
                "task" : task,
                "version" : version
            }
            item = "Shot"

            # Generate publish filepath
            publishFilepath = super().publish(projectRoot, datas, item, fileTemplate)

            func(publishFilepath)

        return _publishShot


    def save(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the workspace path that will
        be passed in the function to execute.

        :param func: The function that actually save the file to the
        generated workspace path.
        :type func: function
        """
        def _saveShot(projectRoot, parentShow, parentEpisode, parentSequence, id, task, dcc):
            """A submethod that generate a workspace path then
            execute the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param parentShow: The show id containing this shot.
            :type parentShow: str
            :param parentEpisode: The episode id containing this shot.
            :type parentEpisode: str
            :param parentSequence: The sequence id containing this shot.
            :type parentSequence: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being published as a string
            :type task: str
            :param dcc: The DCC saving the file as a string
            :type dcc: str
            """

            datas = {
                "projectRoot" : projectRoot,
                "showId" : parentShow,
                "episodeId" : parentEpisode,
                "sequenceId" : parentSequence,
                "shotId" : id,
                "task" : task,
                "dcc" : dcc
            }
            item = "Shot"

            # Generate workspace path
            workspacePath = super().save(projectRoot, datas, item)

            func(workspacePath)
        
        return _saveShot
    

    def deliver(func):
        """This method is a decorator. It is designed to be called with
        a bunch of arguments to generate the delivery filepath that will
        be passed in the function to execute.

        :param func: The function that actually deliver the file to the
        generated filepath.
        :type func: function
        """
        def _deliverShot(projectRoot, parentShow, parentEpisode, parentSequence, id, task, version, fileTemplate):
            """A submethod that generate a filepath, and then execute
            the decorator function.

            :param projectRoot: The root path of the current project
            :type projectRoot: str
            :param parentShow: The show id containing this shot.
            :type parentShow: str
            :param parentEpisode: The episode id containing this shot.
            :type parentEpisode: str
            :param parentSequence: The sequence id containing this shot.
            :type parentSequence: str
            :param id: The id is the folder name in the database.
            :type id: str
            :param task: The task being delivered as a string
            :type task: str
            :param version: The version delivered as a string
            :type version: str
            :param fileTemplate: The file template name to generate
            :type fileTemplate: str
            """

            datas = {
                "projectRoot" : projectRoot,
                "showId" : parentShow,
                "episodeId" : parentEpisode,
                "sequenceId" : parentSequence,
                "shotId" : id,
                "task" : task,
                "version" : version
            }
            item = "Shot"

            # Generate delivery filepath
            deliveryFilepath = super().deliver(projectRoot, datas, item, fileTemplate)

            func(deliveryFilepath)

        return _deliverShot
    

    def modify(self, value, toModify):
        """Modifies the id.json associated with this shot. First argument
        is the new value and the second the key to modify.

        :param value: The new value to set for this shot
        :type value: str or list or dict
        :param toModify: The key to edit. Valable values are
        - status : value must be list(Status.property)
        - description : value must be string
        - userDatas : value must be a dict
        :type toModify: str
        :raises ValueError: Raises an error if "toModify" arg is not a shot property.
        :return: self
        :rtype: Shot() object
        """

        datas = {
            "projectRoot" : self.projectRoot,
            "showId" : self.parentShow,
            "episodeId" : self.parentEpisode,
            "sequenceId" : self.parentSequence,
            "shotId" : self.id
        }

        itemProperties = {
            "parentShow" : self.parentShow,
            "parentEpisode" : self.parentEpisode,
            "parentSequence" : self.parentSequence,
            "status" : self.status,
            "description" : self.description,
            "userDatas" : self.userDatas
        }

        # Sanity check
        if not toModify in list(itemProperties.keys()):
            raise ValueError("toModify arg is not valid.")

        itemProperties[toModify] = value

        return super().modify(datas, itemProperties)
    

# that's all folks #
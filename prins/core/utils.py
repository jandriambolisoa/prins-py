#
# This file contains utility classes
#

import os
import yaml
import json

# 
# PathFinder is the path generator of the Prins pipeline
# The Prins PathFinder class is designed to generate pipeline
# friendly filenames and filepaths. This class is a builder.
# WARNING : Attributes must not be edited directly. Methods are
# available to do so.
#

class PathFinder:

    def __init__(self, projectRoot) -> None:

        self.projectRoot = projectRoot

        self.templateType = None
        self.templateName = None
        self.templateFile = None

        self.datas = {
            "projectRoot": self.projectRoot,
            "task": None,
            "assetId": None,
            "userId": None,
            "version": None,
            "iteration": None,
            "UDIM": None,
            "showId": None,
            "episodeId": None,
            "sequenceId": None,
            "shotId": None,
            "dcc": None
        }

    def __str__(self):
        return str("<Prins Utility : %s>"%(self.__class__.__name__))

    def setTemplateType(self, input):
        """Set the templateType class variable

        :param input: The template type
        :type input: str
        :raises TypeError: Raises an error if the input arg is not a string
        :return: The current instance of PathFinder
        :rtype: self
        """

        if not isinstance(input, str):
            raise TypeError("Template type must be a string.")
        
        self.templateType = input
        return self

    def setTemplateName(self, input):
        """Set the templateName class variable

        :param input: The template name
        :type input: str
        :raises TypeError: Raises an error if the input arg is not a string
        :return: The current instance of PathFinder
        :rtype: self
        """

        if not isinstance(input, str):
            raise TypeError("Template name must be a string.")

        self.templateName = input
        return self

    def setTemplateFile(self, input):
        """Set the templateFile class variable

        :param input: The file template name
        :type input: str
        :raises TypeError: Raises an error if the input arg is not a string
        :return: The current instance of PathFinder
        :rtype: self
        """

        if not isinstance(input, str):
            raise TypeError("File template name must be a string.")
        
        self.templateFile = input
        return self


    def setDatas(self, newDatas):
        """Overrides existing datas with new datas

        :param newDatas: A dictionnary containing datas
        :type newDatas: dict
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Note invalid newDatas keys
        invalidKeys = []

        for k in list(newDatas.keys()):
            if k in list(self.datas.keys()):
                # If the new data is valid, replace
                self.datas[k] = newDatas[k]

            else:
                invalidKeys.append(k)

        # Inform the user if keys were not used
        if (invalidKeys):
            print("At least one data is unknown and cannot be updated : %s"%(invalidKeys))

        return self


    def update_projectRoot(self, input):
        """Update the projectRoot key from the self.datas with the user input

        :param input: projectRoot as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :raises Exception: Raises an error if the input has no slashes
        :return: The current instance of PathFinder
        :rtype: self
        """

        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")

        # Check if the root is a valid path
        if not os.path.isdir(os.path.normpath(input)):
            raise Exception("The project root must be a valid path")

        # Update datas
        data = {"projectRoot":os.path.normpath(input)}
        self.setDatas(data)

        return self


    def update_task(self, input):
        """Update the task key from the self.datas with the user input

        :param input: Task as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is a string
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"task":input}
        self.setDatas(data)

        return self


    def update_assetId(self, input):
        """Update the assetId key from the self.datas with the user input

        :param input: assetId as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"assetId":input}
        self.setDatas(data)

        return self
    

    def update_userId(self, input):
        """Update the userId key from the self.datas with the user input

        :param input: userId as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"userId":input}
        self.setDatas(data)

        return self


    def update_version(self):
        """Update the version key from the self.datas with the user input

        :param input: version as an integer
        :type input: int
        :raises TypeError: Raises an error if the input is of the wrong type
        :raises ValueError: Raises an error if the input is not between 0 and 999
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an int
        if not isinstance(input, int):
            raise TypeError("The input arg must be an integer")
        
        # Convert the input to a string
        if input < 0 or input > 999:
            raise ValueError("The version must be between 0 and 999")
        input = "v%03d"%input

        # Update datas
        data = {"version":input}
        self.setDatas(data)

        return self


    def update_iteration(self, input):
        """Update the iteration key from the self.datas with the user input

        :param input: iteration as an integer
        :type input: int
        :raises TypeError: Raises an error if the input is of the wrong type
        :raises ValueError: Raises an error if the input is not between 0 and 999
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, int):
            raise TypeError("The input arg must be an integer")
        
        # Convert the input to a string
        if input < 0 or input > 999:
            raise ValueError("The iteration must be between 0 and 999")
        input = "%03d"%input

        # Update datas
        data = {"iteration":input}
        self.setDatas(data)

        return self

    def update_UDIM(self, input):
        """Update the UDIM key from the self.datas with the user input

        :param input: UDIM as an integer
        :type input: int
        :raises TypeError: Raises an error if the input is of the wrong type
        :raises ValueError: Raises an error if the input is inferior to 1001
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an int
        if not isinstance(input, int):
            raise TypeError("The input arg must be an integer")
        
        # Convert the input to a string
        if input < 1001:
            raise ValueError("The UDIM value must be greater than 1001")
        input = "%03d"%input

        # Update datas
        data = {"UDIM":input}
        self.setDatas(data)

        return self

    def update_showId(self, input):
        """Update the showId key from the self.datas with the user input

        :param input: showId as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"showId":input}
        self.setDatas(data)

        return self


    def update_episodeId(self, input):
        """Update the episodeId key from the self.datas with the user input

        :param input: episodeId as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"episodeId":input}
        self.setDatas(data)

        return self


    def update_sequenceId(self, input):
        """Update the sequenceId key from the self.datas with the user input

        :param input: sequenceId as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"sequenceId":input}
        self.setDatas(data)

        return self


    def update_shotId(self, input):
        """Update the shotId key from the self.datas with the user input

        :param input: shotId as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"shotId":input}
        self.setDatas(data)

        return self


    def update_dcc(self, input):
        """Update the dcc key from the self.datas with the user input

        :param input: dcc as a string
        :type input: str
        :raises TypeError: Raises an error if the input is of the wrong type
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Make sure the input is an str
        if not isinstance(input, str):
            raise TypeError("The input arg must be a string")
        
        # Update datas
        data = {"dcc":input}
        self.setDatas(data)

        return self


    def increment_version(self, value = 1):
        """Update the version value

        :param value: Incrementation amount, defaults to 1
        :type value: int, optional
        :raises Exception: Raises an error if self.datas has no version yet
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Check if the datas contains a version
        if not self.datas["version"]:
            raise Exception("No version found in the datas")
        
        newVersion = int(self.datas["version"].lstrip("v"))
        newVersion += value
        newVersion = "v%03d"%newVersion

        data = {"version": newVersion}
        self.setDatas(data)

        return self


    def increment_UDIM(self, value = 1):
        """Update the UDIM value

        :param value: Incrementation amount, defaults to 1
        :type value: int, optional
        :raises Exception: Raises an error if self.datas has no UDIM yet
        :return: The current instance of PathFinder
        :rtype: self
        """
        # Check if the datas contains an UDIM
        if not self.datas["UDIM"]:
            raise Exception("No UDIM found in the datas")
        
        newUDIM = int(self.datas["UDIM"])
        newUDIM += value
        newUDIM = "%s"%newUDIM

        data = {"UDIM": newUDIM}
        self.setDatas(data)

        return self


    def update_datasFromFilename(self, filename):
        """Extract datas from a filename according to the given template

        :param filename: The filename to parse
        :type filename: str
        :raises TypeError: Raises an error if arguments are of the wrong type
        :raises Exception: Raises an error if the filename has no extension
        :raises Exception: Raises an error if the filename does not correspond to the template
        :return: The current instance of PathFinder
        :rtype: self
        """

        # Check if arguments are string and that the filename is valid
        if not isinstance(filename, str):
            raise TypeError("The filename must be of type string")
        if not os.path.splitext(filename)[1]:
            raise Exception("The filename must be a valid filename")

        template = self._getTemplate("Files", self.templateFile)

        # Parse the filename and template
        # Split filename and template into a list
        filename = os.path.splitext(filename)[0]
        splittedFilename = filename.split(".")
        userKeys = splittedFilename[0].split("_")
        if len(splittedFilename) > 1:
            userKeys.append(splittedFilename[1])

        template = os.path.splitext(template)[0]
        splittedTemplate = template.split(".")
        templateKeys = splittedTemplate[0].split("_")
        if len(splittedTemplate) > 1:
            templateKeys.append(splittedTemplate[1])
        
        if len(userKeys) != len(templateKeys):
            raise Exception("The filename is not corresponding to the given template")
        
        # Extract the datas
        extractedDatas = {}

        for i in range(len(userKeys)):
            if templateKeys[i].find("{") > -1:
                key = templateKeys[i].strip("{ }")
                value = userKeys[i]

                extractedDatas[key] = value

        # Update datas
        self.setDatas(extractedDatas)
        return self


    def update_datasFromPath(self, path):
        """Extract datas from a path according to the given self.template

        :param path: The path to extract datas from
        :type path: str
        :raises Exception: This method needs the project root to be set
        :raises Exception: This method needs the template to be set
        :raises TypeError: Raises an error if the path argument is of the wrong type
        :raises Exception: Raises an error if the path is not long enough
        :return: The current instance of PathFinder
        :rtype: self
        """

        # First check if there is a project root, a template and the input type
        if not self.datas["projectRoot"]:
            raise Exception("A project root must be set before updating datas from path")
        if not self.templateType or not self.templateName:
            raise Exception("A template must be set before updating datas from path")
        if not isinstance(path, str):
            raise TypeError("The path argument must be a string")

        path = os.path.normpath(path)

        # Parse the path
        # Split path and template into a list
        rootlessPath = path.lstrip(self.datas["projectRoot"])
        userKeys = rootlessPath.split("\\").insert(0, self.datas["projectRoot"])

        template = self._getTemplate(self.templateType, self.templateName)
        templateKeys = template.split("/")
        
        if len(userKeys) < len(templateKeys):
            raise Exception("Not enough datas extracted from the path.")
        
        # Extract the datas
        extractedDatas = {}

        for i in range(len(userKeys)):
            if templateKeys[i].find("{") > -1:
                key = templateKeys.strip("{ }")
                value = userKeys[i]

                extractedDatas[key] = value

        # Update datas
        self.setDatas(extractedDatas)
        return self


    def clear(self, toClear = "datas"):
        """Clear this instance variables

        :param toClear: What to clear, use * to clear all, defaults to "datas"
        :type toClear: str, optional
        :return: The current instance of PathFinder
        :rtype: self
        """
        
        if "templateType" in toClear or toClear == "template" or "*" in toClear:
            self.templateType = None
        if "templateName" in toClear or toClear == "template" or "*" in toClear:
            self.templateName = None
        if "templateFile" in toClear or toClear == "template" or "*" in toClear:
            self.templateFile = None

        if "data" in toClear or "*" in toClear:
            self.datas = {
                "projectRoot": None,
                "task": None,
                "assetId": None,
                "version": None,
                "iteration": None,
                "UDIM": None,
                "showId": None,
                "episodeId": None,
                "sequenceId": None,
                "shotId": None,
                "dcc": None
            }

        return self


    def getResult(self):
        """Find a path by combining given attributes

        :raises Exception: Raises a custom error if argument is missing
        :raises Exception: Raises an error if the format method fails
        :return: The result path
        :rtype: str
        """
        if not self.templateType or not self.templateName:
            raise Exception("A template must be set to get a result")
        
        pathTemplate = self._getTemplate(self.templateType, self.templateName)

        # If a templateFile is set, generate a filename
        if self.templateFile:
            fileTemplate = self._getTemplate("Files", self.templateFile)
            try:
                filename = fileTemplate.format(**self.datas)
                self.setDatas({"file":filename})
            except:
                raise Exception("An error occured. Datas might be incomplete or wrong")

        try:
            result = os.path.normpath(self.pathTemplate.format(**self.datas))
            return result
        except:
            raise Exception("An error occured. Datas might be incomplete or wrong")


    def _getTemplate(self, type, name):
        """Returns an unformated path template from templateType and templateName.

        :raises ValueError: Raises an error if the requested template does not exist.
        :return: The template with variables to substitute
        :rtype: str
        """

        # Import paths yaml file as a dict
        folderpath, filename = os.path.split(os.path.normpath(__file__))
        filepath = os.path.join(folderpath, "paths.yml")
        with open(filepath, "r") as f:
            paths = yaml.safe_load(f)

        # Get the requested template
        request = paths[self.templateType].get(self.templateName, "Unknown")
        if request == "Unknown":
            raise ValueError("The template is not recognized.")
        
        return request
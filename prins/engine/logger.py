from datetime import datetime
import logging

import os

class PrinsLogger:

    def __init__(self) -> None:
        pass

    def _log(self, level, message):
        """Generates a log.

        :param level: The importance of this log.
        0 is DEBUG, 1 is INFO, 2 is WARNING, 3 is ERROR, 4 is CRITICAL
        :type level: int
        :param user: The user generating this log.
        :type user: str
        :param message: The message to log
        :type message: str
        """

        ## Init logging system
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if not os.path.isdir("../logs"):
            os.makedirs("../logs")

        fileHandler = logging.FileHandler("../logs/%s.log"%(datetime.today().strftime('%Y%m%d')))
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formatter)

        logger = logging.getLogger("prins-py")
        logger.addHandler(fileHandler)

        # Get active user
        activeUser = os.environ.get("PRINS_ACTIVE_USER", os.getlogin())

        levels = {
            0 : lambda message : logger.debug("%s : %s"%(activeUser, message)),
            1 : lambda message : logger.info("%s : %s"%(activeUser, message)),
            2 : lambda message : logger.warning("%s : %s"%(activeUser, message)),
            3 : lambda message : logger.error("%s : %s"%(activeUser, message)),
            4 : lambda message : logger.critical("%s : %s"%(activeUser, message)),
        }

        # Execute
        levels[level](message)
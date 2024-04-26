#
# This file contains the super classes defining the
# Prins pipeline.
#

#
# PrinsObject is the base class for any object
# of the Prins pipeline
#

class PrinsObject:

    """Base class for any 'Prins Object'
    """

    def __init__(self, projectRoot) -> None:
        self.projectRoot = projectRoot
        self.id = None

    def __str__(self):
        return str("<Prins Object : %s>"%(self.__class__.__name__))

# that's all folks #
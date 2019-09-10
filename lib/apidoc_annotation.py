from abc import ABC, abstractmethod

class ApidocAnnotation(ABC):

    def parse(self):
        pass

    def to_swagger(self):
        pass

from abc import ABC, abstractmethod

class ApidocAnnotation(ABC):

    def parse(self):
        pass

    def validate(self):
        pass

    def to_swagger(self):
        pass

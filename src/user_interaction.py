from abc import ABC, abstractmethod

class UserInteraction(ABC):

    @abstractmethod
    def get_input(self):
        ...

class ConsoleUserInteraction(UserInteraction):
    def get_input(self):
        s1 = input("Сторона A: ")
        s2 = input("Сторона B: ")
        s3 = input("Сторона C: ")
        return s1, s2, s3
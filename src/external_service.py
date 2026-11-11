from abc import ABC, abstractmethod
import logging

class ExternalService(ABC):

    @abstractmethod
    def send(self, message: str) -> bool:
        ...

class EmailService(ExternalService):

    def send(self, message: str) -> bool:
        logging.info(f"[EmailService] Отправка: {message}")
        return True
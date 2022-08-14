import logging

logger = logging.getLogger("server_dist")


class PortValidation:
    def __set__(self, instance, val):
        if not 1023 < val < 65536:
            logger.error(f"Порт находится вне промежутка [1023; 65536]")
            exit(1)
        else:
            instance.__dict__[self.name] = val

    def __set_name__(self, owner, name):
        self.name = name

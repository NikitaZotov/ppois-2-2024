import logging


class LoggerUtil:
    @staticmethod
    def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

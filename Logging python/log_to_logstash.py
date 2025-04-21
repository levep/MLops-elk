import logging
import logging.handlers
import json
import socket


class JsonLogstashFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "@timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "host": socket.gethostname()
        }
        return json.dumps(log_record)


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Console handler
    console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Logstash TCP handler
    logstash_handler = logging.handlers.SocketHandler('localhost', 5050)
    logstash_formatter = JsonLogstashFormatter()
    logstash_handler.setFormatter(logstash_formatter)
    logger.addHandler(logstash_handler)

    logger.info('My format changed!')


if __name__ == '__main__':
    main()
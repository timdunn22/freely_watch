import logging
from elasticsearch_dsl.connections import connections


class DisableLogger:
    def __enter__(self):
        logging.disable(logging.CRITICAL)

    def __exit__(self, a, b, c):
        logging.disable(logging.NOTSET)


def wait_elasticsearch_availability():
    good_statuses = ['green', 'yellow']
    with DisableLogger():
        while True:
            try:
                response = connections.get_connection().cluster.health()
                if response.get('status') in good_statuses:
                    return
            except Exception:
                pass

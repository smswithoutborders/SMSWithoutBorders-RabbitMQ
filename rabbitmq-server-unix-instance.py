#!/usr/bin/env python3

import sys, os
import logging
import threading
import subprocess

sbin_path = os.path.join( 
        os.path.dirname(__file__), 'deps/builds/rabbitmq_server-3.9.9/sbin')

rabbitmq_server = sbin_path + "/rabbitmq-server"
rabbitmqctl = sbin_path + "/rabbitmqctl"

logging.basicConfig(level=logging.DEBUG)

def start_rabbitmq_server() -> str:
    """
    """
    try:
        start_rabbitmq_service=rabbitmq_server
        output = subprocess.check_output(start_rabbitmq_service.split(' '), 
                stderr=subprocess.STDOUT).decode('unicode_escape')

    except subprocess.CalledProcessError as error:
        logging.exception(error)
        logging.debug(output)

    else:
        logging.debug("[*] Finished running threading process....")
        logging.debug(output)


def start_service() -> str:
    """
    """
    # start_rabbitmq_service=f"./sbin/rabbitmq-server -detached"
    rabbitmq_thread = threading.Thread(target=start_rabbitmq_server,
            daemon=True)
    rabbitmq_thread.start()
    logging.debug("[*] RabbitMQ services started!")
    rabbitmq_thread.join()


if __name__ == "__main__":
    try:
        logging.debug("[*] Starting RabbitMQ services..")
        start_service()
    except Exception as error:
        raise error

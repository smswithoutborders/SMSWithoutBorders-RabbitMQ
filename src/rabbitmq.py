#!/usr/bin/env python3

import sys, os
import logging
import subprocess
import pika
import json

logging.basicConfig(level=logging.DEBUG)


class RabbitMQ:
    sbin_path = os.path.join(
        os.path.dirname(__file__), "../deps/builds/rabbitmq_server-3.9.9/sbin"
    )

    rabbitmq_server = sbin_path + "/rabbitmq-server"
    rabbitmqctl = sbin_path + "/rabbitmqctl"

    def __init__(self, dev_id: str):
        """ """
        self.dev_id = dev_id

    def add_user(self, dev_key: str) -> None:
        """ """
        if self.exist():
            logging.info("user %s already exist", self.dev_id)
        else:
            try:
                # requires sudo privileges
                # First ".*" for configure permission on every entity
                # Second ".*" for write permission on every entity
                # Third ".*" for read permission on every entity

                create_user_command = (
                    self.rabbitmqctl + f" add_user {self.dev_id} {dev_key}"
                )

                output = subprocess.check_output(
                    create_user_command.split(" "), stderr=subprocess.STDOUT
                ).decode("unicode_escape")

            except subprocess.CalledProcessError as error:
                """TODO:
                check if user already exist
                """
                raise error

            except Exception as error:
                raise error

            else:
                try:
                    logging.debug("[*] New user added")
                    self.__set_users_privilege__()
                    logging.debug("[*] User privilege set")
                except Exception as error:
                    raise error
                else:
                    self.__set_users_tag__()
                    logging.debug("[*] User tag set")

    def delete(self) -> None:
        """ """
        try:
            delete_user_command = self.rabbitmqctl + " delete_user " + self.dev_id

            output = subprocess.check_output(
                delete_user_command.split(" "), stderr=subprocess.STDOUT
            ).decode("unicode_escape")

        except subprocess.CalledProcessError as error:
            """TODO:
            check if user already exist
            """
            raise error

        except Exception as error:
            raise error

    @staticmethod
    def list() -> list:
        """ """
        try:
            list_users_commands = RabbitMQ.rabbitmqctl + " list_users"
            output = subprocess.check_output(
                list_users_commands.split(" "), stderr=subprocess.STDOUT
            ).decode("unicode_escape")

        except subprocess.CalledProcessError as error:
            """TODO:
            check if user already exist
            """
            raise error

        except Exception as error:
            raise error
        else:
            return RabbitMQ._parse_users_(output)

    @classmethod
    def _parse_users_(cls, data) -> list:
        """ """
        data = data.split("\n")[2:]
        users = []
        for line in data:
            line = line.split("[")
            line = line[0].rstrip()
            users.append(line)

        return users

    def exist(self) -> bool:
        """ """
        try:
            list_users_commands = self.rabbitmqctl + " list_users"

            output = subprocess.check_output(
                list_users_commands.split(" "), stderr=subprocess.STDOUT
            ).decode("unicode_escape")

        except subprocess.CalledProcessError as error:
            """TODO:
            check if user already exist
            """
            raise error

        except Exception as error:
            raise error

        else:
            users = self._parse_users_(output)
            return self.dev_id in users

    def __set_users_tag__(self) -> None:
        """
        Exceptions:
            subprocess.CalledProcessError:
                When encounters an issue with locally installed instance of
                RabbitMQ (rabbitmq-server).
        """
        try:
            update_user_permissions= self.rabbitmqctl + \
                    f" set_user_tags {self.dev_id} management"

            output = subprocess.check_output(
                update_user_permissions.split(" "), stderr=subprocess.STDOUT
            ).decode("unicode_escape")

        except subprocess.CalledProcessError as error:
            raise error
        except Exception as error:
            raise error
        else:
            logging.debug("[*] Set users privilege: %s", output)

    def __set_users_privilege__(self) -> None:
        """
        Exceptions:
            subprocess.CalledProcessError:
                When encounters an issue with locally installed instance of
                RabbitMQ (rabbitmq-server).
        """
        try:
            # requires sudo privileges
            # First ".*" for configure permission on every entity
            # Second ".*" for write permission on every entity
            # Third ".*" for read permission on every entity
            update_user_permissions= self.rabbitmqctl + \
                    f" set_permissions -p / {self.dev_id} .* .* .*"

            output = subprocess.check_output(
                update_user_permissions.split(" "), stderr=subprocess.STDOUT
            ).decode("unicode_escape")

        except subprocess.CalledProcessError as error:
            raise error
        except Exception as error:
            raise error
        else:
            logging.debug("[*] Set users privilege: %s", output)

    def request_sms(
        self,
        data: dict,
        rabbitmq_host_url: str = "127.0.0.1",
        rabbitmq_exchange_name: str = "DEKU_CLUSTER_SMS",
        rabbitmq_queue_name: str = "OUTGOING_SMS",
        rabbitmq_exchange_type: str = "topic",
    ) -> None:
        """ """

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_host_url)
        )
        channel = connection.channel()

        """ creates the exchange """
        channel.exchange_declare(
            exchange=rabbitmq_exchange_name,
            exchange_type=rabbitmq_exchange_type,
            durable=True,
        )

        if not "operator_name" in data:
            raise Exception("Missing operator name")

        if not "text" in data:
            raise Exception("Missing text in data")

        if not "number" in data:
            raise Exception("Missing number in data")

        operator_name = data["operator_name"].lower()
        queue_name = "%s_%s_%s" % (self.dev_id, rabbitmq_queue_name, operator_name)
        routing_key = "%s_%s.%s" % (self.dev_id, rabbitmq_queue_name, operator_name)

        """
        FIXME: If queue is created here - might lead to exception handling user created
        queue.
        """
        # channel.queue_declare(queue_name, durable=True)

        text = data["text"]
        number = data["number"]
        data = json.dumps({"text": text, "number": number})

        try:
            channel.basic_publish(
                exchange=rabbitmq_exchange_name,
                routing_key=routing_key,
                body=data,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
        except Exception as error:
            raise error

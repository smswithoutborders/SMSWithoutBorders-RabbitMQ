FROM rabbitmq:3.11-management

COPY ./rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

RUN apt update && apt install -y curl

RUN rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_federation_management rabbitmq_stomp

EXPOSE 15671
EXPOSE 15672

EXPOSE 15692

EXPOSE 5671
EXPOSE 5672
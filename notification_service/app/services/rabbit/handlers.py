import pika
import logging
import json
from utils.email_sender import create_letter, send_email


def register_user(
    channel: pika.adapters.blocking_connection.BlockingChannel, method, properties, body
):
    logging.warning(body)
    payload = body.decode(encoding="utf-8")
    logging.warning(payload)
    logging.warning(type(payload))
    payload_json = json.loads(payload)

    user_email = payload_json["email"]

    letter = create_letter(payload_json, "user_register")
    logging.warning(letter)

    send_email([user_email], mail_body=letter, mail_subject="Registration")

    channel.basic_ack(delivery_tag=method.delivery_tag)


def user_added_product_to_cart(
    channel: pika.adapters.blocking_connection.BlockingChannel, method, properties, body
):
    channel.basic_ack(delivery_tag=method.delivery_tag)

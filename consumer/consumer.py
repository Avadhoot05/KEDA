import pika
import json
from datetime import datetime

def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
    except Exception:
        message = body.decode()
    
    print(f"Received: {message}")
    with open("../consumed_messages.log", "a") as f:
        f.write(f"{datetime.now().isoformat()} - {json.dumps(message)}\n")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',   # Kubernetes service name or IP
    port=5672,                 # Default RabbitMQ port
    virtual_host='/',          # Default virtual host
    credentials=pika.PlainCredentials('guest', 'guest')))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')

    channel.basic_consume(queue='order_queue', on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()

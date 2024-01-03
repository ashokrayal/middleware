import pika
import logging  # Added logging module

def consume_events():
    logging.basicConfig(level=logging.INFO)  # Added logging configuration
    # Implement Rabbit MQ event consumption logic for order creation
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='orders', exchange_type='topic')  # Adjust the exchange_type
    result = channel.queue_declare(queue='order_updates', exclusive=False)
    queue_name = result.method.queue
    logging.info(f"Notification Service 1 connected to RabbitMQ. Queue: {queue_name}")
    channel.queue_bind(exchange='orders', queue=queue_name)

    def callback(ch, method, properties, body):
        logging.info(f"Notification Service 1 received: {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    logging.info("Notification Service 1 waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()

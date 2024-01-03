# notification_service_1.py
import pika
import logging

def consume_events():
    """Consume events from RabbitMQ fanout exchange.

    Connects to RabbitMQ fanout exchange, binds to a queue, and consumes events.

    Raises:
        Exception: If an error occurs during connection or event consumption.

    Returns:
        None
    """
    logging.basicConfig(level=logging.INFO)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='FanoutExchange', exchange_type='fanout')  # Fanout exchange for broadcasting events
    result = channel.queue_declare(queue='OrderCreationQueue', exclusive=False)
    queue_name = result.method.queue
    logging.info(f"Notification Service 1 connected to RabbitMQ. Queue: {queue_name}")
    channel.queue_bind(exchange='FanoutExchange', queue=queue_name)  # Bind to fanout exchange

    def callback(ch, method, properties, body):
        """Callback function for handling received events."""
        logging.info(f"Notification Service 1 received: {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    logging.info("Notification Service 1 waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()

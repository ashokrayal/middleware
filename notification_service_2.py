# notification_service_2.py
import pika
import logging

def consume_events():
    """Consume events from RabbitMQ topic exchange.

    Connects to RabbitMQ topic exchange, binds to a queue, and consumes events selectively.

    Raises:
        Exception: If an error occurs during connection or event consumption.

    Returns:
        None
    """
    logging.basicConfig(level=logging.INFO)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='TopicExchange', exchange_type='topic')  # Topic exchange for selective events
    result = channel.queue_declare(queue='OrderUpdateQueue', exclusive=False)
    queue_name = result.method.queue
    logging.info(f"Notification Service 2 connected to RabbitMQ. Queue: {queue_name}")
    channel.queue_bind(exchange='TopicExchange', queue=queue_name, routing_key='order.update')  # Bind to topic exchange
    channel.queue_bind(exchange='FanoutExchange', queue=queue_name, routing_key='order.update')
    def callback(ch, method, properties, body):
        """Callback function for handling received events."""
        logging.info(f"Notification Service 2 received: {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    logging.info("Notification Service 2 waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()

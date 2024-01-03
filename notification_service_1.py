# Import necessary libraries
import pika
import logging

def consume_events():
    logging.basicConfig(level=logging.INFO)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='order_updates_fanout', exchange_type='fanout')  # Fanout exchange for broadcasting events
    result = channel.queue_declare(queue='order_updates_queue_1', exclusive=False)
    queue_name = result.method.queue
    logging.info(f"Notification Service 1 connected to RabbitMQ. Queue: {queue_name}")
    channel.queue_bind(exchange='order_updates_fanout', queue=queue_name)  # Bind to fanout exchange

    def callback(ch, method, properties, body):
        logging.info(f"Notification Service 1 received: {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    logging.info("Notification Service 1 waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()

# notification_service_2.py
import pika
import logging

def consume_events():
    logging.basicConfig(level=logging.INFO)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='TopicExchange', exchange_type='topic')  # Topic exchange for selective events
    result = channel.queue_declare(queue='OrderUpdateQueue', exclusive=False)
    queue_name = result.method.queue
    logging.info(f"Notification Service 2 connected to RabbitMQ. Queue: {queue_name}")
    channel.queue_bind(exchange='TopicExchange', queue=queue_name, routing_key='order.update')  # Bind to topic exchange

    def callback(ch, method, properties, body):
        logging.info(f"Notification Service 2 received: {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    logging.info("Notification Service 2 waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()

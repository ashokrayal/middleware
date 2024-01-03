# notification_service_1.py

import pika

def consume_events():
    # Implement Rabbit MQ event consumption logic for order creation
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='orders', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='orders', queue=queue_name)

    def callback(ch, method, properties, body):
        print(f"Notification Service 1 received: {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Notification Service 1 waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()

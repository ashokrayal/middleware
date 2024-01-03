# notification_service_2.py

import pika

def consume_events():
    # Implement Rabbit MQ event consumption logic for order creation and updating
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='orders', exchange_type='topic')
    result = channel.queue_declare(queue='inventory_updates', exclusive=True)
    queue_name = result.method.queue
    print(queue_name)
    channel.queue_bind(exchange='orders', queue=queue_name, routing_key='order.updated')

    def callback(ch, method, properties, body):
        print(f"Notification Service 2 received: {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Notification Service 2 waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()

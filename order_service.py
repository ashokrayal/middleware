# order_service.py
import grpc
from concurrent import futures
import orders_pb2
import orders_pb2_grpc
import logging
import pika  # Import RabbitMQ library

class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.rabbitmq_channel = self.setup_rabbitmq()
        logging.info("Order Service initialized")

    def setup_rabbitmq(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='order_status_updates')  # Declare RabbitMQ queue
        return channel

    def send_message_to_rabbitmq(self, queue_name, message):
        self.rabbitmq_channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    def PlaceOrder(self, request, context):
        order_id = request.order_id

        logging.info(f"Received gRPC request: PlaceOrder - Order ID: {order_id}")

        # Dummy logic: Process the order
        # In a real system, this would involve more complex logic, like order validation, payment processing, etc.
        response = orders_pb2.OrderResponse(message=f"Order {order_id} placed successfully. Order processing initiated.")

        # Publish message to RabbitMQ
        self.send_message_to_rabbitmq('order_status_updates', f"Order placed: {order_id}")

        return response

    def UpdateOrder(self, request, context):
        order_id = request.order_id

        logging.info(f"Received gRPC request: UpdateOrder - Order ID: {order_id}")

        # Dummy logic: Check if the order exists
        # In a real system, this would involve querying a database.
        if order_id.startswith("ORDER"):
            # Dummy logic: Update the order status
            # In a real system, this would involve more complex logic, like updating a database.
            response = orders_pb2.OrderResponse(message=f"Order {order_id} updated successfully. Order status changed.")

            # Publish message to RabbitMQ
            self.send_message_to_rabbitmq('order_status_updates', f"Order updated: {order_id}")
        else:
            response = orders_pb2.OrderResponse(message=f"Error: Order {order_id} not found.")

        return response

def serve():
    logging.basicConfig(level=logging.INFO)  # Added logging configuration
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Order Service started and waiting for requests...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

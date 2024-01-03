# order_service.py
import grpc
from concurrent import futures
import orders_pb2
import orders_pb2_grpc
import logging
import pika
import json

class OrderService(orders_pb2_grpc.OrderServiceServicer):
    """Order service for handling order-related operations.

    Attributes:
        order_counter (int): Class variable to keep track of the order counter.

    """

    order_counter = 1  # Class variable to keep track of the order counter

    def __init__(self):
        """Initialize the OrderService."""
        self.rabbitmq_channel_fanout = self.setup_rabbitmq_fanout()
        self.rabbitmq_channel_topic = self.setup_rabbitmq_topic()
        self.inventory = self.load_inventory()
        logging.info("Order Service initialized")

    def setup_rabbitmq_fanout(self):
        """Set up RabbitMQ connection for fanout exchange."""
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='FanoutExchange', exchange_type='fanout')  # Fanout exchange for broadcasting events
        return channel

    def setup_rabbitmq_topic(self):
        """Set up RabbitMQ connection for topic exchange."""
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='TopicExchange', exchange_type='topic')  # Topic exchange for selective events
        return channel

    def send_message_to_rabbitmq_fanout(self, message):
        """Send message to RabbitMQ fanout exchange."""
        self.rabbitmq_channel_fanout.basic_publish(exchange='FanoutExchange', routing_key='', body=message)

    def send_message_to_rabbitmq_topic(self, message):
        """Send message to RabbitMQ topic exchange."""
        self.rabbitmq_channel_topic.basic_publish(exchange='TopicExchange', routing_key='order.update', body=message)

    def load_inventory(self):
        """Load inventory data from JSON file."""
        with open('inventory.json', 'r') as file:
            inventory_data = json.load(file)
        return inventory_data

    def update_inventory(self, product_id, quantity):
        """Update inventory after placing or updating an order."""
        for product in self.inventory:
            if product['id'] == product_id:
                product['quantity'] -= quantity
                break

    def PlaceOrder(self, request, context):
        """Place an order.

        Args:
            request: The gRPC request containing product_id and quantity.
            context: The gRPC context.

        Returns:
            OrderResponse: The gRPC response containing the order placement status and order ID.
        """
        product_id = request.product_id
        quantity = request.quantity

        logging.info(f"Received gRPC request: PlaceOrder - Product ID: {product_id}, Quantity: {quantity}")

        product_found = False
        for product in self.inventory:
            if product['id'] == product_id and product['quantity'] >= quantity:
                product_found = True
                break

        if product_found:
            order_id = f"ORDER{OrderService.order_counter}"  # Use the class variable for the order counter
            OrderService.order_counter += 1  # Increment the order counter

            response = orders_pb2.OrderResponse(
                message=f"Order placed successfully for product {product_id} with quantity {quantity}. Order ID: {order_id}. Order processing initiated."
            )

            # Update inventory
            self.update_inventory(product_id, quantity)

            # Publish message to RabbitMQ (fanout exchange)
            self.send_message_to_rabbitmq_fanout(f"Order placed: Order ID: {order_id}, Product ID: {product_id}, Quantity: {quantity}")

            logging.info(f"Order Service response: {response}")
        else:
            response = orders_pb2.OrderResponse(
                message=f"Error: Product {product_id} not available in sufficient quantity."
            )

            logging.info(f"Order Service response: {response}")

        return response

    def UpdateOrder(self, request, context):
        """Update an existing order.

        Args:
            request: The gRPC request containing order_id, product_id, and quantity.
            context: The gRPC context.

        Returns:
            OrderResponse: The gRPC response containing the order update status.
        """
        order_id = request.order_id
        product_id = request.product_id
        quantity = request.quantity

        logging.info(
            f"Received gRPC request: UpdateOrder - Order ID: {order_id}, Product ID: {product_id}, Quantity: {quantity}"
        )

        product_found = False
        for product in self.inventory:
            if product['id'] == product_id and product['quantity'] >= quantity:
                product_found = True
                break

        if product_found:
            response = orders_pb2.OrderResponse(
                message=f"Order {order_id} updated successfully. Order status changed."
            )

            # Update inventory
            self.update_inventory(product_id, quantity)

            # Publish message to RabbitMQ (topic exchange)
            self.send_message_to_rabbitmq_topic(f"Order updated: Order ID: {order_id}, Product ID: {product_id}, Quantity: {quantity}")

            logging.info(f"Order Service response: {response}")
        else:
            response = orders_pb2.OrderResponse(
                message=f"Error: Product {product_id} not available in sufficient quantity for updating order {order_id}."
            )

            logging.info(f"Order Service response: {response}")

        return response

def serve():
    """Start the gRPC server."""
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Order Service started and waiting for requests...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

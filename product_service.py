# Import necessary libraries
import grpc
from concurrent import futures
import json
import products_pb2
import products_pb2_grpc
import logging
import pika

# Import the generated gRPC order service module
import orders_pb2
import orders_pb2_grpc

class ProductService(products_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.rabbitmq_channel = self.setup_rabbitmq()
        self.inventory = self.load_inventory()
        self.order_counter = 1
        logging.info("Product Service initialized")

    def setup_rabbitmq(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='order_updates_fanout', exchange_type='fanout')
        return channel

    def send_message_to_rabbitmq(self, exchange_name, message):
        self.rabbitmq_channel.basic_publish(exchange=exchange_name, routing_key='', body=message)

    def load_inventory(self):
        with open('inventory.json', 'r') as file:
            inventory_data = json.load(file)
        return inventory_data

    def update_inventory(self, product_id, quantity):
        for product in self.inventory:
            if product['id'] == product_id:
                product['quantity'] -= quantity
                break

    def PlaceOrder(self, request, context):
        product_id = request.product_id
        quantity = request.quantity

        logging.info(f"Received gRPC request: PlaceOrder - Product ID: {product_id}, Quantity: {quantity}")

        product_found = False
        for product in self.inventory:
            if product['id'] == product_id and product['quantity'] >= quantity:
                product_found = True
                break

        if product_found:
            # Call the gRPC method to place an order
            with grpc.insecure_channel('localhost:50052') as order_channel:
                order_stub = orders_pb2_grpc.OrderServiceStub(order_channel)
                order_request = orders_pb2.OrderRequest(product_id=product_id, quantity=quantity)
                order_stub.PlaceOrder(order_request)

            response = products_pb2.OrderResponse(message=f"Order placed successfully for product {product_id} with quantity {quantity}. Inventory updated.")

            # Update inventory
            self.update_inventory(product_id, quantity)

            # Generate order ID and publish message to RabbitMQ
            order_id = f"ORDER{self.order_counter}"
            self.order_counter += 1
            self.send_message_to_rabbitmq('order_updates_fanout', f"Order placed: {order_id}")

            response.order_id = order_id
        else:
            response = products_pb2.OrderResponse(message=f"Error: Product {product_id} not available in sufficient quantity.")

        return response

    def UpdateOrder(self, request, context):
        order_id = request.order_id
        product_id = request.product_id
        quantity = request.quantity

        logging.info(f"Received gRPC request: UpdateOrder - Order ID: {order_id}, Product ID: {product_id}, Quantity: {quantity}")

        product_found = False
        for product in self.inventory:
            if product['id'] == product_id and product['quantity'] >= quantity:
                product_found = True
                break

        if product_found:
            # Call the gRPC method to update an order
            with grpc.insecure_channel('localhost:50052') as order_channel:
                order_stub = orders_pb2_grpc.OrderServiceStub(order_channel)
                order_request = orders_pb2.OrderRequest(order_id=order_id, product_id=product_id, quantity=quantity)
                order_stub.UpdateOrder(order_request)

            response = products_pb2.OrderResponse(message=f"Order {order_id} updated successfully. Order status changed.")

            # Update inventory
            self.update_inventory(product_id, quantity)

            # Publish message to RabbitMQ
            self.send_message_to_rabbitmq('order_updates_fanout', f"Order updated: {order_id}")
        else:
            response = products_pb2.OrderResponse(message=f"Error: Product {product_id} not available in sufficient quantity for updating order.")

        return response

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    products_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Product Service started and waiting for requests...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

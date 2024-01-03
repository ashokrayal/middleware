# product_service.py

import grpc
from concurrent import futures
import json
import logging

import products_pb2
import products_pb2_grpc
import orders_pb2
import orders_pb2_grpc


class ProductService(products_pb2_grpc.ProductServiceServicer):
    """
    gRPC service to handle product-related operations.
    """

    def __init__(self):
        """
        Initialize the Product Service.
        """
        self.inventory = self.load_inventory()
        self.order_counter = 1
        logging.info("Product Service initialized")

    def load_inventory(self):
        """
        Load product inventory from a JSON file.

        Returns:
            list: Product inventory data.
        """
        with open('inventory.json', 'r') as file:
            inventory_data = json.load(file)
        return inventory_data

    def update_inventory(self, product_id, quantity):
        """
        Update product inventory.

        Args:
            product_id (str): ID of the product.
            quantity (int): Quantity to be updated.
        """
        for product in self.inventory:
            if product['id'] == product_id:
                product['quantity'] -= quantity
                break

    def PlaceOrder(self, request, context):
        """
        Handle the PlaceOrder gRPC method.

        Args:
            request (products_pb2.OrderRequest): gRPC request message.
            context (grpc.ServicerContext): gRPC context.

        Returns:
            products_pb2.OrderResponse: gRPC response message.
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
            # Call the gRPC method to place an order
            with grpc.insecure_channel('localhost:50052') as order_channel:
                order_stub = orders_pb2_grpc.OrderServiceStub(order_channel)
                order_request = orders_pb2.OrderRequest(product_id=product_id, quantity=quantity)
                order_response = order_stub.PlaceOrder(order_request)
                logging.info(f"Order Service response: {order_response.message}")

            response = products_pb2.OrderResponse(
                message=order_response.message
            )

            # Update inventory
            self.update_inventory(product_id, quantity)

            # Generate order ID
            order_id = f"ORDER{self.order_counter}"
            self.order_counter += 1
            response.order_id = order_id
        else:
            response = products_pb2.OrderResponse(
                message=f"Error: Product {product_id} not available in sufficient quantity."
            )

        return response

    def UpdateOrder(self, request, context):
        """
        Handle the UpdateOrder gRPC method.

        Args:
            request (products_pb2.OrderRequest): gRPC request message.
            context (grpc.ServicerContext): gRPC context.

        Returns:
            products_pb2.OrderResponse: gRPC response message.
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
            # Call the gRPC method to update an order
            with grpc.insecure_channel('localhost:50052') as order_channel:
                order_stub = orders_pb2_grpc.OrderServiceStub(order_channel)
                order_request = orders_pb2.OrderRequest(
                    order_id=order_id, product_id=product_id, quantity=quantity
                )
                order_response = order_stub.UpdateOrder(order_request)
                logging.info(f"Order Service response: {order_response.message}")

            response = products_pb2.OrderResponse(
                message=f"Order {order_id} updated successfully. Order status changed."
            )

            # Update inventory
            self.update_inventory(product_id, quantity)
        else:
            response = products_pb2.OrderResponse(
                message=f"Error: Product {product_id} not available in sufficient quantity for updating order."
            )

        return response


def serve():
    """
    Start the gRPC server for the Product Service.
    """
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    products_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Product Service started and waiting for requests...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

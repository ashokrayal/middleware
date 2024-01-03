import grpc
from concurrent import futures
import json
import products_pb2
import products_pb2_grpc
import logging  # Added logging module

class ProductService(products_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products = self.load_products()
        logging.info("Product Service initialized")

    def load_products(self):
        # Load products from a JSON file
        with open('products.json', 'r') as file:
            products_data = json.load(file)
        return products_data

    def PlaceOrder(self, request, context):
        product_id = request.product_id
        quantity = request.quantity

        logging.info(f"Received gRPC request: PlaceOrder - Product ID: {product_id}, Quantity: {quantity}")

        # Dummy logic: Check if the product is available in the inventory
        if product_id in [product['id'] for product in self.products]:
            # Dummy logic: Update the inventory (reduce quantity)
            # In a real system, this would involve more complex logic, like updating a database.
            response = products_pb2.OrderResponse(message=f"Order placed successfully for product {product_id} with quantity {quantity}. Inventory updated.")
        else:
            response = products_pb2.OrderResponse(message=f"Error: Product {product_id} not available in the inventory.")

        return response

    def UpdateOrder(self, request, context):
        product_id = request.product_id  # Corrected field name

        logging.info(f"Received gRPC request: UpdateOrder - Product ID: {product_id}")

        # Dummy logic: Check if the order exists
        # In a real system, this would involve querying a database.
        if product_id.startswith("ORDER"):
            # Dummy logic: Update the order status
            # In a real system, this would involve more complex logic, like updating a database.
            response = products_pb2.OrderResponse(message=f"Order updated successfully for product ID: {product_id}")
        else:
            response = products_pb2.OrderResponse(message=f"Error: Product {product_id} not found.")

        return response

def serve():
    logging.basicConfig(level=logging.INFO)  # Added logging configuration
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    products_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Product Service started and waiting for requests...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

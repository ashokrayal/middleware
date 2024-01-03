# product_service.py

import grpc
from concurrent import futures
import json
import products_pb2
import products_pb2_grpc

class ProductService(products_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products = self.load_products()

    def load_products(self):
        # Load products from a JSON file
        with open('products.json', 'r') as file:
            products_data = json.load(file)
        return products_data

    def PlaceOrder(self, request, context):
        # Implement place order logic
        # Call Order Service to place the order using gRPC
        # Update products data
        response = products_pb2.OrderResponse(message="Order placed successfully")
        return response

    def UpdateOrder(self, request, context):
        # Implement update order logic
        # Call Order Service to update the order using gRPC
        # Update products data
        response = products_pb2.OrderResponse(message="Order updated successfully")
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    products_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

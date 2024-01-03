import grpc
from concurrent import futures
import orders_pb2
import orders_pb2_grpc
import logging  # Added logging module

class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def PlaceOrder(self, request, context):
        order_id = request.order_id

        logging.info(f"Received gRPC request: PlaceOrder - Order ID: {order_id}")

        # Dummy logic: Process the order
        # In a real system, this would involve more complex logic, like order validation, payment processing, etc.
        response = orders_pb2.OrderResponse(message=f"Order {order_id} placed successfully. Order processing initiated.")
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

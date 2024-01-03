import grpc
import logging
import products_pb2
import products_pb2_grpc
import orders_pb2
import orders_pb2_grpc

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():
    # Connect to Product Service
    with grpc.insecure_channel('localhost:50051') as channel:
        product_stub = products_pb2_grpc.ProductServiceStub(channel)

        # Place an order
        order_request = products_pb2.OrderRequest(product_id='1', quantity=2)
        order_response = product_stub.PlaceOrder(order_request)
        logger.info("Product Service Response: %s", order_response.message)

        # Update an order (use the correct field name)
        update_request = products_pb2.OrderRequest(product_id='ORDER123')  # Corrected field name
        update_response = product_stub.UpdateOrder(update_request)
        logger.info("Product Service Response: %s", update_response.message)

    # Connect to Order Service
    with grpc.insecure_channel('localhost:50052') as channel:
        order_stub = orders_pb2_grpc.OrderServiceStub(channel)

        # Place an order
        place_order_request = orders_pb2.OrderRequest(order_id='ORDER456')
        place_order_response = order_stub.PlaceOrder(place_order_request)
        logger.info("Order Service Response: %s", place_order_response.message)

        # Update an order
        update_order_request = orders_pb2.OrderRequest(order_id='ORDER789')
        update_order_response = order_stub.UpdateOrder(update_order_request)
        logger.info("Order Service Response: %s", update_order_response.message)

if __name__ == '__main__':
    run()

# grpc_client.py
import grpc
import logging
import products_pb2
import products_pb2_grpc

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():
    """Run gRPC client to interact with the Product Service.

    Connects to the Product Service using gRPC, performs PlaceOrder and UpdateOrder operations,
    and logs the responses.

    Raises:
        grpc.RpcError: If an error occurs during gRPC communication.

    Returns:
        None
    """
    # Connect to Product Service
    with grpc.insecure_channel('localhost:50051') as product_channel:
        product_stub = products_pb2_grpc.ProductServiceStub(product_channel)

        # Place an order with a static order ID
        place_order_request = products_pb2.OrderRequest(product_id='1', quantity=2)
        place_order_response = product_stub.PlaceOrder(place_order_request)
        logger.info("Product Service Response (Place Order): %s", place_order_response.message)
        
        # Update an order within the Product Service using a static order ID
        update_request = products_pb2.OrderRequest(order_id='1', product_id='1', quantity=1)  # Use order_id
        update_response = product_stub.UpdateOrder(update_request)
        logger.info("Product Service Response (Update Order): %s", update_response.message)

if __name__ == '__main__':
    run()

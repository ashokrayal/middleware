# order_service.py

import grpc
from concurrent import futures
import orders_pb2
import orders_pb2_grpc
import pika

class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def PlaceOrder(self, request, context):
        # Implement place order logic
        # Publish events for order creation using Rabbit MQ fanout exchange
        self.publish_event('order.created', request.order_id)
        response = orders_pb2.OrderResponse(message="Order placed successfully")
        return response

    def UpdateOrder(self, request, context):
        # Implement update order logic
        # Publish events for order updating using Rabbit MQ topic exchange
        self.publish_event('order.updated', request.order_id)
        response = orders_pb2.OrderResponse(message="Order updated successfully")
        return response

    def publish_event(self, event_type, order_id):
        # Implement Rabbit MQ event publishing logic
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='orders', exchange_type='fanout')
        channel.basic_publish(exchange='orders', routing_key='', body=f'{event_type} - {order_id}')
        connection.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

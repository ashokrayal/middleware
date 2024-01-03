# Overview

## Problem Statement

The project addresses the challenge of designing and implementing a system for managing orders, products, and notifications in a distributed environment. The key aspects of the problem statement include:

1. **Product Service:**
    - Responsible for managing products and inventory.
    - Exposes gRPC endpoints to facilitate placing and updating orders.

2. **Order Service:**
    - Processes order-related requests received from the Product Service.
    - Generates order events and publishes them to RabbitMQ using both fanout and topic exchanges.

3. **Notification Services:**
    - Notification Service 1:
        - Listens for order creation events broadcasted on the fanout exchange.
        - Connects to RabbitMQ to consume these events and logs them.
    - Notification Service 2:
        - Listens for both order creation and update events based on a topic exchange.
        - Connects to RabbitMQ to consume these events and logs them.

The problem is focused on building a reliable, scalable, and asynchronous system that ensures seamless communication between services, real-time updates, and proper handling of events.

## Solution

The solution involves creating three main components:

1. **Product Service:**
    - Manages products and inventory.
    - Utilizes gRPC for communication with other services.
    - Publishes order events to RabbitMQ.

2. **Order Service:**
    - Processes order-related requests from the Product Service.
    - Publishes order events to RabbitMQ using fanout and topic exchanges.

3. **Notification Services:**
    - Notification Service 1:
        - Listens for order creation events on the fanout exchange.
        - Consumes events from RabbitMQ and logs them.
    - Notification Service 2:
        - Listens for both order creation and update events on the topic exchange.
        - Consumes events from RabbitMQ and logs them.

The solution leverages gRPC for communication efficiency and RabbitMQ for distributed event-driven architecture.

# Prerequisites

**Python Installation:**
Ensure that Python 3 is installed on your system.


**RabbitMQ Installation:**
Install RabbitMQ following the official installation guide: [RabbitMQ Installation Guide](https://www.rabbitmq.com/download.html)

**Git Setup**

Clone the repository containing your solution:

```bash
git clone <repository_url>
cd <repository_folder>

Install the required Python dependencies:
pip install -r requirements.txt

Start the RabbitMQ server.

Usage
To use the system, follow these steps:

Start Product Service:
python product_service.py

Start Order Service:
python order_service.py

Start Notification Service 1:
python notification_service_1.py

Start Notification Service 2:
python notification_service_2.py

Run gRPC Client:
python grpc_client.py


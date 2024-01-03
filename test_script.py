import subprocess
import time
import threading

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()

def run_order_service():
    run_command("python order_service.py")

def run_notification_service_1():
    run_command("python notification_service_1.py")

def run_notification_service_2():
    run_command("python notification_service_2.py")

def run_product_service():
    run_command("python product_service.py")

def test_system():
    # Start each service in a separate thread
    order_service_thread = threading.Thread(target=run_order_service)
    notification_service_1_thread = threading.Thread(target=run_notification_service_1)
    notification_service_2_thread = threading.Thread(target=run_notification_service_2)
    product_service_thread = threading.Thread(target=run_product_service)

    order_service_thread.start()
    notification_service_1_thread.start()
    notification_service_2_thread.start()

    # Sleep for a while to allow services to start
    time.sleep(5)

    product_service_thread.start()

    # Wait for all threads to finish
    order_service_thread.join()
    notification_service_1_thread.join()
    notification_service_2_thread.join()
    product_service_thread.join()

if __name__ == "__main__":
    test_system()

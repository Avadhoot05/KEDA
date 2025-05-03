from flask import Flask, request, jsonify, json
import pika
import time
import os

LOG_FILE = "../consumed_messages.log"

app = Flask(__name__)

@app.route('/orders', methods=['POST'])
def createOrder():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',   # Kubernetes service name or IP
    port=5672,                 # Default RabbitMQ port
    virtual_host='/',          # Default virtual host
    credentials=pika.PlainCredentials('guest', 'guest')))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    orderData = request.get_json()
    if not orderData:
        return jsonify({'error': 'No data provided'}), 400

    # Log the received data
    print("Received Order:", orderData)
    orderId = orderData.get('orderId')
    productName = orderData.get('productName')
    quantity = orderData.get('quantity')
    price = orderData.get('price')

    message = json.dumps({
        'message': 'Order received',
        'order': {
            'orderId': orderId,
            'productName': productName,
            'quantity': quantity,
            'price': price
        }
    })

    # message = "Hello from Producer!"
    channel.basic_publish(exchange='', routing_key='order_queue', body=message.encode())
    print("Sent:", message)
    time.sleep(2)

    return jsonify('POSTED'), 200

@app.route('/', methods=['GET'])
def homePage():

    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',   # Kubernetes service name or IP
    # port=5672,                 # Default RabbitMQ port
    # virtual_host='/',          # Default virtual host
    # credentials=pika.PlainCredentials('guest', 'guest')))
    # channel = connection.channel()
    # channel.queue_declare(queue='order_queue')

    # # method_frame, header_frame, body = channel.basic_get(queue='order_queue', auto_ack=True)

    # messages = []

    # while True:
    #     method_frame, header_frame, body = channel.basic_get(queue='order_queue', auto_ack=True)
    #     if method_frame:
    #         # decode and parse each message
    #         msg = json.loads(body.decode())
    #         messages.append(msg)
    #     else:
    #         break  # No more messages in queue
    # connection.close()

    # return {"received": messages}, 200

    # orders = []

    # def callback(ch, method, properties, body):
    #     orders.append(body)

    # channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)
    # print("Waiting for messages...")
    # channel.start_consuming()
    
    # return jsonify(orders), 200

    if not os.path.exists(LOG_FILE):
        return jsonify({"orders": [], "status": "Log file not found"}), 200

    orders = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                timestamped_data = line.strip().split(" - ", 1)
                if len(timestamped_data) == 2:
                    _, json_str = timestamped_data
                    order = json.loads(json_str)
                    orders.append(order)
            except Exception as e:
                print(f"Error parsing line: {line}\n{e}")
                continue

    return jsonify({"orders": orders, "count": len(orders)}), 200

if __name__ == '__main__':
    app.run(debug=True)

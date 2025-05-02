from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/orders', methods=['POST'])
def createOrder():
    orderData = request.get_json()
    if not orderData:
        return jsonify({'error': 'No data provided'}), 400

    # Log the received data
    print("Received Order:", orderData)
    orderId = orderData.get('orderId')
    productName = orderData.get('productName')
    quantity = orderData.get('quantity')
    price = orderData.get('price')

    return jsonify({
        'message': 'Order received',
        'order': {
            'orderId': orderId,
            'productName': productName,
            'quantity': quantity,
            'price': price
        }
    }), 200

@app.route('/', methods=['GET'])
def homePage():
    return jsonify({
            'message': 'This is Home page',
        }), 200

if __name__ == '__main__':
    app.run(debug=True)

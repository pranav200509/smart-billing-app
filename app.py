from flask import Flask, render_template, request, redirect, url_for, session
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'secret_key'  


def generate_qr_code_base64(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64

@app.route('/')
def index():
    products = [
        {"id": 1, "name": "Apple", "price": 25},
        {"id": 2, "name": "Banana", "price": 10},
        {"id": 3, "name": "Orange", "price": 20},
        {"id": 4, "name": "Grapes", "price": 30},
        {"id": 5, "name": "Pineapple", "price": 50},
        {"id": 6, "name": "Mango", "price": 40},
        {"id": 7, "name": "Strawberry", "price": 35},
        {"id": 8, "name": "Watermelon", "price": 60},
        {"id": 9, "name": "Peach", "price": 25},
        {"id": 10, "name": "Kiwi", "price": 28},
        {"id": 11, "name": "Blueberry", "price": 45},
        {"id": 12, "name": "Dragon Fruit", "price": 90},
        {"id": 13, "name": "Raspberry", "price": 38},
        {"id": 14, "name": "Blackberry", "price": 42},
        {"id": 15, "name": "Potato", "price": 12},
        {"id": 16, "name": "Ladies Finger", "price": 18},
        {"id": 17, "name": "Cucumber", "price": 25},
        {"id": 18, "name": "Tomato", "price": 30},
        {"id": 19, "name": "Green Chilli", "price": 15},
        {"id": 20, "name": "Carrot", "price": 20}





    ]
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form.get('product_name')
    quantity = int(request.form.get('quantity'))
    price_per_unit = float(request.form.get('price_per_unit'))
    total_price = quantity * price_per_unit

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({
        'product_name': product_name,
        'quantity': quantity,
        'price_per_unit': price_per_unit,
        'total_price': total_price
    })
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total_amount = sum(item['total_price'] for item in cart)
    return render_template('cart.html', cart=cart, total_amount=total_amount)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)  
    return redirect(url_for('view_cart'))  

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('index'))

    total_amount = sum(item['total_price'] for item in cart)
    qr_data = f"Total Amount: ${total_amount:.2f}"
    qr_code_base64 = generate_qr_code_base64(qr_data)

    session.pop('cart', None)

    return render_template('receipt.html', total_amount=total_amount, qr_code_base64=qr_code_base64)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель для хранения заказов
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.id}>'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('base.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/orderfound')
def contact():
    return render_template('order.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        quantity = request.form['quantity']

        new_order = Order(name=name, phone=phone, address=address, quantity=quantity)
        
        try:
            db.session.add(new_order)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка при добавлении заказа'
    
    return render_template('order.html')

@app.route('/admin')
def admin():
    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


    
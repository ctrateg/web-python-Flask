from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# БД - Таблица - Записи
# ТАблица:
# id  title  price   isActive
# 1   Some   100     True
# 2   Some2  200     False
# 3   Some3  49      True
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    #text = db.Column(db.Text, nullable=False)

    def __repr__(self):
         return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all() #text
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')\


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str (item.price) + "00" #text)
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        #text = request.form['text']
        price = request.form['price']

        item = Item(title=title, price=price) #text=text)

        try:
            db.session.add(Item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилось ошибка"
    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
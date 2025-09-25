from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)  
app.secret_key = "supersecretkey"  

# Подключение к базе
connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()

# Получить список товаров
def get_products():
    cursor.execute("SELECT id, name, description, price, image_link FROM product")
    return cursor.fetchall()

# Получить один товар
def get_product(product_id):
    cursor.execute("SELECT id, name, description, price, image_link FROM product WHERE id = ?", (product_id,))
    return cursor.fetchone()

# Главная (с баннером и товарами)
@app.route("/")
def index():
    shop = get_products()
    return render_template("index.html", shop=shop, title="Главная")

# Страница карточки товара
@app.route("/product/<int:product_id>")
def product_page(product_id):
    product = get_product(product_id)
    if product:
        product_data = {
            "id": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "image": product[4] if product[4] else "product1.jpg"
        }
        return render_template("product.html", product=product_data, title=product_data["name"])
    else:
        return "Товар не найден", 404
    
# Добавить товар в корзину
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])
    if product_id not in cart:
        cart.append(product_id)
    session["cart"] = cart
    return redirect(url_for("cart"))

# Убрать товар из корзины
@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    if product_id in cart:
        cart.remove(product_id)
    session["cart"] = cart
    return redirect(url_for("cart"))

# Добавить товар в избранные
@app.route("/add_to_favorites/<int:product_id>")
def add_to_favorites(product_id):
    favorites = session.get("favorites", [])
    if product_id not in favorites:
        favorites.append(product_id)
    session["favorites"] = favorites
    return redirect(url_for("favorites"))

# Убрать товар из избранных
@app.route("/remove_from_favorites/<int:product_id>")
def remove_from_favorites(product_id):
    favorites = session.get("favorites", [])
    if product_id in favorites:
        favorites.remove(product_id)
    session["favorites"] = favorites
    return redirect(url_for("favorites"))

# Поиск
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("q")  # забираем параметр из строки запроса
    products = []

    if query:
        cursor.execute(
            "SELECT id, name, description, price, image_link FROM product WHERE name LIKE ? OR description LIKE ?",
            (f"%{query}%", f"%{query}%")
        )
        products = cursor.fetchall()

    return render_template("search.html", products=products, query=query, title="Поиск")

# Бренды
@app.route("/brands")
def brands():
    return render_template("brands.html", title="Бренды", page_label="Список брендов" )

# Коллекция 1 (продукты 1 и 2)
@app.route("/brands/collection1")
def brands_collection1():
    cursor.execute("SELECT id, name, description, price, image_link FROM product WHERE id IN (1,2)")
    products = cursor.fetchall()
    return render_template(
        "brands_collection.html",
        products=products,
        title="Коллекция 1",
        banner_image="banner1.jpg"
    )

@app.route("/brands/collection2")
def brands_collection2():
    cursor.execute("SELECT id, name, description, price, image_link FROM product WHERE id IN (3,4)")
    products = cursor.fetchall()
    return render_template(
        "brands_collection.html",
        products=products,
        title="Коллекция 2",
        banner_image="banner2.jpg"
    )


# Меню
@app.route("/menu")
def menu():
    return render_template("menu.html", title="Меню", page_label="Меню", links=[
        {"url": "/login", "label": "Вход/Регистрация", "icon": "login-icon.png" },
        {"url": "https://t.me/+euCjSbjLR_AxZDJi", "label": "телеграм", "icon": "telegram.png"},
        {"url": "https://www.forbes.ru/svoi-biznes/544859-zapret-reklamy-v-instagram-s-1-sentabra-cto-mozno-i-nel-za-publikovat", "label": "инстаграм", "icon": "instagram.png"},
        {"url": "/brands", "label": "Список брендов", "icon": "brands-icon.png"},
        {"url": "/about/history", "label": "История бренда","icon": "history-icon.png"},
        {"url": "/store-reviews", "label": "Отзывы о магазине", "icon": "reviews-icon.png"},
        {"url": "/favorites", "label": "Избранные", "icon": "favorites-icon.png"},
    ])

# Корзина
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    products = []
    for product_id in cart_items:
        product = get_product(product_id)
        if product:
            products.append(product)
    return render_template("cart.html", products=products, title="Корзина")

# Избранные
@app.route("/favorites")
def favorites():
    fav_items = session.get("favorites", [])
    products = []
    for product_id in fav_items:
        product = get_product(product_id)
        if product:
            products.append(product)
    return render_template("favorites.html", products=products, title="Избранные")


# О нас
@app.route("/about")
def about():
    return render_template("about.html", title="О нас", page_label="О нас")

# История
@app.route("/about/history")
def history():
    return render_template("page.html", title="История", page_label="История бренда", text="ну очень грустная история")

# Отзывы
@app.route("/store-reviews")
def reviews():
    return render_template("page.html", title="Отзывы", page_label="Отзывы", text="чотко")

#оформление заказа
@app.route("/checkout")
def checkout():
    cart_items = session.get("cart", [])
    products = []
    for product_id in cart_items:
        product = get_product(product_id)
        if product:
            products.append(product)

    return render_template("checkout.html", products=products, title="Оформление заказа")
from flask import Flask, render_template, request, redirect, url_for, session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Обработка входа
        email = request.form.get('email')
        password = request.form.get('password')
        # Здесь проверка логина/пароля
        session['user'] = email
        return redirect(url_for('menu'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Обработка регистрации
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # Здесь сохранение пользователя
        session['user'] = email
        return redirect(url_for('menu'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
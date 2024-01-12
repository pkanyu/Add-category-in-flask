from flask import *
import pymysql

app = Flask(__name__,static_url_path='/static')

# MySQL configuration
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="Testing"
)

@app.route('/')
def home():
    return render_template('admin_form.html')

# Route for admin to add a product category
@app.route('/admin/add_category', methods=['GET', 'POST'])
def admin_add_category():
    if request.method == 'POST':
        category = request.form['category']
        cursor = db.cursor()
        cursor.execute("INSERT INTO categories (category_name) VALUES (%s)", (category,))
        db.commit()
    return render_template('admin_form.html')

# Route for vendors to add a product
@app.route('/vendor/add_product', methods=['GET', 'POST'])
def vendor_add_product():
    cursor = db.cursor()
    cursor.execute("SELECT category_name FROM categories")
    categories = [row[0] for row in cursor.fetchall()]
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        chosen_category = request.form['category']
        cursor.execute("INSERT INTO products (product_name, product_category) VALUES (%s, %s)", (product_name, chosen_category))
        db.commit()
    
    return render_template('add_products.html', categories=categories)

# Route for users to view products
@app.route('/products')
def view_products():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('view_products.html', products=products)

@app.route('/admin/edit_category/<category_id>', methods=['GET', 'POST'])
def admin_edit_category(category_id):
    cursor = db.cursor()
    cursor.execute("SELECT category_id, category_name FROM categories WHERE category_id = %s", (category_id,))
    category = cursor.fetchone()

    if request.method == 'POST':
        new_name = request.form['new_name']
        cursor.execute("UPDATE categories SET category_name = %s WHERE category_id = %s", (new_name, category_id))
        db.commit()
    
    return render_template('/edit_category.html',category = category)

@app.route('/admin/delete_category/<category_id>', methods=['POST'])
def admin_delete_category(category_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    db.commit()
    return redirect('/admin/add_category')
























if __name__ == '__main__':
    app.run(debug=True)
 

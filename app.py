from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, default=0)
    num_sold = db.Column(db.Integer, default=0)
    sales = db.Column(db.Float, default=0.0)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@app.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        product = Product(
            product_id=request.form.get('product_id'),
            name=request.form.get('name'),
            quantity=int(request.form.get('quantity')),
            price=float(request.form.get('price')),
            discount=int(request.form.get('discount'))
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('products'))
    return render_template('add_product.html')

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        product = Product.query.get_or_404(id)
        if request.method == 'POST':
            try:
                product.product_id = request.form.get('product_id')
                product.name = request.form.get('name')
                product.quantity = int(request.form.get('quantity'))
                product.price = float(request.form.get('price'))
                product.discount = int(request.form.get('discount', 0))
                db.session.commit()
                flash('Product updated successfully!', 'success')
                return redirect(url_for('products'))
            except ValueError as e:
                flash(f'Invalid input: {str(e)}', 'danger')
                return redirect(url_for('edit_product', id=id))
            except Exception as e:
                flash(f'Error updating product: {str(e)}', 'danger')
                return redirect(url_for('edit_product', id=id))
        
        return render_template('edit_product.html', product=product)
    except Exception as e:
        flash(f'Error loading product: {str(e)}', 'danger')
        return redirect(url_for('products'))

@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
        
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('products'))

@app.route('/purchase/<int:id>', methods=['POST'])
@login_required
def purchase(id):
    product = Product.query.get_or_404(id)
    quantity = int(request.form.get('quantity'))
    
    if product.quantity < quantity:
        flash('Not enough stock available!')
        return redirect(url_for('products'))
        
    product.quantity -= quantity
    product.num_sold += quantity
    product.sales += quantity * product.price * (1 - product.discount / 100.0)
    db.session.commit()
    flash('Purchase successful!')
    return redirect(url_for('products'))

@app.route('/sales_report')
@login_required
def sales_report():
    products = Product.query.all()
    return render_template('sales_report.html', products=products)

@app.route('/employees')
@login_required
def employees():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
    users = User.query.filter(User.is_admin == False).all()
    return render_template('employees.html', users=users)

@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('add_employee'))
            
        new_employee = User(
            username=username,
            password_hash=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!')
        return redirect(url_for('employees'))
        
    return render_template('add_employee.html')

@app.route('/delete_employee/<int:id>')
@login_required
def delete_employee(id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
        
    employee = User.query.get_or_404(id)
    if employee.is_admin:
        flash('Cannot delete admin user!')
        return redirect(url_for('employees'))
        
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!')
    return redirect(url_for('employees'))

@app.route('/inventory_report')
@login_required
def inventory_report():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
        
    products = Product.query.all()
    return render_template('inventory_report.html', products=products)

# API Routes
@app.route('/api/products')
@login_required
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'product_id': p.product_id,
        'name': p.name,
        'quantity': p.quantity,
        'price': p.price,
        'discount': p.discount,
        'num_sold': p.num_sold,
        'sales': p.sales
    } for p in products])

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True) 
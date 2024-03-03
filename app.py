from flask import Flask, abort, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from forms import LoginForm, RegistrationForm, TransactionForm
from models import db, User, Transaction, Category
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '123654Ss#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf = CSRFProtect(app)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/transactions')
@login_required
def transactions():
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions.html', transactions=user_transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        # Handling category as text input
        category_name = form.category.data
        category = Category.query.filter_by(name=category_name, user_id=current_user.id).first()
        if not category:
            category = Category(name=category_name, user_id=current_user.id)
            db.session.add(category)
            db.session.commit()

        transaction = Transaction(type=form.type.data, amount=form.amount.data,
                                  date=form.date.data, description=form.description.data,
                                  category_id=category.id, user_id=current_user.id)
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions'))
    return render_template('add_transaction.html', title='Add New Transaction', form=form)


# Placeholder for edit and delete transaction routes

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        abort(403)  # Forbidden access if the current user doesn't own the transaction
    form = TransactionForm(obj=transaction)  # Pre-populate form with transaction data
    if form.validate_on_submit():
        transaction.type = form.type.data
        transaction.amount = form.amount.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        transaction.category = form.category.data  # Assuming you handle category as a string
        # Update the category handling here as per your application logic
        db.session.commit()
        flash('Transaction has been updated.', 'success')
        return redirect(url_for('transactions'))
    elif request.method == 'GET':
        # Pre-fill the form fields
        form.type.data = transaction.type
        form.amount.data = transaction.amount
        form.date.data = transaction.date
        form.description.data = transaction.description
        form.category.data = transaction.category.name  # Adjust based on your model relationships
    return render_template('edit_transaction.html', title='Edit Transaction', form=form, transaction_id=transaction_id)


from flask import request

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        abort(403)  # Forbidden access if the current user doesn't own the transaction
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction has been deleted.', 'success')
    return redirect(url_for('transactions'))

from sqlalchemy import func

@app.route('/financial_reports')
@login_required
def financial_reports():
    # Aggregate income vs. expenses
    income_expense_summary = db.session.query(
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).filter(Transaction.user_id == current_user.id).group_by(Transaction.type).all()

    income_expense_data = {'Income': 0, 'Expense': 0}
    for item in income_expense_summary:
        income_expense_data[item.type] = item.total

    # Aggregate spending by category for expenses only
    category_spending_summary = db.session.query(
        Category.name,
        func.sum(Transaction.amount).label('total')
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id, 
        Transaction.type == 'Expense'
    ).group_by(Category.name).all()

    category_names = [item.name for item in category_spending_summary]
    category_totals = [float(item.total) for item in category_spending_summary]

    return render_template('financial_reports.html', 
                           income_expense_data=income_expense_data, 
                           category_names=category_names, 
                           category_totals=category_totals)



# Make sure to implement these based on your application's needs

if __name__ == '__main__':
    app.run(debug=True)

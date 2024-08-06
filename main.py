from flask import Flask, request, redirect, render_template
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from db import connect_db, create_tables

app = Flask(__name__)

# Initialize the database
create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    date = request.form['date']
    description = request.form['description']
    category = request.form['category']
    amount = float(request.form['amount'])
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)',
                   (date, description, category, amount))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/view_expenses')
def view_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return render_template('view_expenses.html', expenses=expenses)

@app.route('/visualize_expenses')
def visualize_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()
    conn.close()
    
    categories, amounts = zip(*data)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(categories), y=list(amounts))
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.title('Expense by Category')
    plt.savefig('static/expenses.png')
    return redirect('/static/expenses.png')

if __name__ == '__main__':
    app.run(debug=True)

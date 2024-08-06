import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

def generate_expense_report():
    conn = sqlite3.connect('budget.db')
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

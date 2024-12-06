from flask import Flask, render_template,request,redirect
from sqlalchemy import create_engine,Column,Integer, String, Float,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

Base = declarative_base()
engine = create_engine('sqlite:///expenses.db')
Session = sessionmaker(bind=engine)
session = Session() 

class Expense(Base):
    __tablename__= 'expenses'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    expenses = session.query(Expense).all()
    
    # Calculate the total expenses (sum of the amounts)
    total_expenses = sum(expense.amount for expense in expenses)
    
    return render_template('index.html', expenses=expenses, total_expenses=total_expenses)



from datetime import datetime

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Extract data from the form
        date_str = request.form['date']  # This is a string, e.g., '2024-12-06'
        category = request.form['category']
        amount = request.form['amount']

        # Convert the date string to a Python date object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Create a new expense
        new_expense = Expense(date=date, category=category, amount=float(amount))
        session.add(new_expense)
        session.commit()

        return redirect('/')  # Redirect to the homepage

    # Render the form for adding a new expense
    return render_template('createAddForm.html')


if __name__ == '__main__':
    app.run(debug=True)


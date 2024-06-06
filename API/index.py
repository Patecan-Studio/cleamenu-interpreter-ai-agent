from flask import Flask, jsonify, request

from API.model.expense import Expense, ExpenseSchema
from API.model.income import Income, IncomeSchema
from API.model.transaction_type import TransactionType
from API.model.message_event import MessageEvent, MessageEventSchema
from ai_agent.agent import cleamenu_agent

app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]


@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes)


@app.route('/stores/<string:storeId>', methods=['POST'])
def message_event(storeId):
    print(request.get_json())
    message = MessageEventSchema().load(request.get_json())
    prompt = (f"The Store Id: {storeId}, only use items in this store \n"
              f"The request from User is: {message}")

    response_from_agent = cleamenu_agent({"input": prompt})
    return response_from_agent, 204

@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return "", 204

@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses)


@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return "", 204


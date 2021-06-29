from flask import Blueprint, request, jsonify, json
from flask_login import login_required, current_user
from icecream import ic

from app.models import User, Transaction
from . import db

views = Blueprint("views", __name__)


@views.route('/')
@login_required
def home():
    balance = current_user.balance
    return {'Balance': balance}


@views.route('/send', methods=['POST'])
def send():
    data = request.json
    receiver_id, amount = data.get('receiver_id'), data.get("amount")

    recipient = User.query.filter_by(id=receiver_id).first_or_404("Invalid Recipient")

    sender = User.query.get(current_user.id)

    if amount is None or amount > sender.balance:
        return jsonify("Invalid amount")

    recipient.balance += amount
    sender.balance -= amount
    current_user.balance -= amount

    transaction = {"sender_id": sender.id, "receiver_id": receiver_id, "amount": amount, }
    new_transaction = Transaction(**transaction)

    db.session.add(new_transaction)
    db.session.commit()
    return jsonify("Transaction Successful")


@views.route('/transactions')
@login_required
def transactions():
    id = current_user.id
    __transactions__ = Transaction.query.filter((Transaction.receiver_id == id) | (Transaction.sender_id == id)).all()
    _transactions_ = [i.repr for i in __transactions__]
    ic(_transactions_)
    return json.dumps(_transactions_)

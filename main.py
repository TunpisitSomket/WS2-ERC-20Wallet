from bank.chain import ChainAPI
from flask import Flask, render_template, request


chain = ChainAPI()
app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/my_address", methods=["GET"])
def my_address():
    chains = ChainAPI()
    return chains.my_address


@app.route("/accounts", methods=["GET"])
def accounts():
    return chain.get_all_accounts()


@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json()
    key = data['key']
    to = data['to']
    amount = data['amount']
    message = data['message']
    return chain.transfer(key, to, amount, message)


@app.route("/transactions", methods=["GET"])
def transactions():
    return chain.get_all_block()


@app.route("/pair_key", methods=["GET"])
def pair_key():
    return chain.pair_key()


@app.route("/p2p", methods=["POST"])
def p2p():
    data = request.get_json()
    send_from = data['send_from']
    to = data['to']
    amount = data['amount']
    message = data['message']
    return chain.p2p(send_from, to, amount, message)


if __name__ == "__main__":
    app.run(debug=True)

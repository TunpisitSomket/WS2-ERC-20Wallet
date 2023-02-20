from web3 import Web3


class ChainAPI:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))
        # success
        self.my_address = [self.w3.eth.accounts[0], self.w3.eth.getBalance(self.w3.eth.accounts[0])]

    # success
    def get_all_accounts(self):
        accounts = []
        for account in self.w3.eth.accounts:
            if account != self.my_address[0]:
                accounts.append([account, self.w3.eth.getBalance(account)])
        return accounts

    # success
    def transfer(self, key, to, amount, message):
        amount = self.w3.toWei(amount, 'ether')
        if self.w3.eth.getBalance(self.my_address[0]) > amount:
            signed_txn = self.w3.eth.account.signTransaction(dict(
                nonce=self.w3.eth.getTransactionCount(self.my_address[0]),
                gasPrice=self.w3.eth.gasPrice,
                gas=100000,
                to=to,
                value=amount,
                data=message.encode('utf-8')
            ), key)
            self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            transactions = self.w3.eth.waitForTransactionReceipt(signed_txn.hash.hex())
            if transactions['status'] == 1:
                transactions_info = {
                    'block': transactions['blockNumber'],
                    'hash': transactions['transactionHash'].hex(),
                    'from': transactions['from'],
                    'to': transactions['to'],
                    'value': amount,
                    'message': message,
                    'gas': transactions['gasUsed'],
                    'time': self.w3.eth.getBlock(transactions['blockNumber'])['timestamp']
                }
                return transactions_info
        else:
            return False

    # success
    def get_all_block(self):
        blocks = []
        for block in range(0, self.w3.eth.blockNumber + 1):
            blocks.append([self.w3.eth.getBlock(block)['number'], str(self.w3.eth.getBlock(block)['transactions'])[11:-3], self.w3.eth.getBlock(block)['timestamp']])
        return blocks

    # success
    def pair_key(self):
        public_key = self.w3.eth.accounts
        private_key = []
        key = open('./bank/key.txt', 'r')
        for line in key:
            private_key.append(line.replace('\n', ''))
        key.close()
        par_key = dict(zip(public_key, private_key))
        return par_key

    # success
    def p2p(self, send_from, to, amount, message):
        amount = self.w3.toWei(amount, 'ether')
        if self.w3.eth.getBalance(send_from) > amount:
            signed_txn = self.w3.eth.account.signTransaction(dict(
                nonce=self.w3.eth.getTransactionCount(send_from),
                gasPrice=self.w3.eth.gasPrice,
                gas=100000,
                to=to,
                value=amount,
                data=message.encode('utf-8')
            ), self.pair_key()[send_from])
            self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            transactions = self.w3.eth.waitForTransactionReceipt(signed_txn.hash.hex())
            if transactions['status'] == 1:
                transactions_info = {
                    'block': transactions['blockNumber'],
                    'hash': transactions['transactionHash'].hex(),
                    'from': transactions['from'],
                    'to': transactions['to'],
                    'value': amount,
                    'message': message,
                    'gas': transactions['gasUsed'],
                    'time': self.w3.eth.getBlock(transactions['blockNumber'])['timestamp']
                }
                return transactions_info
        else:
            return False

import datetime
from random import randint

from yoomoney import Quickpay, Client

client_id = '37E2223174AA2B4A643374EDCBF713E3C431DEB9D6EAEECEF4318E0C4A42FBC8'
token = '4100115953324924.24FD2DF197459AE979271A4CA97B5A2F93AD64BE774A60546BD33501CDD5185B7D70377C7E8D6F6ECDA760643B2524D703C5512ED68F9AF43CD9F386ACEE84052AAE1EDA3EC47B9414A9A87D272DDFD1BC77E4D94529C74AF84E7D51F9E6B58FC636C237336A23AB458C2931AB68D1CF5C6A9DE609ED378A7D341FCBEB096AD1'
redirect_url = 'http://t.me/intermediate_robot'

receiver = '4100115953324924'
label = ''
for _ in range(8):
    label += str(randint(100, 1000))


def get_balance_url(amount):
    quickpay = Quickpay(
        receiver=receiver,
        quickpay_form="shop",
        targets="Пополнение баланса в боте",
        paymentType="SB",
        sum=amount,
        label=label
    )
    return quickpay.base_url


def is_success():
    client = Client(token)
    history = client.operation_history()
    amount = 0
    for operation in history.operations:
        if operation.status == 'success' and \
                str(operation.datetime).split()[0] == str(datetime.datetime.today()).split()[0] and \
                str(int(datetime.datetime.now().time().hour) - 7) in str(operation.datetime).split()[1] and \
                operation.label == label and operation.amount > 0:
            amount = operation.amount
    return True, amount

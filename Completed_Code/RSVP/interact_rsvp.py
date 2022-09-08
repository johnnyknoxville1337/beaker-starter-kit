from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.atomic_transaction_composer import (
    TransactionWithSigner,
    AccountTransactionSigner,
    AtomicTransactionComposer
)

from beaker.sandbox import get_accounts, get_algod_client, add_account
from beaker.client import ApplicationClient, LogicException

from rsvp import EventRSVP

client = get_algod_client()
accts = get_accounts()

# print(accts)
creator_acct = accts[0]
guest_acct1 = accts[1]
guest_acct2 = accts[2]


# Initialize Application from algosocial.py
app = EventRSVP()

# Create an Application client containing both an algod client and my app
app_client = ApplicationClient(client, app, signer=creator_acct.signer)

# # Create an Application client containing both an algod client and my app
# app_client_guest = ApplicationClient(client, app, signer=guest_acct.signer)

def demo():
    sp = client.suggested_params()

    # Create the applicatiion on chain, set the app id for the app client

    app_id, app_addr, txid = app_client.create(event_price=1000000)
    print(f"Created App with id: {app_id} and address addr: {app_addr} in tx: {txid}")
    eve_price = app_client.call(app.read_price)
    print(f"Event price is set to {eve_price.return_value}")


    # Fund the contract for minimum balance
    atc = AtomicTransactionComposer()
    ptxn1 = TransactionWithSigner(
        txn=transaction.PaymentTxn(creator_acct.address, sp, app_addr,100000),
        signer=creator_acct.signer,
    )
    atc.add_transaction(ptxn1)
    atc.submit(client)

    #Guest 1

    app_client_guest1 = app_client.prepare(signer=guest_acct1.signer)

    # RSVP to the event by opting in

    # atc = AtomicTransactionComposer()
    ptxn2 = TransactionWithSigner(
            txn=transaction.PaymentTxn(guest_acct1.address, sp, app_addr,1000000),
            signer=guest_acct1.signer,
        )

    app_client_guest1.opt_in(payment=ptxn2)
    acct_state = app_client_guest1.get_account_state()
    print(f"Only RSVPed so checked_in should be 0 and the state is {acct_state}")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')}")
    
    # Check in to the event
    app_client_guest1.call(app.check_in)
    acct_state = app_client_guest1.get_account_state()
    print(f"checked_in should be 1 and the state is {acct_state}")
    
    # See How many RSVPed
    result = app_client.call(app.read_rsvp)
    print(f"The number of people RSVPed should be 1 and it is {result.return_value}")

    # Guest 2

    app_client_guest2 = app_client.prepare(signer=guest_acct2.signer)

     # RSVP to the event by opting in
    ptxn2 = TransactionWithSigner(
            txn=transaction.PaymentTxn(guest_acct2.address, sp, app_addr,1000000),
            signer=guest_acct2.signer,
        )

    app_client_guest2.opt_in(payment=ptxn2)
    acct_state = app_client_guest2.get_account_state()
    print(f"Only RSVPed so checked_in should be 0 and the state is {acct_state}")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')}")
    
    # See How many RSVPed
    result = app_client.call(app.read_rsvp)
    print(f"The number of people RSVPed should be 2 and it is {result.return_value}")

    # Cancel RSVP to the event
    app_client_guest2.close_out()

    try:
        app_client_guest2.get_account_state()
    except AlgodHTTPError as e:
        print(f"Succesfully closed_out: {e}")

    # See How many RSVPed
    result = app_client.call(app.read_rsvp)
    print(f"The number of people RSVPed should be 1 and it is {result.return_value}")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')}")

    # Withdraw funds and close event RSVP
    app_client.call(app.withdraw_external)
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')}")
    print(f"Event Organizer successfully withdrew remaining balance.")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')}")

    app_client.delete()
    print(f"RSVP successfully deleted.")

if __name__ == "__main__":
    demo()
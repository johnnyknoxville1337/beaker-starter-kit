from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.atomic_transaction_composer import (
    TransactionWithSigner,
)

from beaker import sandbox, consts
from beaker.client import ApplicationClient

from rsvp import EventRSVP

client = "TODO: get algod client"
accts = "TODO: get accounts"

creator_acct = "TODO: get specific account"
guest_acct1 = "TODO: get specific account"
guest_acct2 = "TODO: get specific account"


# Create instance of the EventRSVP contract
app = "TODO"

# Create an Application client for event creator containing both an algod client and my app
app_client = "TODO"

def rsvp_testing():

    print("### CREATE AND INITIALIZE CONTRACT ### \n")
    sp = "TODO: get suggested param"

    # Create the applicatiion on chain, set the app id for the app client
    app_id, app_addr, txid = "TODO"
    print(f"Created App with id: {app_id} and address addr: {app_addr} in tx: {txid}")

    event_price = "TODO: read event price"
    print(f"Event price is set to {event_price.return_value} microAlgos")

    # Fund the contract for minimum balance
    "TODO: Fund the contract to cover minimum balance here"
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')} microAlgos \n")

    # Guest 1
    print("### GUEST 1 SCENARIO ###\n")
    
    # Set up Guest 1 application client
    app_client_guest1 = "TODO"

    # RSVP to the event by opting in
    print("Guest 1 rsvp to the event...")
    ptxn2 = "TODO: transaction with signer that pays the event registration fee to the contract address"
    
    # Opt in to contract with event registration payment included
    "TODO: Account 1 opt in to contract here"
    acct_state = "TODO: get account 1 state"
    checked_in_val = acct_state["checked_in"]
    print(f"Only RSVPed so checked_in should be 0 and the state is {checked_in_val}")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')} microAlgos \n")
    
    # Check in to the event
    print("Guest 1 checking in to the Event...")
    "TODO: Account 1 check in to the event here"
    acct_state = "TODO: get account 1 state"
    checked_in_val = acct_state["checked_in"]
    print(f"checked_in should be 1 and the state is {checked_in_val}")
    
    # See How many RSVPed
    result = "TODO: read how many rsvped"
    print(f"The number of people RSVPed should be 1 and it is {result.return_value}\n")

    # Guest 2 Scenario

    print("### GUEST 2 SCENARIO ###\n")
    # Set up Guest 2 application client
    app_client_guest2 = "TODO"

    # RSVP to the event by opting in
    print("Guest 2 rsvp to the event...")
    ptxn2 = "TODO: transaction with signer that pays the event registration fee to the contract address"
    
    # Opt in to contract with event registration payment included
    "TODO: Account 1 opt in to contract here"
    acct_state = "TODO: get account 2 state"
    checked_in_val = acct_state["checked_in"]
    print(f"Only RSVPed so checked_in should be 0 and the state is {checked_in_val}")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')} microAlgos")
    
    # See How many RSVPed
    result = "TODO: read how many rsvped"
    print(f"The number of people RSVPed should be 2 and it is {result.return_value}\n")

    # Cancel RSVP to the event
    print("Guest 2 canceling registration and getting refund...")
    "TODO: close out of the contract to get refund and cancel rsvp here"

    try:
        app_client_guest2.get_account_state()
    except AlgodHTTPError as e:
        print(f"Succesfully closed_out: {e}")

    # See How many RSVPed
    result = "TODO: read how many rsvped"
    print(f"The number of people RSVPed should be 1 and it is {result.return_value}")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')} microAlgos \n")

    # Withdraw and Delete Scenario
    print("### WITHDRAW AND DELETE SCENARIO ###\n")

    # Withdraw funds and close event RSVP
    print("Event creator withdrawing funds...")
    "TODO: withdraw collected funds here"
    print(f"Event creator successfully withdrew remaining balance.")
    print(f"RSVP Balance: {client.account_info(app_addr).get('amount')} microAlgos \n")

    print("Event creator deleting rsvp contract...")
    "TODO: Delete the rsvp contract here"
    print(f"RSVP successfully deleted")

if __name__ == "__main__":
    rsvp_testing()
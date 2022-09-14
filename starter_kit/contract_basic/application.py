from pyteal import abi
from pyteal import *

from beaker.client import ApplicationClient
from beaker.application import Application
from beaker.decorators import external
from beaker import sandbox

# TODO: create a class with a hello method that returns "hello (your name)"  


# interaction code given for now. Will learn soon!
def demo():
    client = sandbox.get_algod_client()

    acct = sandbox.get_accounts().pop()

    # Create an Application client containing both an algod client and app
    app_client = ApplicationClient(client=client, app=Simple(), signer=acct.signer)

    # Create the application on chain, set the app id for the app client
    app_id, app_addr, txid = app_client.create()
    print(f"Created App with id: {app_id} and address: {app_addr} in tx: {txid}\n")

    # TODO: replace with your name to make it personal :) 
    result = app_client.call(Simple.hello, name="YOUR NAME")
    print(f"result: {result.return_value}")

demo()
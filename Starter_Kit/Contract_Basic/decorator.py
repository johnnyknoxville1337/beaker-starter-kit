from typing import Final

from imaplib import Internaldate2tuple
from sre_parse import State
from turtle import update
from typing import Final
from pyteal import abi
from pyteal import *

from beaker import (
    Application,
    ApplicationStateValue,
    DynamicApplicationStateValue,
    AccountStateValue,
    DynamicAccountStateValue,
    create,
    opt_in,
    external,
    internal
)
from beaker.state import AccountStateBlob, ApplicationStateBlob
from pyteal import abi, TealType, Bytes, Int, Txn
from beaker.client import ApplicationClient
from beaker import sandbox, Authorize

class DecoratorExample(Application):

    rsvp: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Number of people who RSVPed to the event"
    )

    ####################
    # External Methods #
    ####################

    @external
    def check_in(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        return output.set(a.get() + b.get())
    
    @external(read_only=True)
    def read_rsvp(self, *, output: abi.Uint64):
        return self.rsvp

    @external
    def add_with_internal(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        return output.set(self.internal_add(a.get(), b.get()))

    ####################
    # Internal Methods #
    ####################

    @internal(TealType.uint64)
    def internal_add(self, a: abi.Uint64, b: abi.Uint64):
        return a.get() + b.get()

    #########################
    # Bare External Methods #
    #########################

    @create
    def create(self):
        return self.initialize_application_state()

    @update(authorize=Authorize.only(Global.creator_address()))
    def update(self):
        return self.rsvp.set(Int(0))

    def demo():
        client = sandbox.get_algod_client()

        acct = sandbox.get_accounts().pop()

        # Create an Application client containing both an algod client and app
        app_client = ApplicationClient(client=client, app=DecoratorExample(), signer=acct.signer)

        # Create the application on chain, set the app id for the app client
        app_id, app_addr, txid = app_client.create()
        print(f"Created App with id: {app_id} and address: {app_addr} in tx: {txid}\n")

        result = app_client.call(DecoratorExample.)
        print(f"result: {result.return_value}")

demo()
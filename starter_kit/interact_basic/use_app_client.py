import json
from typing import Final
from pyteal import abi, TealType, Global, Approve
from beaker import (
    Application,
    AccountStateValue,
    ApplicationStateValue,
    Authorize,
    create,
    external,
    opt_in,
    close_out,
    delete,
    sandbox,
    consts,
)
from beaker.client import ApplicationClient

# Contract given.
class ClientExample(Application):
    manager: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.bytes, default=Global.creator_address()
    )

    nickname: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.bytes, descr="what this user prefers to be called"
    )

    @create
    def create(self):
        return self.initialize_application_state()

    @opt_in
    def opt_in(self):
        # Defaults to sender
        return self.initialize_account_state()

    @close_out
    def close_out(self):
        return Approve()

    @delete(authorize=Authorize.only(manager))
    def delete(self):
        return Approve()

    @external(authorize=Authorize.only(manager))
    def set_manager(self, new_manager: abi.Address):
        return self.manager.set(new_manager.get())

    @external
    def set_nick(self, nick: abi.String):
        return self.nickname.set(nick.get())

    @external(read_only=True)
    def get_nick(self, *, output: abi.String):
        return output.set(self.nickname)


def demo():
    # Set up accounts we'll use
    accts = sandbox.get_accounts()
    acct1 = accts.pop()
    print(f"account 1 address: {acct1.address}")

    # Set up Algod Client
    client=sandbox.get_algod_client()

    # Create Application client (uses signer1)
    app_client1 = ApplicationClient(
        client, app=ClientExample(), signer=acct1.signer
    )

    # Create the app on-chain 
    app_client1.create()
    print(f"Current app state: {app_client1.get_application_state()}\n")
    # Fund the app account with 1 algo
    app_client1.fund(1 * consts.algo)

    # Set nickname of acct1
    app_client1.opt_in()
    app_client1.call(ClientExample.set_nick, nick="first")
    print("account 1 local state:")
    print(app_client1.get_account_state(), "\n")

    # Show application account information
    print("application acct info:")
    app_acct_info = json.dumps(app_client1.get_application_account_info(), indent=4)
    print(app_acct_info)

    try:
        app_client1.close_out()
        app_client1.delete()
    except Exception as e:
        print(e)
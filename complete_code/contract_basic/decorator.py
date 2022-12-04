from beaker import (
    Application,
    create,
    delete,
    external,
    internal
)
from pyteal import abi, TealType, Approve, Global
from beaker.client import ApplicationClient
from beaker import sandbox, Authorize

class DecoratorExample(Application):

    ####################
    # External Methods #
    ####################

    @external
    def add(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        return output.set(a.get() + b.get())

    @external
    def add_with_internal(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        return output.set(self.internal_add(a, b))

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
        return Approve()

    @delete(authorize=Authorize.only(Global.creator_address()))
    def update(self):
        return Approve()

def demo():
    # Set up accounts we'll use
    accts = sandbox.get_accounts()
    acct1 = accts.pop()
    print(f"account 1 address: {acct1.address}")

    # Set up Algod Client
    client=sandbox.get_algod_client()

    app=DecoratorExample()

    # Create Application client
    app_client1 = ApplicationClient(client, app, signer=acct1.signer)

    # Create the app on-chain (uses signer1)
    app_client1.create()


    print(app_client1.call(DecoratorExample.add, a=7, b=4).return_value)
    print(app_client1.call(DecoratorExample.add_with_internal, a=6, b=4).return_value)

    try:
        app_client1.delete()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    demo()
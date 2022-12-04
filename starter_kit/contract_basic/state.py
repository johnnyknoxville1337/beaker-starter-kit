from typing import Final
from beaker.client import ApplicationClient, LogicException
from beaker.sandbox import get_algod_client, get_accounts
from beaker import (
    Application,
    ApplicationStateValue,
    DynamicApplicationStateValue,
    AccountStateValue,
    DynamicAccountStateValue,
    create,
    opt_in,
    external,
)
from pyteal import abi, TealType, Bytes, Int, Txn

class StateExample(Application):
    """
    <Application vs Account state>

    Application(Global) State: States held by the smart contract

    Account(Local) State: Specific states for each account
    """

    #####################
    # Application States
    #####################
    """
    Learn more about Application State here: https://algorand-devrel.github.io/beaker/html/state.html#application-state
    """

    # TODO: Declare a static app state with 
    # stack type = TealType.bytes
    # default value: "This value is immutable!"
    declared_app_value: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.bytes,
        default=Bytes(
            "This value is immutable!"
        ),
        static=True,
        descr="A static declared variable",
    )

    # TODO: Declare a dynamic app state with 
    # stack type = TealType.uint64
    # max keys = 32
    dynamic_app_value: Final[
        DynamicApplicationStateValue
        ] = DynamicApplicationStateValue(
        stack_type=TealType.uint64,
        max_keys=32,
        descr="A dictionary-like dynamic app state variable, with 32 possible keys",

    )
    #################
    # Account States
    #################
    """
    Learn more about Account State here: https://algorand-devrel.github.io/beaker/html/state.html#account-state
    """

    # TODO: Declare Account state with
    # stack type = TealType.uint64
    # default value = 1
    declared_account_value: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
        descr="Account state storing integer values",
    )

    # TODO: Declare Dynamic Account state with
    # stack type = TealType.bytes
    # max keys = 8 
    dynamic_account_value: Final[DynamicAccountStateValue] = DynamicAccountStateValue(
        stack_type=TealType.bytes,
        max_keys=8,
        descr="A dynamic state value, allowing 8 keys to be reserved, in this case byte type",
    )

    # Code from here and below are given. Calling the Demo function should work if states are implemented correctly.
    @create
    def create(self):
        return self.initialize_application_state()

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def set_app_state_val(self, v: abi.String):
        # This will fail, since it was declared as `static` and initialized to a default value during create
        return self.declared_app_value.set(v.get())

    @external(read_only=True)
    def get_app_state_val(self, *, output: abi.String):
        return output.set(self.declared_app_value)

    @external
    def set_dynamic_app_state_val(self, k: abi.Uint8, v: abi.Uint64):
        # Accessing the key with square brackets, accepts both Expr and an ABI type
        # If the value is an Expr it must evaluate to `TealType.bytes`
        # If the value is an ABI type, the `encode` method is used to convert it to bytes
        return self.dynamic_app_value[k].set(v.get())

    @external(read_only=True)
    def get_dynamic_app_state_val(self, k: abi.Uint8, *, output: abi.Uint64):
        return output.set(self.dynamic_app_value[k])

    @external
    def set_account_state_val(self, v: abi.Uint64):
        # Accessing with `[Txn.sender()]` is redundant but
        # more clear what is happening
        return self.declared_account_value[Txn.sender()].set(v.get())

    @external(read_only=True)
    def get_account_state_val(self, *, output: abi.Uint64):
        return output.set(self.declared_account_value[Txn.sender()])

    @external
    def set_dynamic_account_state_val(self, k: abi.Uint8, v: abi.String):
        return self.dynamic_account_value[k][Txn.sender()].set(v.get())

    @external(read_only=True)
    def get_dynamic_account_state_val(self, k: abi.Uint8, *, output: abi.String):
        return output.set(self.dynamic_account_value[k][Txn.sender()])


def demo():

    accts = get_accounts()

    acct = accts.pop()

    client = get_algod_client()

    app = StateExample()

    app_client = ApplicationClient(client, app, signer=acct.signer)
    app_id, app_address, transaction_id = app_client.create()
    print(
        f"DEPLOYED: App ID: {app_id} Address: {app_address} Transaction ID: {transaction_id}"
    )

    app_client.opt_in()
    print("Opted in")

    app_client.call(StateExample.set_account_state_val, v=123)
    result = app_client.call(StateExample.get_account_state_val)
    print(f"Set/get acct state result: {result.return_value}")

    app_client.call(StateExample.set_dynamic_account_state_val, k=123, v="stuff")
    result = app_client.call(StateExample.get_dynamic_account_state_val, k=123)
    print(f"Set/get dynamic acct state result: {result.return_value}")

    try:
        app_client.call(StateExample.set_app_state_val, v="Expect fail")
    except LogicException as e:
        print(f"Task failed successfully: {e}")
        result = app_client.call(StateExample.get_app_state_val)
        print(f"Set/get app state result: {result.return_value}")

    app_client.call(StateExample.set_dynamic_app_state_val, k=15, v=123)
    result = app_client.call(StateExample.get_dynamic_app_state_val, k=15)
    print(f"Set/get dynamic app state result: {result.return_value}")

if __name__ == "__main__":
    demo()
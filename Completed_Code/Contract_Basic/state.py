from sre_parse import State
from typing import Final
from pyteal import abi

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
from beaker.state import AccountStateBlob, ApplicationStateBlob
from pyteal import abi, TealType, Bytes, Int, Txn
from beaker.client import ApplicationClient
from beaker import sandbox

class StateExample(Application):

    #####################
    # Application States
    #####################

    declared_app_value: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.bytes,
        default=Bytes(
            "This value is immutable!"
        ),
        static=True,
        descr="A static declared variable",
    )

    dynamic_app_value: Final[
        DynamicApplicationStateValue
    ] = DynamicApplicationStateValue(
        stack_type=TealType.uint64,
        max_keys=32,
        descr="A dictionary-like dynamic app state variable, with 32 possible keys",
    )

    application_blob: Final[ApplicationStateBlob] = ApplicationStateBlob(
        max_keys=16,
    )

    #################
    # Account States
    #################

    declared_account_value: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
        descr="An int stored for each account that opts in",
    )

    dynamic_account_value: Final[DynamicAccountStateValue] = DynamicAccountStateValue(
        stack_type=TealType.bytes,
        max_keys=8,
        descr="A dynamic state value, allowing 8 keys to be reserved, in this case byte type",
    )

    account_blob: Final[AccountStateBlob] = AccountStateBlob(max_keys=3)

    @create
    def create(self):
        return self.initialize_application_state()

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def write_acct_blob(self, v: abi.String):
        return self.account_blob.write(Int(0), v.get())

    @external
    def read_acct_blob(self, *, output: abi.DynamicBytes):
        return output.set(
            self.account_blob.read(Int(0), self.account_blob.blob.max_bytes - Int(1))
        )

    @external
    def write_app_blob(self, v: abi.String):
        return self.application_blob.write(Int(0), v.get())

    @external
    def read_app_blob(self, *, output: abi.DynamicBytes):
        return output.set(
            self.application_blob.read(
                Int(0), self.application_blob.blob.max_bytes - Int(1)
            )
        )

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
    client = sandbox.get_algod_client()

    acct = sandbox.get_accounts().pop()

    # Create an Application client containing both an algod client and app
    app_client = ApplicationClient(client=client, app=Simple(), signer=acct.signer)

    # Create the application on chain, set the app id for the app client
    app_id, app_addr, txid = app_client.create()
    print(f"Created App with id: {app_id} and address: {app_addr} in tx: {txid}\n")

    result = app_client.call(Simple.hello_world)
    print(f"result: {result.return_value}")

demo()
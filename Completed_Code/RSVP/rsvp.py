from fileinput import close
from typing import Final

# from pyteal import abi, TealType, Int, Expr, Global, Seq, Txn, Approve, Assert,MethodConfig, CallConfig, InnerTxnBuilder, TxnField, TxnType
from pyteal import *

from beaker import (
    Application,
    ApplicationStateValue,
    AccountStateValue,
    create,
    opt_in,
    external,
    internal,
    delete,
    close_out,
    clear_state, 
    bare_external,
    Authorize
)

class EventRSVP(Application):

    price: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(1000000),
        descr="The price of the event. Default price is 1 Algo"
    )

    rsvp: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Number of people who RSVPed to the event"
    )

    checked_in: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="0 = not checked in, 1 = checked in"
    )

    @create
    def create(self, event_price: abi.Uint64):
        """Deploys the contract and initialze the app states"""
        return Seq(
            self.initialize_application_state(),
            self.price.set(event_price.get())
        )

    @opt_in
    def do_rsvp(self, payment: abi.PaymentTransaction):
        """Sender rsvp to the event by opting into the contract"""
        return Seq(
            Assert(
                Global.group_size() == Int(2),
                payment.get().receiver() == self.address,
                payment.get().amount() == self.price
            ),
            self.initialize_account_state(),
            self.rsvp.increment(),
        )
    
    @close_out
    def close_out(self):
        return self.refund()

    @clear_state
    def clear_state(self):
        return self.refund()

    @delete(authorize=Authorize.only(Global.creator_address()))
    def delete(self):
        return Approve()

    @internal
    def refund(self):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: self.price,
            }),
            InnerTxnBuilder.Submit(),
            self.rsvp.decrement()
        )

    @external(authorize=Authorize.opted_in(Global.current_application_id()))
    def check_in(self):
        """If the Sender RSVPed, check-in the Sender"""
        return self.checked_in.set(Int(1))

    @external(read_only=True, authorize=Authorize.only(Global.creator_address()))
    def read_rsvp(self, *, output: abi.Uint64):
        """Read amount of RSVP to the event. Only callable by Creator."""
        return output.set(self.rsvp)
    
    @external(read_only=True)
    def read_price(self, *, output: abi.Uint64):
        """Read amount of RSVP to the event. Only callable by Creator."""
        return output.set(self.price)


if __name__ == "__main__":
    import json

    rsvp_app = EventRSVP()
    print(f"\nApproval program:\n{rsvp_app.approval_program}")
    print(f"\nClear State program:\n{rsvp_app.approval_program}")
    print(f"\nabi:\n{json.dumps(rsvp_app.contract.dictify(), indent=2)}")

    with open("approval.teal", "w") as f:
        f.write(rsvp_app.approval_program)
    with open("rsvp_app.json", "w") as f:
        f.write(json.dumps(rsvp_app.application_spec()))
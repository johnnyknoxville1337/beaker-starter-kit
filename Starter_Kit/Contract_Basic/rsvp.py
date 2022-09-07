from typing import Final

from pyteal import abi, TealType, Int, Expr, Global, Seq

from beaker import (
    Application,
    ApplicationStateValue,
    AccountStateValue,
    create,
    opt_in,

    external,
    internal,

    sandbox,
    Authorize
)

from beaker.client import ApplicationClient

class EventRSVP(Application):

    rsvp: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Number of people who RSVPed to the event"
    )

    rsvped: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        descr="1 = rsvped"
    )

    checked_in: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="0 = not checked in, 1 = checked in"
    )

    @internal(TealType.uint64)
    def is_rsvp(self, acct: Expr):
        """Checks if the Sender RSVPed to the event"""
        return Int(1) == self.rsvped[acct]

    @create
    def create(self):
        """Deploys the contract and initialze the app states"""
        return self.initialize_application_state()

    @opt_in
    def do_rsvp(self):
        """Sender rsvp to the event by opting into the contract"""
        return Seq(
            self.initialize_account_state(),
            self.rsvped.set(Int(1))
        )

    @external(authorize=is_rsvp)
    def check_in(self):
        """If the Sender RSVPed, check-in the Sender"""
        return self.checked_in.set(Int(1))
    
    @external(read_only=True, authorize=Authorize.only(Global.creator_address()))
    def read_rsvp(self, *, output: abi.Uint64):
        """Read amount of RSVP to the event. Only callable by Creator."""
        return output.set(self.rsvp.get())



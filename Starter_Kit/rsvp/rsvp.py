from typing import Final

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
    bare_external,
    Authorize
)

class EventRSVP(Application):

    ##########
    # States #
    ##########

    price: Final[ApplicationStateValue] = "TODO"

    rsvp: Final[ApplicationStateValue] = "TODO"

    checked_in: Final[AccountStateValue] = "TODO"

    ############
    # Constants#
    ############

    # Contract address minimum balance
    MIN_BAL = Int(100000)

    # Algorand minimum txn fee
    FEE = Int(1000)

    # TODO: add appropriate decorator here
    def create(self, event_price: abi.Uint64):
        """Deploys the contract and initialze the app states"""
        pass

    # TODO: add appropriate decorator here
    def do_rsvp(self, payment: abi.PaymentTransaction):
        """Let txn sender rsvp to the event by opting into the contract"""
        pass

    # TODO: add appropriate decorator here
    # Only authorize accounts that opted in
    def check_in(self):
        """If the Sender RSVPed, check-in the Sender"""
        pass

    # TODO: add appropriate decorator here
    def withdraw_funds(self):
        """Helper method that withdraws funds in the RSVP contract"""
        pass
    
    # TODO: add appropriate decorator here
    # Only authorize the creator of the contract
    def withdraw_external(self):
        """Let event creator to withdraw all funds in the contract"""
        pass

    # TODO: add appropriate decorator here
    # Only authorize the creator of the contract
    def delete(self):
        """Let event creator delete the contract. Withdraws remaining funds"""
        pass

    # TODO: add appropriate decorator here.
    # hint: should direct close_out AND clear_state OnComplete calls to this method.
    def refund(self):
        """Refunds event payment to guests"""
        pass

    ################
    # Read Methods #
    ################
    
    # TODO: add appropriate decorator here.
    # specify it as a read only method
    # Only authorize the creator of the contract
    def read_rsvp(self, *, output: abi.Uint64):
        """Read amount of RSVP to the event. Only callable by Creator."""
        pass
    
    # TODO: add appropriate decorator here.
    # specify it as a read only method
    def read_price(self, *, output: abi.Uint64):
        """Read amount of RSVP to the event. Only callable by Creator."""
        pass


# RUN THIS FILE to create contract.json, approval.teal, and clear.teal files
if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))

    rsvp_app = EventRSVP()

    # Dump out the contract as json that can be read in by any of the SDKs
    with open(os.path.join(path, "contract.json"), "w") as f:
        f.write(json.dumps(rsvp_app.application_spec(), indent=2))

    # Write out the approval and clear programs
    with open(os.path.join(path, "approval.teal"), "w") as f:
        f.write(rsvp_app.approval_program)

    with open(os.path.join(path, "clear.teal"), "w") as f:
        f.write(rsvp_app.clear_program)

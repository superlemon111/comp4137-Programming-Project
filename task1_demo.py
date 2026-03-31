from __future__ import annotations

import json
from dataclasses import replace

from minichain import Account, Transaction


def short_address(public_key_pem: str) -> str:
    lines = [line for line in public_key_pem.splitlines() if "BEGIN" not in line and "END" not in line]
    joined = "".join(lines)
    return f"{joined[:16]}...{joined[-16:]}"


def main() -> None:
    alice = Account.create("Alice")
    bob = Account.create("Bob")

    transaction = Transaction.create(sender=alice, recipient=bob, amount=25)

    print("=== Accounts ===")
    print(f"Alice address: {short_address(alice.address)}")
    print(f"Bob address:   {short_address(bob.address)}")
    print()

    print("=== Signed Transaction ===")
    print(json.dumps(transaction.to_dict(), indent=2))
    print()

    print("=== Verification ===")
    print(f"Valid transaction: {transaction.verify()}")
    print(f"Transaction ID: {transaction.transaction_id}")
    print()

    tampered_transaction = replace(
        transaction,
        data=replace(transaction.data, amount=999),
    )
    print("=== Tampering Simulation ===")
    print(f"Valid after changing amount: {tampered_transaction.verify()}")


if __name__ == "__main__":
    main()

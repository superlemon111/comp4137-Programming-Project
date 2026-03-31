from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from .account import Account


def sha256_hex(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


@dataclass(frozen=True)
class TransactionData:
    amount: int
    amount_hash: str

    @classmethod
    def from_amount(cls, amount: int) -> "TransactionData":
        if amount <= 0:
            raise ValueError("amount must be greater than zero")
        return cls(amount=amount, amount_hash=sha256_hex(str(amount).encode("ascii")))


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    data: TransactionData
    tx_input: str
    tx_output: str
    signature: str

    @classmethod
    def create(cls, sender: Account, recipient: Account, amount: int) -> "Transaction":
        data = TransactionData.from_amount(amount)
        signing_payload = cls._build_signing_payload(
            tx_input=sender.address,
            tx_output=recipient.address,
            data=data,
        )
        signature = sender.sign(signing_payload)
        transaction_id = cls._calculate_transaction_id(
            tx_input=sender.address,
            tx_output=recipient.address,
            data=data,
            signature=signature,
        )
        return cls(
            transaction_id=transaction_id,
            data=data,
            tx_input=sender.address,
            tx_output=recipient.address,
            signature=signature,
        )

    def verify(self) -> bool:
        if self.data.amount_hash != sha256_hex(str(self.data.amount).encode("ascii")):
            return False

        signing_payload = self._build_signing_payload(
            tx_input=self.tx_input,
            tx_output=self.tx_output,
            data=self.data,
        )
        if not Account.verify_signature(self.tx_input, signing_payload, self.signature):
            return False

        expected_transaction_id = self._calculate_transaction_id(
            tx_input=self.tx_input,
            tx_output=self.tx_output,
            data=self.data,
            signature=self.signature,
        )
        return self.transaction_id == expected_transaction_id

    def to_dict(self) -> dict[str, object]:
        return {
            "transaction_id": self.transaction_id,
            "data": asdict(self.data),
            "input": self.tx_input,
            "output": self.tx_output,
            "signature": self.signature,
        }

    @staticmethod
    def _canonical_json(payload: dict[str, object]) -> bytes:
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    @classmethod
    def _build_signing_payload(
        cls,
        tx_input: str,
        tx_output: str,
        data: TransactionData,
    ) -> bytes:
        payload = {
            "data": asdict(data),
            "input": tx_input,
            "output": tx_output,
        }
        return cls._canonical_json(payload)

    @classmethod
    def _calculate_transaction_id(
        cls,
        tx_input: str,
        tx_output: str,
        data: TransactionData,
        signature: str,
    ) -> str:
        payload = {
            "data": asdict(data),
            "input": tx_input,
            "output": tx_output,
            "signature": signature,
        }
        return sha256_hex(cls._canonical_json(payload))

from __future__ import annotations

from dataclasses import dataclass

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


@dataclass(frozen=True)
class Account:
    name: str
    private_key: Ed25519PrivateKey
    public_key_pem: str

    @classmethod
    def create(cls, name: str) -> "Account":
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii")
        return cls(name=name, private_key=private_key, public_key_pem=public_key_pem)

    @property
    def address(self) -> str:
        return self.public_key_pem

    def sign(self, payload: bytes) -> str:
        return self.private_key.sign(payload).hex()

    @staticmethod
    def verify_signature(public_key_pem: str, payload: bytes, signature_hex: str) -> bool:
        try:
            public_key = serialization.load_pem_public_key(public_key_pem.encode("ascii"))
            if not isinstance(public_key, Ed25519PublicKey):
                return False
            public_key.verify(bytes.fromhex(signature_hex), payload)
            return True
        except (InvalidSignature, TypeError, ValueError):
            return False

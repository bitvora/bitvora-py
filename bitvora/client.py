import hmac
import hashlib
import requests
from requests import Session
from typing import Optional, Union, Dict

from .types import (
    BitcoinDepositResponse,
    BitcoinNetwork,
    BitcoinWithdrawalResponse,
    CreateLightningAddressResponse,
    CreateLightningInvoiceResponse,
    Currency,
    GetTransactionsResponse,
    Metadata,
    LightningInvoice
)

from .withdrawal import (
    Withdrawal,
)

class BitvoraAPIError(Exception):
    """Custom exception class for Bitvora API errors."""
    pass

class BitvoraClient:
    def __init__(self, api_key: str, network: BitcoinNetwork):
        self.api_key = api_key
        self.network = network
        self.session = Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_api_key()}"
        })

    def get_api_key(self) -> str:
        return self.api_key

    def get_network(self) -> str:
        return self.network

    def is_valid_network(self) -> bool:
        return self.get_network() in ["mainnet", "testnet", "signet"]

    def get_host(self) -> str:
        if self.get_network() == "mainnet":
            return "https://api.bitvora.com"
        elif self.get_network() == "testnet":
            return "https://api.testnet.bitvora.com"
        elif self.get_network() == "signet":
            return "https://api.signet.bitvora.com"
        else:
            return ""

    def validate_webhook_signature(self, payload: str, signature: str, secret: str) -> bool:
        hmac_obj = hmac.new(secret.encode(), payload.encode(), hashlib.sha256)
        hash_val = hmac_obj.hexdigest()
        return hash_val == signature

    def withdraw(self, destination: str, amount: float, currency: Currency) -> Withdrawal:
        response = self.session.post(
            f"{self.get_host()}/v1/bitcoin/withdraw/confirm",
            json={"destination": destination, "amount": amount, "currency": currency.value}
        )
        data = response.json()

        if response.status_code not in [200, 201]:
            raise BitvoraAPIError(data.get("message", "Unknown error occurred"))

        return Withdrawal(self, data)

    def get_withdrawal(self, withdrawal_id: str) -> BitcoinWithdrawalResponse:
        response = self.session.get(
            f"{self.get_host()}/v1/transactions/withdrawals/{withdrawal_id}"
        )
        return response.json()

    def get_deposit(self, deposit_id: str) -> BitcoinDepositResponse:
        response = self.session.get(
            f"{self.get_host()}/v1/transactions/deposits/{deposit_id}"
        )
        return response.json()

    def create_lightning_address(self, metadata: Optional[Metadata]) -> CreateLightningAddressResponse:
        response = self.session.post(
            f"{self.get_host()}/v1/bitcoin/deposit/lightning-address",
            json={"handle": None, "domain": None, "metadata": metadata}
        )
        return response.json()

    def create_custom_lightning_address(self, handle: str, domain: str, metadata: Optional[Metadata]) -> Dict:
        response = self.session.post(
            f"{self.get_host()}/v1/bitcoin/deposit/lightning-address",
            json={"handle": handle, "domain": domain, "metadata": metadata}
        )
        return response.json()

    def create_lightning_invoice(self, amount: float, currency: Currency, memo: str, expiry_seconds: int, metadata: Optional[Metadata]) -> LightningInvoice:
        response = self.session.post(
            f"{self.get_host()}/v1/bitcoin/deposit/lightning-invoice",
            json={
                "amount": amount,
                "currency": currency.value,
                "description": memo,
                "expiry_seconds": expiry_seconds,
                "metadata": metadata
            }
        )
        return LightningInvoice(self, response.json())

    def get_lightning_invoice(self, invoice_id: str) -> CreateLightningInvoiceResponse:
        response = self.session.get(
            f"{self.get_host()}/v1/bitcoin/deposit/lightning-invoice/id/{invoice_id}"
        )
        return response.json()

    def get_balance(self) -> float:
        response = self.session.get(
            f"{self.get_host()}/v1/transactions/balance"
        )
        data = response.json()
        if "data" not in data or "balance" not in data["data"]:
            raise BitvoraAPIError("Unexpected response format")
        return data["data"]["balance"]

    def get_transactions(self) -> GetTransactionsResponse:
        response = self.session.get(
            f"{self.get_host()}/v1/transactions"
        )
        return response.json()

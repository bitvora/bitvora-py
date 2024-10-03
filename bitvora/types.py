from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union

Metadata = Dict[str, str]

class BitcoinNetwork(str, Enum):
    MAINNET = "mainnet"
    TESTNET4 = "testnet4"
    SIGNET = "signet"

class Currency(str, Enum):
    AUD = "aud"
    CAD = "cad"
    CHF = "chf"
    CNY = "cny"
    EUR = "eur"
    GBP = "gbp"
    HKD = "hkd"
    JPY = "jpy"
    NZD = "nzd"
    USD = "usd"
    BTC = "btc"
    SATS = "sats"

@dataclass
class DepositOnChainPayload:
    deposit_id: str
    chain_txid: str
    chain_deposit_address: str
    amount_sats: int
    fee: float
    status: str  # "pending" | "settled" | "failed"
    metadata: Metadata

@dataclass
class WithdrawalOnChainPayload:
    withdrawal_id: str
    chain_txid: str
    chain_withdrawal_address: str
    amount_sats: int
    fee: float
    status: str  # "pending" | "settled" | "failed"
    metadata: Metadata

@dataclass
class WithdrawalLightningPayload:
    withdrawal_id: str
    recipient: str
    status: str  # "pending" | "settled" | "failed"
    amount_sats: int
    payment_route: Dict[str, List[Dict[str, Union[str, int]]]]
    payment_preimage: str
    metadata: Metadata

@dataclass
class DepositLightningPayload:
    deposit_id: str
    sender: str
    status: str  # "pending" | "settled" | "failed"
    amount_sats: int
    payment_request: str
    description_hash: str
    expiry_seconds: int
    payment_preimage: str
    r_hash: str
    metadata: Metadata

@dataclass
class WebhookPayloads:
    deposit_chain_pending: DepositOnChainPayload
    deposit_chain_completed: DepositOnChainPayload
    withdrawal_chain_pending: WithdrawalOnChainPayload
    withdrawal_chain_completed: WithdrawalOnChainPayload
    withdrawal_lightning_pending: WithdrawalLightningPayload
    withdrawal_lightning_completed: WithdrawalLightningPayload
    deposit_lightning_completed: DepositLightningPayload

@dataclass
class DepositOnChainCompletedEvent:
    data: DepositOnChainPayload
    event_type: str = "deposit.onchain.completed"

@dataclass
class DepositOnChainPendingEvent:
    data: DepositOnChainPayload
    event_type: str = "deposit.onchain.pending"

@dataclass
class DepositLightningCompletedEvent:
    data: DepositLightningPayload
    event_type: str = "deposit.lightning.completed"

@dataclass
class WithdrawalChainPendingEvent:
    data: WithdrawalOnChainPayload
    event_type: str = "withdrawal.chain.pending"

@dataclass
class WithdrawalChainCompletedEvent:
    data: WithdrawalOnChainPayload
    event_type: str = "withdrawal.chain.completed"

@dataclass
class WithdrawalLightningPendingEvent:
    data: WithdrawalLightningPayload
    event_type: str = "withdrawal.lightning.pending"

@dataclass
class WithdrawalLightningCompletedEvent:
    data: WithdrawalLightningPayload
    event_type: str = "withdrawal.lightning.completed"

WebhookEvent = Union[
    DepositOnChainCompletedEvent,
    DepositOnChainPendingEvent,
    DepositLightningCompletedEvent,
    WithdrawalChainPendingEvent,
    WithdrawalChainCompletedEvent,
    WithdrawalLightningPendingEvent,
    WithdrawalLightningCompletedEvent,
]

@dataclass
class BitcoinWithdrawalResponse:
    status: int
    message: str
    data: 'BitcoinWithdrawal'  # Forward reference

@dataclass
class BitcoinWithdrawal:
    id: str
    company_id: str
    ledger_tx_id: str
    amount_sats: int
    recipient: str
    network_type: str
    rail_type: str
    fee_sats: int
    status: str
    lightning_payment: Optional['LightningPayment']
    metadata: Optional[str]
    chain_tx_id: Optional[str]
    created_at: str
    updated_at: str

@dataclass
class LightningAddress:
    id: str
    company_id: str
    handle: Optional[str]
    domain: Optional[str]
    address: str
    metadata: Metadata
    created_at: str
    updated_at: str
    last_used_at: Optional[str]
    deleted_at: Optional[str]

@dataclass
class CreateLightningAddressResponse:
    status: int
    message: str
    data: LightningAddress

@dataclass
class LightningInvoice:
    id: str
    company_id: str
    node_id: str
    memo: str
    r_preimage: str
    r_hash: str
    value: int
    settled: bool
    creation_date: str
    settle_date: str
    payment_request: str
    description_hash: str
    expiry: str
    state: str
    metadata: Metadata
    lightning_address_id: Optional[str]

@dataclass
class CreateLightningInvoiceResponse:
    status: int
    message: str
    data: LightningInvoice

@dataclass
class BitcoinDeposit:
    id: str
    company_id: str
    ledger_tx_id: str
    recipient: str
    amount_sats: int
    network_type: str
    rail_type: str
    status: str
    chain_tx_id: Optional[str]
    lightning_invoice_id: Optional[str]
    created_at: str
    updated_at: str

@dataclass
class BitcoinDepositResponse:
    status: int
    message: str
    data: BitcoinDeposit

@dataclass
class LightningPayment:
    node_id: str
    response: Dict[str, Union[str, Dict[str, Union[int, str, List[Dict[str, Union[str, int]]]]]]]

@dataclass
class GetTransactionsResponse:
    status: int
    message: str
    data: List['Transaction'] 

@dataclass
class Transaction:
    id: str
    company_id: str
    amount_sats: int
    recipient: str
    rail_type: str
    type: str
    status: str
    created_at: str

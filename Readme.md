# Bitvora SDK

A Python SDK for the Bitvora API and Webhooks.

## Installation

```bash
pip install bitvora
```

## Usage

### Sending Bitcoin (withdrawal)

```python
from bitvora import BitvoraClient, Withdrawal

client = BitvoraClient(api_key="<API_KEY>", network="signet") # Use 'mainnet', 'testnet', or 'signet'

async def send_bitcoin():
    withdrawal_response = await client.withdraw(
        "utxo1@getalby.com",  # accepts on-chain, lightning invoice (payment request), lightning address, lnurl
        10.0,                 # amount in your desired currency
        'USD'                 # currency code
    )

    withdrawal = Withdrawal(client, withdrawal_response)

    # Wait until the payment succeeds or fails (optional)
    await withdrawal.is_settled()

    return withdrawal
```

### Creating a Lightning Address

```python
from bitvora import BitvoraClient

client = BitvoraClient(api_key="<API_KEY>", network="signet") # Use 'mainnet', 'testnet', or 'signet'

async def create_lightning_address():
    metadata = {
        'userID': 'your-internal-user-id',
        'email': 'useremail@protonmail.com'
    }  # Optional metadata object to attach

    return await client.create_lightning_address(metadata)  
```

### Create a Lightning Invoice

```python
from bitvora import BitvoraClient, Currency

client = BitvoraClient(api_key="<API_KEY>", network="signet") # Use 'mainnet', 'testnet', or 'signet'

async def create_lightning_invoice():
    metadata = {
        'userID': 'your-internal-user-id',
        'email': 'useremail@protonmail.com'
    }  # Optional metadata object to attach

    invoice = await client.create_lightning_invoice(
        amount=50,  # Amount to charge
        currency=Currency.SATS,  # Currency type (assuming SATS is defined in your types module)
        description='this is from the sdk',
        expiry=3600,  # Expiry time in seconds
        metadata=metadata  # Pass the metadata dictionary
    )

    await invoice.is_settled()  # Wait until the invoice is settled (payment succeeded or failed)

    return invoice
```

### Get Balance

```python
from bitvora import BitvoraClient

client = BitvoraClient(api_key="<API_KEY>", network="signet") # Use 'mainnet', 'testnet', or 'signet'

async def get_balance() -> float:
    balance = await client.get_balance() 
    return balance
```

### Get Transactions

```python
from bitvora import BitvoraClient

client = BitvoraClient(api_key="<API_KEY>", network="signet") # Use 'mainnet', 'testnet', or 'signet'

async def get_transactions() -> dict:
    transactions = await client.get_transactions() 
    return transactions
```

### Get Deposit

```python
from bitvora import BitvoraClient

client = BitvoraClient(api_key="<API_KEY>", network="signet") # Use 'mainnet', 'testnet', or 'signet'

async def get_deposit(deposit_uuid: str) -> dict:
    deposit = await client.get_deposit(deposit_uuid) 
    return deposit
```

### Get Withdrawal

```python
from bitvora import BitvoraClient

client = BitvoraClient(api_key="<API_KEY>", network="signet") # Use 'mainnet', 'testnet', or 'signet'

async def get_withdrawal(withdrawal_uuid: str) -> dict:
    withdrawal = await client.get_withdrawal(withdrawal_uuid) 
    return withdrawal

```

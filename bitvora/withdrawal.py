import time
from typing import Any, Optional
from .types import (
    BitcoinWithdrawalResponse,
    LightningPayment
)

class Withdrawal:
    """
    Represents a Bitcoin withdrawal and provides methods to check its status.
    """

    def __init__(self, data: BitcoinWithdrawalResponse):
        """
        Initializes the Withdrawal object.

        Args:
            data (BitcoinWithdrawalResponse): The withdrawal response data.
        """
        withdrawal_data = data['data']
        self.id: str = withdrawal_data['id']
        self.company_id: str = withdrawal_data['company_id']
        self.ledger_tx_id: str = withdrawal_data['ledger_tx_id']
        self.amount_sats: int = withdrawal_data['amount_sats']
        self.recipient: str = withdrawal_data['recipient']
        self.network_type: str = withdrawal_data['network_type']
        self.rail_type: str = withdrawal_data['rail_type']
        self.fee_sats: int = withdrawal_data['fee_sats']
        self.status: str = withdrawal_data['status']
        self.lightning_payment: Optional[LightningPayment] = withdrawal_data.get('lightning_payment')
        self.chain_tx_id: Optional[str] = withdrawal_data.get('chain_tx_id')
        self.metadata: Optional[Any] = withdrawal_data.get('metadata')
        self.created_at: str = withdrawal_data['created_at']
        self.updated_at: str = withdrawal_data['updated_at']

    async def is_settled(self, client, max_duration: int = 20000, check_interval: int = 1000) -> None:
        """
        Checks if the withdrawal is settled, updating the object with the latest status.

        Args:
            client: The Bitvora client instance to fetch the latest status.
            max_duration (int): The maximum time to wait for the withdrawal to settle, in milliseconds.
            check_interval (int): The time interval between status checks, in milliseconds.
        """
        from .client import BitvoraClient  # Import inside the function to avoid circular imports

        if not isinstance(client, BitvoraClient):
            raise ValueError("Invalid client instance provided.")

        start_time = time.time()

        while True:
            try:
                withdrawal_status = await client.get_withdrawal(self.id)
                status = withdrawal_status['data']['status']

                if status in ("settled", "failed"):
                    self.__dict__.update(withdrawal_status['data'])
                    break
                elif (time.time() - start_time) * 1000 >= max_duration:
                    self.__dict__.update(withdrawal_status['data'])
                    break

            except Exception as e:
                raise e

            time.sleep(check_interval / 1000)

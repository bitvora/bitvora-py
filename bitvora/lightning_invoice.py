import time
from typing import Any, Optional
from .types import BitvoraClient, CreateLightningInvoiceResponse

class LightningInvoice:
    def __init__(self, client: BitvoraClient, data: CreateLightningInvoiceResponse):
        lightning_invoice_data = data['data']
        self.client = client
        self.id = lightning_invoice_data['id']
        self.company_id = lightning_invoice_data['company_id']
        self.memo = lightning_invoice_data['memo']
        self.preimage = lightning_invoice_data['r_preimage']
        self.rhash = lightning_invoice_data['r_hash']
        self.value = lightning_invoice_data['value']
        self.is_settled = lightning_invoice_data['settled']
        self.settle_date = lightning_invoice_data['settle_date']
        self.payment_request = lightning_invoice_data['payment_request']
        self.description_hash = lightning_invoice_data['description_hash']
        self.expiry = lightning_invoice_data['expiry']
        self.state = lightning_invoice_data['state']
        self.metadata = lightning_invoice_data['metadata']
        self.lightning_address_id = lightning_invoice_data.get('lightning_address_id')

    async def check_settlement_status(self) -> None:
        """Check the settlement status of the lightning invoice asynchronously."""
        invoice_status = await self.client.get_lightning_invoice(self.id)
        self.__dict__.update(invoice_status['data'])

    async def wait_for_settlement(self, max_duration: int = 2000000, check_interval: int = 1000) -> None:
        """Wait for the lightning invoice to be settled or until the max duration is reached."""
        start_time = time.time()

        while True:
            try:
                await self.check_settlement_status()
                if self.is_settled:
                    break
                elif (time.time() - start_time) * 1000 >= max_duration:
                    break
            except Exception as e:
                raise e
            time.sleep(check_interval / 1000)

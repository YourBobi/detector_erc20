from django.core.management.base import BaseCommand
from erc20.models import ERC20


class Command(BaseCommand):
    help = "Filling in the Contract table"

    def handle(self, *args, **kwargs):
        with open("erc20/management/commands/Uni.sol") as file:
            for i in range(50):
                ERC20.objects.create(
                    contract_address="0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
                    contract_name="Uni",
                    solidity_version="0.5.16",
                    source_code=file.read(),
                    erc20_version="",
                    status="wait_processing",
                )
        with open("erc20/management/commands/TokenMintERC20Token.sol") as file:
            for i in range(50):
                ERC20.objects.create(
                    contract_address="0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
                    contract_name="TokenMintERC20Token",
                    solidity_version="0.5.0",
                    source_code=file.read(),
                    erc20_version="",
                    status="wait_processing",
                )
        self.stdout.write("Filling completed")

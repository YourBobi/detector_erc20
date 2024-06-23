from core.token_standards.base_comparer import ContractComparer
from core.token_standards.signatures import ERC20_SIGNATURES


class ERC20ContractComparer(ContractComparer):
    """Compare contracts standards for erc20"""

    contract_type = "ERC20"
    required_functions_names = {'balanceOf', 'totalSupply', 'transferFrom', 'transfer', 'approve', 'allowance'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compare_signature(self):
        """
        Return true if contract is erc20
        :return: true if contract is erc20
        :rtype: bool
        """
        count_result = 0
        for function in self.functions:
            if ERC20_SIGNATURES.get(function.name) == function.signature_str:
                count_result += 1
        return True if count_result == len(self.required_functions_names) else False

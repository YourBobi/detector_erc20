import os

from slither.slither import Slither
from solc_select.solc_select import installed_versions, get_available_versions, current_version


class ContractComparer:

    contract_type = None
    required_functions_names = set()

    def __init__(self, contract_address, contract_name, solidity_version, source_code):
        self.source_code = source_code
        self.__use_correct_solidity_version(solidity_version)
        self.contract = self.__get_slither(contract_address).get_contract_from_name(contract_name)
        self.functions = []
        self.__set_functions()

    def __get_slither(self, contract_address):
        if not os.path.isdir('buffer'):
            os.mkdir('buffer')

        path = f'./buffer/{contract_address}.sol'
        source_file = open(path, 'w')
        source_file.write(self.source_code)
        result = Slither(path)
        os.remove(path)
        return result

    def __set_functions(self):
        for func in self.contract.functions:
            if (
                    func.is_implemented
                    and (func.visibility == 'public' or func.visibility == "external")
                    and func.name in self.required_functions_names
            ):
                self.functions.append(func)

    @staticmethod
    def __use_correct_solidity_version(version):
        if current_version()[0] == version:
            ...
        elif version not in installed_versions() and version in get_available_versions():
            os.system(f'solc-select install {version}')
            os.system(f'solc-select use {version}')
        elif version in installed_versions():
            os.system(f'solc-select use {version}')
        else:
            raise ValueError(f"Incorrect Solidity version {version}")

    def compare_signature(self):
        """"""

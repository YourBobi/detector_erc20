from detector.celery import app
from celery.utils.log import get_task_logger

from erc20.models import ERC20, ERC20Statuses
from erc20.comparer import ERC20ContractComparer

logger = get_task_logger(__name__)


@app.task
def check_and_update_erc20_contracts():
    """Start check type of contract standards"""
    contracts_ids = list(
        ERC20.objects.filter(status=ERC20Statuses.WAIT_PROCESSING)
        .order_by('solidity_version')
        .values_list('id', flat=True)[:12000]
    )
    ERC20.objects.filter(id__in=contracts_ids).update(status=ERC20Statuses.PROCESSING)
    for contract_id in contracts_ids:
        check_and_update_contract.apply_async(kwargs={'contract_id': contract_id})


@app.task
def check_and_update_contract(contract_id: ERC20):
    logger.info(f"Start check_and_update_contract:{contract_id}")
    contract = ERC20.objects.filter(id=contract_id).first()
    try:
        comparer = ERC20ContractComparer(
            source_code=contract.source_code,
            contract_address=contract.contract_address,
            contract_name=contract.contract_name,
            solidity_version=contract.solidity_version,
        )
        contract.is_erc20 = comparer.compare_signature()
        if contract.is_erc20:
            # не реализовал
            contract.erc20_version = ''
        contract.status = ERC20Statuses.PROCESSED
    except Exception as e:
        logger.warning(f"check_and_update_contract:{contract_id} failed with error: {e}")
        contract.status = ERC20Statuses.FAILED
    contract.save()
    logger.info(f"Finish check_and_update_contract:{contract_id}")

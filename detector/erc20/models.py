from django.db import models


class ERC20Statuses(models.TextChoices):

    WAIT_PROCESSING = 'wait_processing', 'Wait processing'
    PROCESSING = 'processing', 'Processing'
    PROCESSED = 'processed', 'Processed'
    FAILED = 'failed', 'Failed'


class ERC20(models.Model):
    contract_address = models.CharField(max_length=100, verbose_name='Contract address', blank=False)
    contract_name = models.CharField(max_length=100, verbose_name='Contract name', blank=False)
    solidity_version = models.CharField(max_length=100, verbose_name='Solidity version', blank=False)
    source_code = models.TextField()
    is_erc20 = models.BooleanField(blank=True, null=True)
    erc20_version = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        verbose_name='Status of contract',
        max_length=128,
        choices=ERC20Statuses.choices,
        default=ERC20Statuses.WAIT_PROCESSING,
        blank=True,
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'ERC20'
        verbose_name_plural = 'ERC20'

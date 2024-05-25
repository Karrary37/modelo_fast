import logging
from typing import List, Optional

from pydantic import BaseModel, validator


logger = logging.getLogger('validacao')


class ValidationPayload(BaseModel):
    """
    Represents a validation payload containing information related to a contract and its validation.

    Attributes:
        contrato (ContractsItem): Information about the contract.
        cliente (ClientItem): Information about the client associated with the contract.
        representante (Optional[RepresentativeItem]): Information about the representative, if applicable.
        beneficio (Optional[BenefitItem]): Information about the benefits associated with the contract.
        parcela (List[PortionItem]): List of portions related to the contract.
        contratosOrigem (Optional[List[SourceContractsItem]]): List of source contracts, if applicable.
        dadosBancariosSacado (Optional[BankDetailsWithdrawnItem]): Bank details of the withdrawn party, if applicable.
        anexos (Optional[List[AttachmentsItem]]): List of attachments related to the contract.
        retornoFGTS (Optional[ReturnFGTSItem]): Information about the FGTS return, if applicable.
        operacao (str): The type of operation associated with the validation payload.
        cessionario (str): The party to whom the contract is assigned.

    Note:
        This class is designed to hold various pieces of information related to the validation of a contract.
        It is structured using the Pydantic BaseModel for data validation and serialization purposes.
    """

import logging
from typing import Optional

from pydantic import BaseModel, validator
from validate_docbr import CNPJ, CPF

logger = logging.getLogger('validacao')


class BankDetailsWithdrawnItem(BaseModel):
    """
    Pydantic model representing bank details for a withdrawn item.

    Attributes:
        cdContaTipo (int): Account type code.
        nuBanco (int): Bank number.
        nuAgencia (int): Agency number.
        nuConta (str): Account number.
        nuContaDigito (int): Account digit.
        nuCpfTitular (Optional[str]): Optional CPF of the account holder.
        nuCnpjTitular (Optional[str]): Optional CNPJ of the account holder.
        cdCreditoTipo (int): Credit type code.
    """

    cdContaTipo: int
    nuBanco: int
    nuAgencia: int
    nuConta: str
    nuContaDigito: str
    nuCpfTitular: Optional[str] = None
    nuCnpjTitular: Optional[str] = None
    cdCreditoTipo: int

    @validator(
        'nuContaDigito',
        pre=True,
        always=True,
    )
    def validate_non_empty_strings(cls, value):
        """
        Validates that a string is not empty or contains only whitespace.

        Args:
            value (str): The string to be validated.

        Raises:
            ValueError: If the string is empty or contains only whitespace.

        Returns:
            str: The input string if it is valid.
        """
        try:
            if not value or value.isspace():
                raise ValueError(
                    'Campo não pode ser vazio ou conter apenas espaços em branco'
                )
            return value
        except Exception as e:
            logger.error(
                f'Campo não pode ser vazio ou conter apenas espaços em branco | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                'Campo não pode ser vazio ou conter apenas espaços em branco'
            )

    @validator('nuCpfTitular', pre=True, always=True)
    def validate_cpf(cls, value):
        """
        Validates the 'nuCpfTitular' field using a CPF validation function.

        Args:
            value (str): The 'nuCpfTitular' value to be validated.

        Raises:
            ValueError: If the 'nuCpfTitular' value is not a valid CPF.

        Returns:
            str: The input 'nuCpfTitular' value if it is a valid CPF.
        """
        try:
            if value is not None:
                if not CPF().validate(value):
                    raise ValueError('CPF inválido')
                return value
        except Exception as e:
            logger.error(f'CPF inválido | Campo: {value} | Error: {e}')
            raise ValueError('CPF inválido')

    @validator('nuCnpjTitular', pre=True, always=True)
    def validate_cnpj(cls, value):
        """
        Validates the 'nuCnpjTitular' field using a CNPJ validation function.

        Args:
            value (str): The CNPJ value to be validated.

        Raises:
            ValueError: If the 'nuCnpjTitular' value is not a valid CNPJ.

        Returns:
            str: The input value if it is a valid CNPJ, or an empty string if the input is None.
        """
        try:
            if value is not None:
                if not CNPJ().validate(value):
                    raise ValueError('CNPJ inválido')
            else:
                return ''
            return value
        except Exception as e:
            logger.error(f'CNPJ inválido | Campo: {value} | Error: {e}')
            raise ValueError('CNPJ inválido')

    @validator('cdContaTipo', pre=True, always=True)
    def validate_tp_account(cls, value):
        """
        Validates that 'cdContaTipo' contains only specific numbers.

        Args:
            value (int): The value of 'cdContaTipo'.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If 'cdContaTipo' contains an invalid number.
        """
        try:
            if int(value) not in {1, 2, 3, 4, 5}:
                raise ValueError('Valor inválido.')
            return value
        except Exception as e:
            logger.error(f'Valor inválido | Campo: {value} | Error: {e}')
            raise ValueError('Valor inválido')

    @validator('cdCreditoTipo', pre=True, always=True)
    def validate_tp_credit(cls, value):
        """
        Validates that 'cdCreditoTipo' contains only specific numbers.

        Args:
            value (int): The value of 'cdCreditoTipo'.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If 'cdCreditoTipo' contains an invalid number.
        """
        try:
            if int(value) not in {1, 2}:
                raise ValueError('Valor inválido')
            return value
        except Exception as e:
            logger.error(f'Valor inválido | Campo: {value} | Error: {e}')
            raise ValueError('Valor inválido')

    @validator(
        'nuBanco', 'nuAgencia', 'nuConta', 'nuContaDigito', pre=True, always=True
    )
    def validate_20_length(cls, value):
        """
        Validates the length of filds .

        Args:
            value (str): The value of filds.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If filds exceeds the maximum length.
        """
        max_length = 20
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('nuConta', pre=True, always=True)
    def validate_nu_conta_not_null(cls, value):
        """
        Validate if nuConta is not null

        Args:
            value (str): The nuConta field

        Returns:
            str: The validated field

        Raises:
            ValueError: If field is empty or none.
        """
        if not value:
            raise ValueError('O campo nuConta é obrigatório.')

        return value

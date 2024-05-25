import logging
from datetime import datetime

from pydantic import BaseModel, validator
from validate_docbr import CNPJ

logger = logging.getLogger('validacao')


class SourceContractsItem(BaseModel):
    """
    Represents an item for source contracts with the following attributes:

    Attributes:
        dtContratoOrigem (str): The date of the source contract in string format ('YYYY-MM-DD').
        dtPrimeiroVencimentoContratoOrigem (str): The date of the first installment in string format ('YYYY-MM-DD').
        dtUltimoVencimentoContratoOrigem (str): The date of the last installment in string format ('YYYY-MM-DD').
        nuContratoOrigem (int): The number of the source contract.
        nuCnpjCorrespondenteOrigem (str): The CNPJ of the corresponding entity for the source contract.
        cdInstFinanceiraOrigem (int): The code of the financial institution for the source contract.
        vrContratoOrigem (float): The value of the source contract.
        vrSaldoContratoOrigem (float): The balance amount of the source contract.
        contrato (str): Additional information related to the source contract.
    """

    dtContratoOrigem: str
    dtPrimeiroVencimentoContratoOrigem: str
    dtUltimoVencimentoContratoOrigem: str
    nuContratoOrigem: int
    nuCnpjCorrespondenteOrigem: str
    cdInstFinanceiraOrigem: int
    vrContratoOrigem: float
    vrSaldoContratoOrigem: float

    @validator(
        'dtContratoOrigem',
        'dtPrimeiroVencimentoContratoOrigem',
        'dtUltimoVencimentoContratoOrigem',
        'nuContratoOrigem',
        'nuCnpjCorrespondenteOrigem',
        'cdInstFinanceiraOrigem',
        'vrContratoOrigem',
        'vrSaldoContratoOrigem',
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

    @validator(
        'dtContratoOrigem',
        'dtPrimeiroVencimentoContratoOrigem',
        'dtUltimoVencimentoContratoOrigem',
        pre=True,
        always=True,
    )
    def validate_date(cls, value):
        """
        Validates and formats date fields in the 'SourceContractsItem' model.

        Args:
            value (str): The value of a date field in the 'SourceContractsItem' model.

        Returns:
            str: The validated and formatted date.

        Raises:
            ValueError: If the date format is invalid.
        """
        try:
            parsed_date = datetime.strptime(value, '%Y-%m-%d')
            formatted_date = parsed_date.strftime('%Y-%m-%d')

            if formatted_date != value:
                raise ValueError("Formato de data inválido. Use o formato 'AAAA-MM-DD'")
            return value
        except Exception as e:
            logger.error(
                f'Formato de data inválido. Use o formato "AAAA-MM-DD" | Campo: {value} | Error: {e}'
            )
            raise ValueError("Formato de data inválido. Use o formato 'AAAA-MM-DD'")

    @validator('nuCnpjCorrespondenteOrigem', pre=True, always=True)
    def validate_cnpj(cls, value):
        """
        Validates the 'nuCnpjCorrespondenteOrigem' field using a CNPJ validation function.

        Args:
            value (str): The CNPJ value to be validated.

        Raises:
            ValueError: If the 'nuCnpjCorrespondenteOrigem' value is not a valid CNPJ.

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

    @validator('vrContratoOrigem', 'vrSaldoContratoOrigem', pre=True, always=True)
    def validate_float(cls, value):
        """
        Validates and converts a string value to a float, ensuring it is greater than or equal to zero.

        Args:
            value (str): The string representation of a float.

        Returns:
            float: The validated float value.

        Raises:
            ValueError: If the value is not a valid float or is less than zero.
        """
        try:
            if value == '':
                value = 0
            parsed_value = float(value)
            if parsed_value < 0:
                raise ValueError('O valor deve ser maior ou igual zero')
            return value
        except Exception as e:
            logger.error(
                f'O valor deve ser maior ou igual zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor deve ser maior ou igual zero')

    @validator('vrContratoOrigem', 'vrSaldoContratoOrigem', pre=True, always=True)
    def validate_vr_source_contracts(cls, value):
        """
        Validates the decimal number to have at most 12 digits with at most 2 decimal places.

        Args:
            value (float): The value of the decimal number.

        Returns:
            float: The validated value.

        Raises:
            ValueError: If the decimal number does not meet the length and precision requirements.
        """
        max_digits = 13
        max_decimal_places = 2
        max_integer_places = 10

        try:
            if value:
                decimal_value = str(float(value))

                integer_part, decimal_part = str(decimal_value).split('.')

                if (
                    len(integer_part) > max_integer_places
                    or len(decimal_part) > max_decimal_places
                ):
                    raise ValueError(
                        f'O número decimal deve ter no máximo {max_digits} dígitos, com no máximo {max_decimal_places} casas decimais'
                    )
            return value
        except Exception as e:
            logger.error(
                f'O número decimal deve ter no máximo {max_digits} dígitos, com no máximo {max_decimal_places} casas decimais | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                f'O número decimal deve ter no máximo {max_digits} dígitos, com no máximo {max_decimal_places} casas decimais'
            )

    @validator('nuContratoOrigem', pre=True, always=True)
    def validate_50_length(cls, value):
        """
        Validates the length of 'nuContratoOrigem' .

        Args:
            value (str): The value of 'nuContratoOrigem'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuContratoOrigem' exceeds the maximum length.
        """
        max_length = 50
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('cdInstFinanceiraOrigem', pre=True, always=True)
    def validate_19_length(cls, value):
        """
        Validates the length of 'cdInstFinanceiraOrigem'.

        Args:
            value (str): The value of 'cdInstFinanceiraOrigem'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'cdInstFinanceiraOrigem' exceeds the maximum length.
        """
        max_length = 19
        try:
            if len(value) > max_length:
                raise ValueError(f'Número dever ter no máximo {max_length} caracteres.')

            try:
                if int(value) <= 0:
                    raise ValueError('Número dever ser maior ou igual à zero')
            except ValueError:
                raise ValueError('Número dever ser maior ou igual à zero')

            return value
        except Exception as e:
            logger.error(
                f'Número dever ser maior ou igual à zero e ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                f'Número dever ser maior ou igual à zero e ter no máximo {max_length} caracteres'
            )

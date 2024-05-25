import logging
from datetime import datetime

from pydantic import BaseModel, validator

logger = logging.getLogger('validacao')


class ReturnFGTSItem(BaseModel):
    """
    Pydantic model representing an item in the 'retornoFGTS' array.

    Attributes:
        nuContratoCCB (int): Contract CCB number.
        nuProtocoloAverbacao (str): Protocol number for averment.
        cdRetornoAverbacao (str): Code indicating the return status of the averment.
        dtRetornoAverbacao (str): Date of the averment return.
    """

    nuContratoCCB: int
    nuProtocoloAverbacao: int
    cdRetornoAverbacao: int
    dtRetornoAverbacao: str

    @validator(
        'nuContratoCCB',
        'nuProtocoloAverbacao',
        'cdRetornoAverbacao',
        'dtRetornoAverbacao',
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
        'cdRetornoAverbacao',
        'nuProtocoloAverbacao',
        'nuContratoCCB',
        pre=True,
        always=True,
    )
    def validate_number_greater_than_zero(cls, value):
        """
        Valida se o valor é um número inteiro maior que zero.

        Parameters:
            value (int): O valor a ser validado.

        Returns:
            int: O valor validado.

        Raises:
            ValueError: Se o valor não for um número inteiro maior que zero.
        """
        try:
            if int(value) <= 0:
                raise ValueError('Campo deve ser um número maior ou igual à zero')
            return value
        except Exception as e:
            logger.error(
                f'Campo deve ser um número maior ou igual à zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('Campo deve ser um número maior ou igual à zero')

    @validator('dtRetornoAverbacao', pre=True, always=True)
    def validate_datetime_(cls, value):
        """
        Validates and formats the date and time.

        Args:
            value (str): The date and time in string format ('YYYY-MM-DD HH:mm:ss').

        Returns:
            str: The validated and formatted date and time.

        Raises:
            ValueError: If the date and time format is invalid.
        """
        try:
            parsed_datetime = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            formatted_datetime = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if formatted_datetime != value:
                raise ValueError(
                    "Formato de data e hora inválido. Use o formato 'YYYY-MM-DD HH:mm:ss'"
                )
            return value
        except Exception as e:
            logger.error(
                f'Formato de data e hora inválido. Use o formato "YYYY-MM-DD HH:mm:ss" | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                "Formato de data e hora inválido. Use o formato 'YYYY-MM-DD HH:mm:ss'"
            )

    @validator('nuProtocoloAverbacao', pre=True, always=True)
    def validate_nu_registration_protocol_length(cls, value):
        """
        Validates the length of 'nuProtocoloAverbacao'.

        Args:
            value (str): The value of 'nuProtocoloAverbacao'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuProtocoloAverbacao' exceeds the maximum length.
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

    @validator('nuContratoCCB', pre=True, always=True)
    def validate_20_length(cls, value):
        """
        Validates the length of 'nuContratoCCB'.

        Args:
            value (str): The value of 'nuContratoCCB'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuContratoCCB' exceeds the maximum length.
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

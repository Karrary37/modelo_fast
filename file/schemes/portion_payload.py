import logging
from datetime import datetime

from pydantic import BaseModel, validator

logger = logging.getLogger('validacao')


class PortionItem(BaseModel):
    """
    Represents an installment item with the following attributes:

    Attributes:
        nuParcela (int): The installment number.
        dtVencimento (str): The due date of the installment in string format.
        dtPagamento (str, optional): The payment date of the installment in string format. Defaults to an empty string.
        vrParcela (float): The amount of the installment.
        vrPago (float, optional): The amount paid for the installment. Defaults to 0.
        recebidoCedente (bool): A boolean indicating whether the installment was received by the payee.
        paga (bool): A boolean indicating whether the installment has been paid.
    """

    nuParcela: int
    dtVencimento: str
    dtPagamento: str = ''
    vrParcela: float
    vrPago: float = 0
    recebidoCedente: bool
    paga: bool

    @validator(
        'nuParcela',
        'dtVencimento',
        'vrParcela',
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

    @validator('dtVencimento', pre=True, always=True)
    def validate_date(cls, value):
        """
        Validates and formats the due date.

        Args:
            value (str): The due date in string format ('YYYY-MM-DD').

        Returns:
            str: The validated and formatted due date.

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

    @validator('dtPagamento', pre=True, always=True)
    def validate_dt_payament(cls, value):
        """
        Validates and formats the payment date.

        Args:
            value (str): The payment date in string format ('YYYY-MM-DD').

        Returns:
            str: The validated and formatted payment date, or an empty string if not provided.

        Raises:
            ValueError: If the date format is invalid.
        """
        try:
            if value:
                if value == '':
                    return value
                parsed_datetime = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                formatted_datetime = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')

                if formatted_datetime != value:
                    raise ValueError(
                        "Formato de data e hora inválido. Use o formato 'YYYY-MM-DD HH:mm:ss'."
                    )
            return value
        except Exception as e:
            logger.error(
                f'Formato de data e hora inválido. Use o formato "YYYY-MM-DD HH:mm:ss" | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                "Formato de data e hora inválido. Use o formato 'YYYY-MM-DD HH:mm:ss'."
            )

    @validator('vrParcela', 'vrPago', pre=True, always=True)
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

    @validator('recebidoCedente', 'paga', pre=True, always=True)
    def validate_received_transferor(cls, value, values):
        """
        Validates the 'recebidoCedente' and 'paga' fields based on the values of 'vrPago'.

        Args:
            value (bool): The value of 'recebidoCedente' or 'paga'.
            values (dict): The values of all fields in the model.

        Returns:
            bool: The validated boolean value.

        Raises:
            ValueError: If the conditions for 'recebidoCedente' are not met.
        """
        try:
            amount_paid = values.get('vrPago')
            dt_payment = values.get('dtPagamento')

            if amount_paid and dt_payment:
                if value is False and float(amount_paid) > 0:
                    raise ValueError(
                        'O campo deve ser true, pois o pagamento foi efetuado'
                    )
            return value
        except Exception as e:
            logger.error(
                f'O campo deve ser true, pois o pagamento foi efetuado | Campo: {value} | Error: {e}'
            )
            raise ValueError('O campo deve ser true, pois o pagamento foi efetuado')

    @validator('paga', pre=True, always=True)
    def validate_amount_paid(cls, value, values):
        """
        Validates the 'paga' field based on the values of 'vrPago'.

        Args:
            value (bool): The value of 'paga'.
            values (dict): The values of all fields in the model.

        Returns:
            bool: The validated boolean value.

        Raises:
            ValueError: If the conditions for 'paga' are not met.
        """
        try:
            amount_paid = values.get('vrPago')
            received_transferor = values.get('recebidoCedente')
            dt_payament = values.get('dtPagamento')

            if value and received_transferor and dt_payament and float(amount_paid) < 1:
                raise ValueError(
                    'O campo vrPago é obrigatório e deve ser maior que zero'
                )
            return value
        except Exception as e:
            logger.error(
                f'O campo vrPago é obrigatório e deve ser maior que zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('O campo vrPago é obrigatório e deve ser maior que zero')

    @validator('paga', pre=True, always=True)
    def validate_dt_paid(cls, value, values):
        """
        Validates the 'paga' field based on the values of 'recebidoCedente', 'dtPagamento', and 'vrPago'.

        Args:
            value (bool): The value of 'paga'.
            values (dict): The values of all fields in the model.

        Returns:
            bool: The validated boolean value.

        Raises:
            ValueError: If the conditions for 'paga' and 'dtPagamento' are not met.
        """
        try:
            received_transferor = values.get('recebidoCedente')
            dt_payament = values.get('dtPagamento')
            amount_paid = values.get('vrPago')

            if value and received_transferor and float(amount_paid) > 0:
                if not dt_payament or dt_payament == '':
                    raise ValueError('O campo dtPagamento é obrigatório')
            return value
        except Exception as e:
            logger.error(
                f'O campo dtPagamento é obrigatório | Campo: {value} | Error: {e}'
            )
            raise ValueError('O campo dtPagamento é obrigatório')

    @validator('nuParcela', pre=True, always=True)
    def validate_19_length(cls, value):
        """
        Validates the length of 'nuParcela'.

        Args:
            value (str): The value of 'nuParcela'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuParcela' exceeds the maximum length.
        """
        max_length = 19
        try:
            if len(value) > max_length:
                raise ValueError(f'Número dever ter no máximo {max_length} caracteres')

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

    @validator('vrParcela', 'vrPago', pre=True, always=True)
    def validate_vr_portion(cls, value):
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
            logger.error(f'Número decimal inválido | Campo: {value} | Error: {e}')
            raise ValueError('Número decimal inválido')

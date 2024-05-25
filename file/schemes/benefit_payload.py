import logging
from datetime import datetime

from pydantic import BaseModel, validator

logger = logging.getLogger('validacao')


class BenefitItem(BaseModel):
    """
    Represents information about a benefit.

    Attributes:
        matricula (str): Registration number associated with the benefit.
        ufBeneficio (str): State where the benefit is applicable.
        categoriaSituacao (str): Category or status of the benefit.
        tipoBeneficio (str): Type of benefit.
        vrBeneficio (str): Benefit value.
        dtConcessaoBeneficio (str): Date of benefit concession.
        diaUtilPagamento (int): Business day of payment.
        diaUtilFormaPagamento (int): Business day of the payment method.
        mesContracheque (int): Month of the payslip.
        autenticidadeContracheque (str): Payslip authenticity.
        nuMatriculaInstituidor (str): Registration number of the grantor.
        codigo (int): Code associated with the benefit.
    """

    matricula: str
    ufBeneficio: str
    categoriaSituacao: int
    tipoBeneficio: str
    vrBeneficio: str
    dtConcessaoBeneficio: str
    diaUtilPagamento: int
    diaUtilFormaPagamento: int
    mesContracheque: int
    autenticidadeContracheque: str
    nuMatriculaInstituidor: str = ''

    @validator(
        'matricula',
        'ufBeneficio',
        'categoriaSituacao',
        'tipoBeneficio',
        'vrBeneficio',
        'dtConcessaoBeneficio',
        'diaUtilPagamento',
        'diaUtilFormaPagamento',
        'mesContracheque',
        'autenticidadeContracheque',
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

    @validator('vrBeneficio', pre=True, always=True)
    def validate_float(cls, value):
        """
        Validates that a given value is a float.

        Args:
            value (float or str): The value to be validated.

        Raises:
            ValueError: If the value is not a float or if it is less than to zero.

        Returns:
            float or str: The input value if it is a valid positive float.
        """
        try:
            parsed_value = float(value)
            if parsed_value < 0:
                raise ValueError('O valor da renda deve ser maior ou igual zero')
            return value
        except Exception as e:
            logger.error(
                f'O valor da renda deve ser um número  ou igual válido | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor da renda deve ser um número  ou igual válido')

    @validator('dtConcessaoBeneficio', pre=True, always=True)
    def validate_dates(cls, value, values):
        """
        Validates date fields, ensuring they have a valid format and are not in the future.

        Args:
            value (str): The date string to be validated.
            values (dict): A dictionary containing other date values for additional checks.

        Raises:
            ValueError: If the date format is invalid or if the date is in the future.

        Returns:
            str: The input date string if it is a valid date.
        """
        try:
            try:
                parsed_date = datetime.strptime(value, '%Y-%m-%d')
                formatted_date = parsed_date.strftime('%Y-%m-%d')

                if formatted_date != value:
                    raise ValueError(
                        "Formato de data inválido. Use o formato 'AAAA-MM-DD'"
                    )

            except ValueError:
                raise ValueError("Formato de data inválido. Use o formato 'AAAA-MM-DD'")

            if value > datetime.now().strftime('%Y-%m-%d'):
                raise ValueError(
                    'Data inválida, data deve ser menor ou igual que a data atual'
                )
            return value
        except Exception as e:
            logger.error(
                f'Formato deve ser "AAAA-MM-DD" e campo deve ser menor ou igual que a data atual | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                "Formato deve ser 'AAAA-MM-DD' e campo deve ser menor ou igual que a data atual"
            )

    @validator('categoriaSituacao', pre=True, always=True)
    def validate_situation_category(cls, value, values):
        """
        Validates the 'categoriaSituacao' field to ensure it is an integer and within the range {1, 2, 3}.

        Args:
            value (int): The value of the 'categoriaSituacao' field.
            values (dict): The values of all fields in the model.

        Returns:
            int: The validated 'categoriaSituacao' value.

        Raises:
            ValueError: If the 'categoriaSituacao' value is not an integer or not within the valid range.
        """
        try:
            if int(value) not in {1, 2, 3}:
                raise ValueError('Tipo inválido. Deve ser 1, 2 ou 3')

            return value
        except Exception as e:
            logger.error(
                f'Tipo inválido. Deve ser 1, 2 ou 3 | Campo: {value} | Error: {e}'
            )
            raise ValueError('Tipo inválido. Deve ser 1, 2 ou 3')

    @validator('matricula', pre=True, always=True)
    def validate_20_length(cls, value):
        """
        Validates the length of 'nuCNH' or 'matricula'.

        Args:
            value (str): The value of 'matricula'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'matricula' exceeds the maximum length.
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

    @validator('ufBeneficio', pre=True, always=True)
    def validate_char_fild_2_length(cls, value):
        """
        Validates the length of 'ufBeneficio'.

        Args:
            value (str): The value of 'ufBeneficio'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'ufBeneficio' exceeds the maximum length.
        """
        max_length = 2
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('categoriaSituacao', pre=True, always=True)
    def validate_category_situation(cls, value):
        """
        Validates that 'categoriaSituacao' contains only specific numbers.

        Args:
            value (int): The value of 'categoriaSituacao'.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If 'categoriaSituacao' contains an invalid number.
        """
        try:
            if int(value) not in {1, 2, 3}:
                raise ValueError('Valor inválido')

            return value
        except Exception as e:
            logger.error(f'Valor inválid | Campo: {value} | Error: {e}')
            raise ValueError('Valor inválido')

    @validator('tipoBeneficio', pre=True, always=True)
    def validate_50_length(cls, value):
        """
        Validates the length of 'tipoBeneficio' .

        Args:
            value (str): The value of 'tipoBeneficio'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'tipoBeneficio' exceeds the maximum length.
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

    @validator('vrBeneficio', pre=True, always=True)
    def validate_vr_benefit(cls, value):
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
            decimal_value = str(float(value))
            integer_part, decimal_part = str(decimal_value).split('.')

            if (
                len(integer_part) > max_integer_places
                or len(decimal_part) > max_decimal_places
            ):
                raise ValueError(
                    f'O número decimal deve ter no máximo {max_digits} dígitos, com no máximo {max_decimal_places} casas decimais.'
                )
            return value
        except Exception as e:
            logger.error(
                f'O número decimal deve ter no máximo {max_digits} dígitos, com no máximo {max_decimal_places} casas decimais | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                f'O número decimal deve ter no máximo {max_digits} dígitos, com no máximo {max_decimal_places} casas decimais'
            )

    @validator('diaUtilPagamento', 'diaUtilFormaPagamento', pre=True, always=True)
    def validate_integer_less_than_31(cls, value):
        """
        Validates if the value is an integer and less than 31.

        Args:
            value (float): The value to be validated.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If the value is not an integer or is greater than or equal to 31.
        """
        try:
            integer_value = int(value)
            if integer_value < 1 or integer_value > 31:
                raise ValueError(
                    'O valor deve ser um número inteiro menor ou igual a 31'
                )
            return value
        except Exception as e:
            logger.error(
                f'Valor inválido. Deve ser um número inteiro menor ou igual a 31 | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                'Valor inválido. Deve ser um número inteiro menor ou igual a 31'
            )

    @validator('mesContracheque', pre=True, always=True)
    def validate_integer_less_than_12(cls, value):
        """
        Validates if the value is an integer and less than 12.

        Args:
            value (float): The value to be validated.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If the value is not an integer or is greater than or equal to 12.
        """
        try:
            integer_value = int(value)
            if integer_value < 1 or integer_value > 12:
                raise ValueError(
                    'O valor deve ser um número inteiro menor ou igual a 12'
                )
            return value
        except Exception as e:
            logger.error(
                f'Valor inválido. Deve ser um número inteiro menor ou igual a 12 | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                'Valor inválido. Deve ser um número inteiro menor ou igual a 12'
            )

    @validator(
        'autenticidadeContracheque', 'nuMatriculaInstituidor', pre=True, always=True
    )
    def validate_char_fild_200_length(cls, value):
        """
        Validates the length of 'CharField'.

        Args:
            value (str): The value of 'CharField'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'CharField' exceeds the maximum length.
        """
        max_length = 200
        try:
            if value:
                if len(value) > max_length:
                    raise ValueError(
                        f'Campo dever ter no máximo {max_length} caracteres'
                    )
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

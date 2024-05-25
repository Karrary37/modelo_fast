import logging
import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator
from validate_docbr import CPF

from file.schemes.company_payload import CompanyItem

logger = logging.getLogger('validacao')


class ClientItem(BaseModel):
    """
    Represents information about a client.

    Attributes:
        nmCliente (str): Client's name.
        dtNascimento (str): Client's date of birth.
        nmMae (str): Mother's name.
        nmPai (Optional[str]): Father's name (optional).
        nmSexo (str): Client's gender.
        dsEstadoCivil (Optional[str]): Client's marital status (optional).
        nmEmail (Optional[str]): Client's email address (optional).
        nuRG (str): Client's RG (identification document) number.
        nuCpf (str): Client's CPF (Brazilian tax ID) number.
        dtEmissaoRg (str): Date of issuance of the client's RG.
        nmOrgaoEmissorRg (str): Issuing authority of the client's RG.
        nmUfOrgaoEmissorRg (str): State of the issuing authority of the client's RG.
        dsNaturalidade (str): Client's place of birth.
        nmEnderecoResidencialTipo (Optional[str]): Type of client's residential address (optional).
        nmEnderecoResidencialLogradouro (str): Client's residential address street.
        nmEnderecoResidencialNumero (str): Client's residential address number.
        nmEnderecoResidencialComplento (Optional[str]): Client's residential address complement (optional).
        nmEnderecoResidencialBairro (str): Client's residential address neighborhood.
        nmEnderecoResidencialCidade (str): Client's residential address city.
        nmEnderecoResidencialUf (str): Client's residential address state.
        nuEnderecoResidencialCep (str): Client's residential address ZIP code.
        nuDddTelefoneCelular (Optional[str]): Client's mobile phone area code (optional).
        nuDddTelefoneResidencial (Optional[str]): Client's residential phone area code (optional).
        vrRenda (str): Client's income.
        nuCNH (Optional[str]): Client's driver's license number (optional).
        tempoResidencia (Optional[str]): Client's duration of residence (optional).
        tipoLogradouro (Optional[str]): Type of street (optional).
        dsNacionalidade (str): Client's nationality.
        vrPatrimonio (str): Client's assets.
        escolaridade (Optional[str]): Client's education level (optional).
        empresa (Optional[CompanyItem]): Information about the client's associated company (optional).
    """

    nmCliente: str
    dtNascimento: str
    nmMae: str
    nmPai: Optional[str] = ''
    nmSexo: str
    dsEstadoCivil: Optional[str] = ''
    nmEmail: Optional[str] = ''
    nuRG: str
    nuCpf: str
    dtEmissaoRg: str
    nmOrgaoEmissorRg: str
    nmUfOrgaoEmissorRg: str
    dsNaturalidade: str
    nmEnderecoResidencialTipo: Optional[str] = ''
    nmEnderecoResidencialLogradouro: str
    nmEnderecoResidencialNumero: Optional[str] = ''
    nmEnderecoResidencialComplemento: Optional[str] = ''
    nmEnderecoResidencialBairro: str
    nmEnderecoResidencialCidade: str
    nmEnderecoResidencialUf: str
    nuEnderecoResidencialCep: str
    nuDddTelefoneCelular: Optional[str] = ''
    nuDddTelefoneResidencial: Optional[str] = ''
    vrRenda: str
    nuCNH: Optional[str] = ''
    tempoResidencia: Optional[str] = ''
    tipoLogradouro: Optional[str] = ''
    dsNacionalidade: str
    vrPatrimonio: str
    escolaridade: Optional[str] = ''
    empresa: Optional[CompanyItem] = None

    @validator(
        'nmPai',
        'dsEstadoCivil',
        'nmEmail',
        'nmEnderecoResidencialTipo',
        'nmEnderecoResidencialNumero',
        'nmEnderecoResidencialComplemento',
        'nuDddTelefoneCelular',
        'nuDddTelefoneResidencial',
        'nuCNH',
        'tempoResidencia',
        'tipoLogradouro',
        'escolaridade',
        pre=True,
        always=True,
    )
    def validate_none(cls, value):
        if value == 'None' or value is None:
            return ''
        return value

    @validator(
        'nmSexo',
        'nuRG',
        'nmOrgaoEmissorRg',
        'nmUfOrgaoEmissorRg',
        'nmEnderecoResidencialUf',
        'nuEnderecoResidencialCep',
        'dtNascimento',
        'dtEmissaoRg',
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

    @validator('dtEmissaoRg', 'dtNascimento', pre=True, always=True)
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
                raise ValueError('Data inválida, data maior ou igual que a data atual')
            return value
        except Exception as e:
            logger.error(
                f'Formato deve ser "AAAA-MM-DD" e campo deve ser menor ou igual que data atual | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                "Formato deve ser 'AAAA-MM-DD' e campo deve ser menor ou igual que data atual"
            )

    @validator('dtEmissaoRg', pre=True, always=True)
    def validate_emission_rg(cls, value, values):
        """
        Validates the 'dtEmissaoRg' field based on the 'dtNascimento' field.

        Args:
            value (str): The 'dtEmissaoRg' date string to be validated.
            values (dict): A dictionary containing other date values for additional checks.

        Raises:
            ValueError: If the 'dtEmissaoRg' date is not greater than the 'dtNascimento' date.

        Returns:
            str: The input 'dtEmissaoRg' date string if it is valid.
        """
        try:
            birth_date = values['dtNascimento']
            if birth_date > value:
                raise ValueError(
                    "Formato deve ser 'AAAA-MM-DD' e campo deve ser menor ou igual que data atual e a data de emissão do RG deve ser maior ou igual que a data de nascimento"
                )
            return value
        except Exception as e:
            logger.error(
                f"Formato deve ser 'AAAA-MM-DD' e campo deve ser menor ou igual que data atual e a data de emissão do RG deve ser maior ou igual que a data de nascimento | Campo: {value} | Error: {e}"
            )
            raise ValueError(
                "Formato deve ser 'AAAA-MM-DD' e campo deve ser menor ou igual que data atual e a data de emissão do RG deve ser maior ou igual que a data de nascimento"
            )

    @validator('nmEmail', pre=True, always=True)
    def validate_email(cls, value):
        """
        Validates the 'nmEmail' field for a valid email format.

        Args:
            value (str): The email address to be validated.

        Raises:
            ValueError: If the email address has an invalid format.

        Returns:
            str: The input email address if it is valid.
        """
        try:
            if value is not None and not cls.is_valid_email(value):
                raise ValueError('Endereço de email inválido')
            return value
        except Exception as e:
            logger.error(f'Endereço de email inválido | Campo: {value} | Error: {e}')
            raise ValueError('Endereço de email inválido')

    @classmethod
    def is_valid_email(cls, email):
        """
        Helper method to check if an email address has a valid format.

        Args:
            email (str): The email address to be checked.

        Returns:
            bool: True if the email address has a valid format, False otherwise.
        """
        # Expressão regular para verificar o formato do e-mail
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @validator('nuCpf', pre=True, always=True)
    def validate_cpf(cls, value):
        """
        Validates the 'nuCpf' field using a CPF validation function.

        Args:
            value (str): The 'nuCpf' value to be validated.

        Raises:
            ValueError: If the 'nuCpf' value is not a valid CPF.

        Returns:
            str: The input 'nuCpf' value if it is a valid CPF.
        """
        try:
            if not CPF().validate(value):
                raise ValueError('CPF inválido')
            return value
        except Exception as e:
            logger.error(f'CPF inválido | Campo: {value} | Error: {e}')
            raise ValueError('CPF inválido')

    @validator('nuEnderecoResidencialCep', pre=True, always=True)
    def validate_cep(cls, value):
        """
        Validates the 'nuEnderecoResidencialCep' field for a valid CEP format.

        Args:
            value (str): The 'nuEnderecoResidencialCep' value to be validated.

        Raises:
            ValueError: If the 'nuEnderecoResidencialCep' value is not a valid CEP.

        Returns:
            str: The input 'nuEnderecoResidencialCep' value if it is a valid CEP.
        """
        try:
            if len(value) != 8 or not value.isdigit():
                raise ValueError('Número de CEP inválido')
            return value
        except Exception as e:
            logger.error(f'Número de CEP inválido | Campo: {value} | Error: {e}')
            raise ValueError('Número de CEP inválido')

    #
    @validator('vrRenda', pre=True, always=True)
    def validate_positive_float(cls, value):
        """
        Validates that a given value is a positive float.

        Args:
            value (float or str): The value to be validated.

        Raises:
            ValueError: If the value is not a float or if it is less than or equal to zero.

        Returns:
            float or str: The input value if it is a valid positive float.
        """
        try:
            parsed_value = float(value)
            if parsed_value <= 0:
                raise ValueError('O valor da renda deve ser maior que zero')
            return value
        except Exception as e:
            logger.error(
                f'O valor da renda deve ser um número válido | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor da renda deve ser um número válido')

    @validator(
        'nmCliente',
        'nmMae',
        'nmPai',
        'nmEmail',
        'dsNaturalidade',
        'nmEnderecoResidencialLogradouro',
        'nmEnderecoResidencialComplemento',
        'nmEnderecoResidencialBairro',
        'nmEnderecoResidencialCidade',
        'dsNacionalidade',
        'escolaridade',
        pre=True,
        always=True,
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
                f'Campo dever ter no máximo {max_length} caracteres | Payload: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('nmSexo', 'dsEstadoCivil', pre=True, always=True)
    def validate_char_fild_50_length(cls, value):
        """
        Validates the length of 'CharField'.

        Args:
            value (str): The value of 'CharField'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'CharField' exceeds the maximum length.
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

    @validator('nuRG', pre=True, always=True)
    def validate_rg_length(cls, value):
        """
        Validates the length of 'nuRG'.

        Args:
            value (str): The value of 'nuRG'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuRG' exceeds the maximum length.
        """
        max_length = 14
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('nmOrgaoEmissorRg', pre=True, always=True)
    def validate_organ_issuer_rg_length(cls, value):
        """
        Validates the length of 'nmOrgaoEmissorRg'.

        Args:
            value (str): The value of 'nmOrgaoEmissorRg'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nmOrgaoEmissorRg' exceeds the maximum length.
        """
        max_length = 10
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

    @validator('nmUfOrgaoEmissorRg', 'nmEnderecoResidencialUf', pre=True, always=True)
    def validate_char_fild_2_length(cls, value):
        """
        Validates the length of 'nmUfOrgaoEmissorRg'.

        Args:
            value (str): The value of 'nmUfOrgaoEmissorRg'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nmUfOrgaoEmissorRg' exceeds the maximum length.
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

    @validator('nmEnderecoResidencialTipo', pre=True, always=True)
    def validate_tp_adress(cls, value):
        """
        Validates that 'nmEnderecoResidencialTipo' contains only specific numbers.

        Args:
            value (int): The value of 'nmEnderecoResidencialTipo'.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If 'nmEnderecoResidencialTipo' contains an invalid number.
        """
        try:
            if value:
                if int(value) not in {1, 2, 3, 4}:
                    raise ValueError('Valor inválido')

            return value
        except Exception as e:
            logger.error(f'Valor inválido | Campo: {value} | Error: {e}')
            raise ValueError('Valor inválido')

    @validator(
        'nuDddTelefoneCelular', 'nuDddTelefoneResidencial', pre=True, always=True
    )
    def validate_16_length(cls, value):
        """
        Validates the length of 'nuDddTelefoneCelular' or 'nuDddTelefoneResidencial'.

        Args:
            value (str): The value of 'nuDddTelefoneCelular' or 'nuDddTelefoneResidencial'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuDddTelefoneCelular' or 'nuDddTelefoneResidencial' exceeds the maximum length.
        """
        max_length = 16
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('nuCNH', 'tipoLogradouro', pre=True, always=True)
    def validate_20_length(cls, value):
        """
        Validates the length of 'nuCNH' or 'tipoLogradouro'.

        Args:
            value (str): The value of 'nuCNH' or 'tipoLogradouro'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuCNH' or 'tipoLogradouro' exceeds the maximum length.
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

    @validator('tempoResidencia', pre=True, always=True)
    def validate_30_length(cls, value):
        """
        Validates the length of 'tempoResidencia'.

        Args:
            value (str): The value of 'tempoResidencia'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'tempoResidencia' exceeds the maximum length.
        """
        max_length = 30
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('vrRenda', 'vrPatrimonio', pre=True, always=True)
    def validate_decimal_number(cls, value):
        """
        Validates the decimal number to have at most 12 digits with at most 7 decimal places.

        Args:
            value (float): The value of the decimal number.

        Returns:
            float: The validated value.

        Raises:
            ValueError: If the decimal number does not meet the length and precision requirements.
        """
        max_digits = 13
        max_decimal_places = 7
        max_integer_places = 5

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
        except (ValueError, AttributeError):
            raise ValueError('Número decimal inválido.')

        return value

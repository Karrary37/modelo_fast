import logging
from datetime import date, datetime

from pydantic import BaseModel, validator
from validate_docbr import CNPJ, CPF

logger = logging.getLogger('validacao')


class ContractsItem(BaseModel):
    """
    Represents information about a financial contract.

    Attributes:
        tipoProduto (int): Type of financial product associated with the contract.
        nuLote (int): Lot number of the contract.
        nuContratoCedente (str): Contract number assigned by the originator.
        cdContratoTipo (str): Type code of the contract.
        nuCnpjCorrespondente (str, optional): CNPJ of the corresponding entity, if applicable.
        dtDigitacao (str): Date of data entry for the contract.
        dtContrato (str): Date of the contract.
        dtPrimeiroVencimento (str): Date of the first installment due.
        nuCpfAgenteValidador (str): CPF of the validating agent.
        qtParcelasAberto (str): Number of open installments.
        qtParcelasPagas (str): Number of paid installments.
        qtParcelasVencer (str): Number of installments yet to be paid.
        qtParcelasAverbadas (str): Number of installments acknowledged.
        qtParcelasTotal (str): Total number of installments in the contract.
        txCETAno (str): Annual Effective Cost rate.
        txCETMes (str): Monthly Effective Cost rate.
        txEfetivaAno (str): Annual Effective Rate.
        txEfetivaMes (str): Monthly Effective Rate.
        vrAberto (str): Open amount in the contract.
        vrContrato (str): Total amount of the contract.
        vrIof (str): IOF (Tax on Financial Operations) amount.
        vrParcela (str): Amount of each installment.
        vrVencer (str): Amount of installments yet to be paid.
        vrLiberadoCliente (str): Amount released to the client.
        vrTAC (str): Amount associated with TAC (Contract Acquisition Cost).
        vrSeguro (str): Amount associated with insurance.
        nuContratoCCB (str): Contract number in the Central Credit Bureau.
        nuAverbacao (str): Contract number annotation.
        nuCessaoRetornoRegistrador (str, optional): Number related to the registration return of the assignment, if applicable.
        IPOC (str, optional) : Number related to contract operation.
        qiTechUuid (str, optional): UUID4 sent by QITech.

    Note:
        This class is designed to hold detailed information about a financial contract.
        It is structured using the Pydantic BaseModel for data validation and serialization purposes.
    """

    tipoProduto: int
    nuLote: int
    nuContratoCedente: int
    cdContratoTipo: int
    nuCnpjCorrespondente: str = None
    dtDigitacao: str
    dtContrato: str
    dtPrimeiroVencimento: str
    nuCpfAgenteValidador: str
    qtParcelasAberto: str
    qtParcelasPagas: str
    qtParcelasVencer: str
    qtParcelasAverbadas: int
    qtParcelasTotal: int
    txCETAno: str
    txCETMes: str
    txEfetivaAno: str
    txEfetivaMes: str
    vrAberto: str
    vrContrato: str
    vrIof: str
    vrParcela: str
    vrVencer: str
    vrLiberadoCliente: str
    vrTAC: str
    vrSeguro: str
    nuContratoCCB: str
    nuAverbacao: str = ""
    nuCessaoRetornoRegistrador: str = None
    IPOC: str = None
    qiTechUuid: str = None

    @validator(
        'nuLote',
        'nuContratoCedente',
        'cdContratoTipo',
        'nuCpfAgenteValidador',
        'qtParcelasAberto',
        'qtParcelasPagas',
        'qtParcelasVencer',
        'qtParcelasAverbadas',
        'qtParcelasTotal',
        'txCETAno',
        'txCETMes',
        'txEfetivaAno',
        'txEfetivaMes',
        'vrAberto',
        'vrContrato',
        'vrIof',
        'vrParcela',
        'vrVencer',
        'vrLiberadoCliente',
        'vrTAC',
        'vrSeguro',
        'nuContratoCCB',
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

    @validator('dtDigitacao', 'dtContrato', pre=True, always=True)
    def validate_dates_not_future(cls, value):
        """
        Validates that the date is not greater than the current date.

        Args:
            value (str): The date in string format ('YYYY-MM-DD').

        Returns:
            str: The validated date.

        Raises:
            ValueError: If the date is greater than the current date or has an invalid format.
        """
        try:
            parsed_date = datetime.strptime(value, '%Y-%m-%d')

            if parsed_date.date() >= date.today():
                raise ValueError(
                    "A data deve ser anterior a data atual e no formato 'AAAA-MM-DD'"
                )

            return value
        except ValueError:
            raise ValueError(
                "A data deve ser anterior a data atual e no formato 'AAAA-MM-DD'"
            )

    @validator('dtPrimeiroVencimento', pre=True, always=True)
    def validate_first_due_date(cls, value, values):
        """
        Validates that the 'dtPrimeiroVencimento' is not earlier than 'dtContrato'.

        Args:
            value (str): The date in string format ('YYYY-MM-DD').
            values (dict): The values of all fields in the model.

        Returns:
            str: The validated date.

        Raises:
            ValueError: If the 'dtPrimeiroVencimento' is earlier than 'dtContrato' or has an invalid format.
        """
        try:
            if values.get('dtContrato') is not None:
                parsed_due_date = datetime.strptime(value, '%Y-%m-%d')
                parsed_contract_date = datetime.strptime(
                    values.get('dtContrato'), '%Y-%m-%d'
                )

                if parsed_due_date.date() < parsed_contract_date.date():
                    raise ValueError(
                        "A data do primeiro vencimento não pode ser anterior à data do contrato e deve ser no formato 'AAAA-MM-DD'"
                    )

            return value
        except ValueError:
            raise ValueError(
                "A data do primeiro vencimento não pode ser anterior à data do contrato e deve ser no formato 'AAAA-MM-DD'"
            )

    @validator('qtParcelasAberto', 'cdContratoTipo', pre=True, always=True)
    def validate_positive_integer(cls, value):
        """
        Valida que um determinado valor é um número inteiro positivo.

        Argumentos:
            valor (int ou str): O valor a ser validado.

        Levanta:
            ValueError: se o valor não for um número inteiro positivo.

        Retorna:
            int ou str: O valor de entrada se for um número inteiro positivo válido.
        """
        try:
            parsed_value = int(value)
            if parsed_value <= 0:
                raise ValueError('O valor deve ser inteiro e maior que zero')

            return value
        except Exception as e:
            logger.error(
                f'O valor deve ser inteiro e maior que zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor deve ser inteiro e maior que zero')

    @validator('qtParcelasPagas', 'qtParcelasVencer', pre=True, always=True)
    def validate_integer(cls, value):
        """
        Validates that a given value is an integer greater than or equal to zero.

        Args:
            value (int or str): The value to be validated.

        Raises:
            ValueError: If the value is not an integer or if it is less than zero.

        Returns:
            int or str: The input value if it is a valid non-negative integer.
        """
        try:
            parsed_value = int(value)
            if parsed_value < 0:
                raise ValueError('O valor deve ser um inteiro e maior ou igual à zero')
            return value
        except Exception as e:
            logger.error(
                f'O valor deve ser um inteiro e maior ou igual à zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor deve ser um inteiro e maior ou igual à zero')

    @validator(
        'txCETAno',
        'txCETMes',
        'txEfetivaAno',
        'txEfetivaMes',
        'vrAberto',
        'vrContrato',
        'vrParcela',
        'vrVencer',
        pre=True,
        always=True,
    )
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
                raise ValueError('O valor deve ser um decimal e maior que zero')
            return value
        except Exception as e:
            logger.error(
                f'O valor deve ser um decimal e maior que zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor deve ser um decimal e maior que zero')

    @validator('vrIof', 'vrTAC', 'vrSeguro', pre=True, always=True)
    def validate_float(cls, value):
        """
        Validates that a given value is a float greater than or equal to zero.

        Args:
            value (float or str): The value to be validated.

        Raises:
            ValueError: If the value is not a float or if it is less than zero.

        Returns:
            float or str: The input value if it is a valid non-negative float.
        """
        try:
            parsed_value = float(value)
            if parsed_value < 0:
                raise ValueError('O valor deve ser um decimal e maior ou igual à zero')
            return value
        except Exception as e:
            logger.error(
                f'O valor deve ser um decimal e maior ou igual à zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor deve ser um decimal e maior ou igual à zero')

    @validator('vrLiberadoCliente', pre=True, always=True)
    def validate_vr_liberado_cliente(cls, value, values):
        """
        Validates the 'vrLiberadoCliente' field based on the 'tipoProduto' field.

        Args:
            value (float or str): The value to be validated.
            values (dict): A dictionary containing other field values for additional checks.

        Raises:
            ValueError: If the 'vrLiberadoCliente' value is not greater than zero for 'tipoProduto' not equal to 4.

        Returns:
            float or str: The input value if it is a valid 'vrLiberadoCliente'.
        """
        try:
            tp_contract = values.get('cdContratoTipo')
            if tp_contract != 4 and float(value) <= 0:
                raise ValueError('O valor liberado ao cliente deve ser maior que zero')
            return value
        except Exception as e:
            logger.error(
                f'O valor liberado ao cliente deve ser maior que zero | Campo: {value} | Error: {e}'
            )
            raise ValueError('O valor liberado ao cliente deve ser maior que zero')

    @validator('vrLiberadoCliente', pre=True, always=True)
    def validate_vr_liberado_cliente_zero(cls, value, values):
        """
        Validates the 'vrLiberadoCliente' field based on the 'tipoProduto' field.

        Args:
            value (float or str): The value to be validated.
            values (dict): A dictionary containing other field values for additional checks.

        Raises:
            ValueError: If the 'vrLiberadoCliente' value is not greater than or equal zero for 'tipoProduto' equal to 4.

        Returns:
            float or str: The input value if it is a valid 'vrLiberadoCliente'.
        """
        try:
            tp_contract = values.get('cdContratoTipo')
            if tp_contract == 4 and float(value) < 0:
                raise ValueError(
                    'O valor liberado ao cliente deve ser maior ou igual a zero'
                )
            return value
        except Exception as e:
            logger.error(
                f'O valor liberado ao cliente deve ser maior ou igual a zero | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                'O valor liberado ao cliente deve ser maior ou igual a zero'
            )

    @validator('nuCnpjCorrespondente', pre=True, always=True)
    def validate_cnpj(cls, value):
        """
        Validates the 'nuCnpjCorrespondente' field using a CNPJ validation function.

        Args:
            value (str): The CNPJ value to be validated.

        Raises:
            ValueError: If the 'nuCnpjCorrespondente' value is not a valid CNPJ.

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

    @validator('nuCpfAgenteValidador', pre=True, always=True)
    def validate_cpf(cls, value):
        """
        Validates the 'nuCpfAgenteValidador' field using a CPF validation function.

        Args:
            value (str): The CPF value to be validated.

        Raises:
            ValueError: If the 'nuCpfAgenteValidador' value is not a valid CPF.

        Returns:
            str: The input value if it is a valid CPF.
        """
        try:
            if not CPF().validate(value):
                raise ValueError('CPF inválido')
            return value
        except Exception as e:
            logger.error(f'CPF inválido | Campo: {value} | Error: {e}')
            raise ValueError('CPF inválido')

    @validator('qtParcelasTotal', pre=True, always=True)
    def validate_equal_parcel_counts(cls, value, values):
        """
        Validates that 'qtParcelasTotal' and 'qtParcelasAverbadas' are equal.

        Args:
            value (int): The value of 'qtParcelasTotal'.
            values (dict): The values of all fields in the model.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If 'qtParcelasTotal' is not equal to 'qtParcelasAverbadas'.
        """
        try:
            if int(value) != int(values.get('qtParcelasAverbadas')):
                raise ValueError(
                    'Campos devem ser iguais. qtParcelasAverbadas e qtParcelasTotal'
                )
            return value
        except Exception as e:
            logger.error(
                f'Campos devem ser iguais. qtParcelasAverbadas e qtParcelasTotal | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                'Campos devem ser iguais. qtParcelasAverbadas e qtParcelasTotal'
            )

    @validator('tipoProduto', pre=True, always=True)
    def validate_tp_product(cls, value):
        """
        Validates that 'tipoProduto' contains only specific numbers.

        Args:
            value (int): The value of 'tipoProduto'.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If 'tipoProduto' contains an invalid number.
        """
        try:
            if int(value) not in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15}:
                raise ValueError('Valor inválido')

            return value
        except Exception as e:
            logger.error(f'Valor inválido | Campo: {value} | Error: {e}')
            raise ValueError('Valor inválido')

    @validator(
        'nuLote', 'qtParcelasAverbadas', 'qtParcelasTotal', pre=True, always=True
    )
    def validate_nu_batch_length(cls, value):
        """
        Validates the length of 'nuLote'.

        Args:
            value (str): The value of 'nuLote'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuLote' exceeds the maximum length.
        """
        max_length = 19
        try:
            if len(value) > max_length or int(value) <= 0:
                raise ValueError(
                    f'Número dever ser maior que zero e ter no máximo {max_length} caracteres'
                )
            return value
        except Exception as e:
            logger.error(
                f'Número dever ser maior que zero e ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(
                f'Número dever ser maior que zero e ter no máximo {max_length} caracteres'
            )

    @validator('nuContratoCedente', pre=True, always=True)
    def validate_nu_assignment_agreement_length(cls, value):
        """
        Validates the length of 'nuContratoCedente'.

        Args:
            value (str): The value of 'nuContratoCedente'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuContratoCedente' exceeds the maximum length.
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

    @validator('nuContratoCedente', pre=True, always=True)
    def validate_nu_assignment_agreement_greater_than_zero(cls, value):
        """
        Validates the type of 'nuContratoCedente'.

        Args:
            value (str): The value of 'nuContratoCedente'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuContratoCedente' greater than zero.
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

    @validator('cdContratoTipo', pre=True, always=True)
    def validate_tp_contract(cls, value):
        """
        Validates that 'tipoProduto' contains only specific numbers.

        Args:
            value (int): The value of 'tipoProduto'.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If 'tipoProduto' contains an invalid number.
        """
        try:
            if int(value) not in {1, 2, 3, 4, 5}:
                raise ValueError('Valor inválido')

            return value
        except Exception as e:
            logger.error(f'Valor inválido | Campo: {value} | Error: {e}')
            raise ValueError('Valor inválido')

    @validator(
        'txCETAno',
        'txCETMes',
        'txEfetivaAno',
        'txEfetivaMes',
        'vrAberto',
        'vrContrato',
        'vrParcela',
        'vrVencer',
        'vrLiberadoCliente',
        'vrTAC',
        'vrSeguro',
        pre=True,
        always=True,
    )
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

    @validator('nuContratoCCB', 'nuAverbacao', pre=True, always=True)
    def validate_nu_contract_ccb_length(cls, value):
        """
        Validates the length of 'nuContratoCCB' and 'nuAverbacao'.

        Args:
            value (str): The value of 'nuContratoCCB' and 'nuAverbacao'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuContratoCCB' and 'nuAverbacao' exceeds the maximum length.
        """
        max_length = 20
        if value != "":
            try:
                if len(value) > max_length:
                    raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
                return value
            except Exception as e:
                logger.error(
                    f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
                )
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
        return value

    @validator('nuCessaoRetornoRegistrador', pre=True, always=True)
    def validate_nu_assignment_return_registrar_length(cls, value):
        """
        Validates the length of 'nuCessaoRetornoRegistrador'.

        Args:
            value (str): The value of 'nuCessaoRetornoRegistrador'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nuCessaoRetornoRegistrador' exceeds the maximum length.
        """
        if value is None:
            return ''
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

    @validator('IPOC', pre=True, always=True)
    def validate_ipoc_length(cls, value):
        """
        Validates the length of 'IPOC'.

        Args:
            value (str): The value of 'IPOC'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'IPOC' exceeds the maximum length.
        """
        if value is None or value == '':
            return ''
        max_length = 100
        try:
            if len(value) > max_length:
                raise ValueError(
                    f'Campo IPOC dever ter no máximo {max_length} caracteres'
                )
            return value
        except Exception as e:
            logger.error(
                f'Campo deve ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo IPOC dever ter no máximo {max_length} caracteres')
    
    @validator('qiTechUuid', pre=True, always=True)
    def validate_qi_tech_uuid_length(cls, value):
        """
        Validates the length of 'qiTechUuid'.

        Args:
            value (str): The value of 'qiTechUuid'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'qiTechUuid' is different from the length of 36.
        """
        if value is None or value == '':
            return ''
        length = 36
        try:
            if len(value) != length:
                raise ValueError(
                    f'Campo qiTechUuid dever ter {length} caracteres'
                )
            return value
        except Exception as e:
            logger.error(
                f'Campo deve ter {length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo qiTechUuid dever {length} caracteres')

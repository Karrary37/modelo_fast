import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

logger = logging.getLogger('validacao')


class CompanyItem(BaseModel):
    """
    Represents information about a company associated with a client.

    Attributes:
        empresa (Optional[str]): Company name (optional).
        profissao (Optional[str]): Profession within the company (optional).
        dtAdmissao (Optional[str]): Date of employment (optional).
        ramoAtividade (Optional[str]): Business activity or sector (optional).
        tipoProfissao (Optional[str]): Type of profession (optional).
        ramoAtividadeOr (Optional[str]): Alternative business activity or sector (optional).
        tipoProfissaoOr (Optional[str]): Alternative type of profession (optional).
        nmCargo (Optional[str]): Job title within the company (optional).
        codOrgao (Optional[str]): Organization code (optional).
        codUPag (Optional[str]): Payroll code (optional).
    """

    empresa: Optional[str] = None
    profissao: Optional[str] = None
    dtAdmissao: Optional[str] = None
    ramoAtividade: Optional[str] = None
    tipoProfissao: Optional[str] = None
    ramoAtividadeOr: Optional[str] = None
    tipoProfissaoOr: Optional[str] = None
    nmCargo: Optional[str] = None
    codOrgao: Optional[str] = None
    codUPag: Optional[str] = None

    @validator(
        'empresa',
        'profissao',
        'dtAdmissao',
        'ramoAtividade',
        'tipoProfissao',
        'tipoProfissaoOr',
        'nmCargo',
        'codOrgao',
        'codUPag',
        pre=True,
        always=True,
    )
    def validate_none(cls, value):
        if value == 'None' or value is None:
            return ''
        return value

    @validator('dtAdmissao', pre=True, always=True)
    def validate_dates_business(cls, value):
        """
        Validate the date format for the 'dtAdmissao' field.

        Args:
            value (str): The value of the 'dtAdmissao' field.

        Returns:
            str: The validated 'dtAdmissao' value.

        Raises:
            ValueError: If the date format is invalid (not in the 'AAAA-MM-DD' format).
        """
        try:
            parsed_date = datetime.strptime(value, '%Y-%m-%d')
            formatted_date = parsed_date.strftime('%Y-%m-%d')

            if formatted_date != value:
                raise ValueError("Formato de data inválido. Use o formato 'AAAA-MM-DD'")
        except ValueError:
            raise ValueError("Formato de data inválido. Use o formato 'AAAA-MM-DD'")

        return value

    @validator(
        'empresa',
        'profissao',
        'ramoAtividade',
        'tipoProfissao',
        'ramoAtividadeOr',
        'tipoProfissaoOr',
        'nmCargo',
        'nmCargo',
        'codOrgao',
        'codUPag',
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
                        f'Campo dever ter no máximo {max_length} caracteres.'
                    )
                return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres. | Payload: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres.')

import base64
import logging
import re

from typing import Optional
from pydantic import BaseModel, validator

logger = logging.getLogger('validacao')


class AttachmentsItem(BaseModel):
    """
    Pydantic model representing an attachment item.

    Attributes:
        cdAnexoTipo (int): Attachment type code.
        nmAnexo (str): Attachment name.
        nmAnexoExtensao (str): Attachment file extension.
        anexoBase64 (str): Base64-encoded content of the attachment.
    """

    cdAnexoTipo: int
    nmAnexo: str
    nmAnexoExtensao: str
    anexoBase64: Optional[str] = None
    nmUrl: Optional[str] = None

    @validator(
        'nmAnexo',
        'nmAnexoExtensao',
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

    @validator('cdAnexoTipo', pre=True, always=True)
    def validate_tp_attachment(cls, value):
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
            if int(value) not in {1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 22}:
                raise ValueError('Valor inválido')
            return value
        except Exception as e:
            logger.error(f'Valor inválido | Campo: {value} | Error: {e}')
            raise ValueError('Valor inválido')

    @validator('nmAnexo', pre=True, always=True)
    def validate_300_length(cls, value):
        """
        Validates the length of 'nmAnexo'.

        Args:
            value (str): The value of 'nmAnexo'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nmAnexo' exceeds the maximum length.
        """
        max_length = 300
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('nmAnexoExtensao', pre=True, always=True)
    def validate_10_length(cls, value):
        """
        Validates the length of 'nmAnexoExtensao'.

        Args:
            value (str): The value of 'nmAnexoExtensao'.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If 'nmAnexoExtensao' exceeds the maximum length.
        """
        max_length = 10
        try:
            if len(value) > max_length:
                raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')
            return value
        except Exception as e:
            logger.error(
                f'Campo dever ter no máximo {max_length} caracteres | Campo: {value} | Error: {e}'
            )
            raise ValueError(f'Campo dever ter no máximo {max_length} caracteres')

    @validator('anexoBase64')
    def validate_base64(cls, value):
        """
        Validates if the string is a valid Base64 encoded string.

        Args:
            value (str): The string to be validated.

        Raises:
            ValueError: If the string is not a valid Base64 string.

        Returns:
            str: The input string if it is a valid Base64 string.
        """
        try:
            base64.b64decode(value)
        except ValueError:
            raise ValueError('AnexoBase64 não é um Base64 válido')
        return value

    @validator('nmUrl')
    def validate_url(cls, value):
        """
        Validates that the provided URL is valid.

        Args:
            value (str): The URL to be validated.

        Raises:
            ValueError: If the URL is not valid.

        Returns:
            str: The input URL if it is valid.
        """
        url_regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE,
        )
        if not re.match(url_regex, value):
            raise ValueError('URL inválida')
        return value

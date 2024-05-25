import logging
from typing import List, Optional

from pydantic import BaseModel, validator

from file.schemes import (
    AttachmentsItem,
    BankDetailsWithdrawnItem,
    BenefitItem,
    ClientItem,
    ContractsItem,
    PortionItem,
    RepresentativeItem,
    ReturnFGTSItem,
    SourceContractsItem,
)

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

    contrato: ContractsItem
    cliente: ClientItem
    representante: Optional[RepresentativeItem] = None
    beneficio: Optional[BenefitItem] = None
    parcela: List[PortionItem]
    contratosOrigem: Optional[List[SourceContractsItem]] = None
    dadosBancariosSacado: BankDetailsWithdrawnItem
    anexos: Optional[List[AttachmentsItem]] = None
    retornoFGTS: Optional[ReturnFGTSItem] = None
    operacao: str
    cessionario: str

    @validator(
        'operacao',
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

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_client_education(cls, value, values):
        """
        Validates the 'cliente' field based on the associated 'contrato' field.

        Args:
            cls: The class containing the validator.
            value: The value of the 'cliente' field being validated.
            values: A dictionary containing all the values of the Pydantic model.

        Raises:
            ValueError: If 'escolaridade' is not provided for contracts of 'tipoProduto' equal to 4.

        Returns:
            ClientItem: The validated 'cliente' value if the validation passes.
        """
        try:
            error = False
            try:
                contract = values.get('contrato')
                education = value.get('escolaridade')
            except Exception as e:
                error = True
                logger.info(
                    f'Não encotrado valores de escolaridade | Payload: {values} | Error: {e}'
                )
                pass
            if error is False:
                if contract.tipoProduto == 4 and not education:
                    raise ValueError(
                        'Escolaridade é obrigatória para contratos do tipoProduto 4'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Escolaridade é obrigatória para contratos do tipoProduto 4 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Escolaridade é obrigatória para contratos do tipoProduto 4'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_name_bussiness(cls, value, values):
        """
        Validate the 'empresa' field in the 'cliente' object.

        Ensure that the 'empresa' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'empresa' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                bussiness = value.get('empresa').get('empresa')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de empresa | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not bussiness:
                    raise ValueError(
                        'Campo empresa no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Campo empresa no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                f' | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo empresa no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_profession_bussiness(cls, value, values):
        """
        Validate the 'profissao' field in the 'empresa' object.

        Ensure that the 'profissao' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'profissao' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                profession = value.get('empresa').get('profissao')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de profissao | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not profession:
                    raise ValueError(
                        'Campo profissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                    )
                return value
        except Exception as e:
            logger.error(
                f'Campo profissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                f' | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo profissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_dt_admission_bussiness(cls, value, values):
        """
        Validate the 'dtAdmissao' field in the 'empresa' object.

        Ensure that the 'dtAdmissao' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'dtAdmissao' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                dt_admission = value.get('empresa').get('dtAdmissao')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de dtAdmissao | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not dt_admission:
                    raise ValueError(
                        'Campo dtAdmissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Campo dtAdmissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13. | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo dtAdmissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_activity_branch_payload_bussiness(cls, value, values):
        """
        Validate the 'ramoAtividade' field in the 'empresa' object.

        Ensure that the 'ramoAtividade' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'ramoAtividade' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                activity_branch = value.get('empresa').get('ramoAtividade')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de ramoAtividade | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not activity_branch:
                    raise ValueError(
                        'Campo ramoAtividade no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Campo ramoAtividade no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13. | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo ramoAtividade no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_tp_profession_bussiness(cls, value, values):
        """
        Validate the 'tipoProfissao' field in the 'empresa' object.

        Ensure that the 'tipoProfissao' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'tipoProfissao' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                tp_profession = value.get('empresa').get('tipoProfissao')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de tipoProfissao | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not tp_profession:
                    raise ValueError(
                        'Campo tipoProfissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Não encotrado valores de tipoProfissao | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo tipoProfissao no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_activity_or_branch_payload_bussiness(cls, value, values):
        """
        Validate the 'ramoAtividadeOr ' field in the 'empresa' object.

        Ensure that the 'ramoAtividadeOr ' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'ramoAtividadeOr ' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                activity_branch = value.get('empresa').get('ramoAtividadeOr')
            except Exception as e:
                logger.info(
                    logger.info(
                        f'Não encotrado valores de ramoAtividadeOr | Payload: {values} | Error: {e}'
                    )
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not activity_branch:
                    raise ValueError(
                        'Campo ramoAtividadeOr no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11'
                        ' e 13.'
                    )

                return value
        except Exception as e:
            logger.error(
                'Campo ramoAtividadeOr no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e'
                f' 13. | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo ramoAtividadeOr no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e'
                ' 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_tp_profession_or_bussiness(cls, value, values):
        """
        Validate the 'tipoProfissaoOr' field in the 'empresa' object.

        Ensure that the 'tipoProfissaoOr' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'tipoProfissaoOr' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                tp_profession = value.get('empresa').get('tipoProfissaoOr')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de tipoProfissaoOr | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not tp_profession:
                    raise ValueError(
                        'Campo tipoProfissaoOr no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                    )

            return value
        except Exception as e:
            logger.error(
                'Campo tipoProfissaoOr no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                f' 8 e categoriaSituacao igual a 3 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo tipoProfissaoOr no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_nm_office_bussiness(cls, value, values):
        """
        Validate the 'nmCargo' field in the 'empresa' object.

        Ensure that the 'nmCargo' field is mandatory for contracts with 'tipoProduto' values
        8, 9, 10, 11, and 13.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'nmCargo' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                nm_office = value.get('empresa').get('nmCargo')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de codOrgao | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto in {8, 9, 10, 11, 13} and not nm_office:
                    raise ValueError(
                        'Campo nmCargo no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Campo nmCargo no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13. | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo nmCargo no array de empresa é obrigatória para contratos do tipoProduto 8, 9, 10, 11 e 13.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_cd_institution_bussiness(cls, value, values):
        """
        Validate the 'codOrgao' field in the 'empresa' object.

        Ensure that the 'codOrgao' field is mandatory for contracts with 'tipoProduto' value
        8.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'nmCargo' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                cd_institution_empresa = value.get('empresa', None)
                cd_institution = cd_institution_empresa.get('codOrgao')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de codOrgao | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto == 8 and not cd_institution:
                    raise ValueError(
                        'Campo codOrgao no array de empresa é obrigatória para contrato do tipoProduto 8.'
                    )

                return value
        except Exception as e:
            logger.error(
                'Campo codOrgao no array de empresa é obrigatória para contrato do tipoProduto 8.'
                f' 8 e categoriaSituacao igual a 3 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo codOrgao no array de empresa é obrigatória para contrato do tipoProduto 8.'
            )

    @validator('cliente', pre=True, always=True, check_fields=False)
    def validate_cd_upag_bussiness(cls, value, values):
        """
        Validate the 'codUPag' field in the 'empresa' object.

        Ensure that the 'codUPag' field is mandatory for contracts with 'tipoProduto' value
        8.

        Args:
            value (Any): The value of the 'cliente' field.
            values (Dict[str, Any]): The values of all fields in the 'cliente' object.

        Returns:
            Any: The validated 'cliente' object.

        Raises:
            ValueError: If the 'codUPag' field is missing for the specified contract types.
        """
        try:
            try:
                contract = values.get('contrato')
                cd_upag = value.get('empresa').get('codUPag')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de cd_upag | Payload: {values} | Error: {e}'
                )
                pass
            if contract:
                if contract.tipoProduto == 8 and not cd_upag:
                    raise ValueError(
                        'Campo codUPag no array de empresa é obrigatória para contrato do tipoProduto 8.'
                    )

            return value
        except Exception as e:
            logger.error(
                'Campo codUPag no array de empresa é obrigatória para contrato do tipoProduto 8. |'
                f' Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo codUPag no array de empresa é obrigatória para contrato do tipoProduto 8.'
            )

    @validator('representante', pre=True, always=True, check_fields=False)
    def validate_representative(cls, value, values):
        """
        Validate the 'representante' field based on the contract type.

        Args:
            value: The value of the 'representante' field.
            values: A dictionary containing all the values of the model.

        Returns:
            The validated 'representante' value.

        Raises:
            ValueError: If the 'representante' field is missing for contract types 2 and 3.
        """
        try:
            contract = values.get('contrato')
            if contract:
                if contract.tipoProduto in {2, 3} and not value:
                    raise ValueError(
                        'Array de representante é obrigatória para contrato do tipoProduto 2 e 3'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Array de representante é obrigatória para contrato do tipoProduto 2 e 3 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Array de representante é obrigatória para contrato do tipoProduto 2 e 3'
            )

    @validator('beneficio', pre=True, always=True, check_fields=False)
    def validate_beneficiary(cls, value, values):
        """
        Validate the 'beneficio' field based on the contract type.

        Args:
            value: The value of the 'beneficio' field.
            values: A dictionary containing all the values of the model.

        Returns:
            The validated 'beneficio' value.

        Raises:
            ValueError: If the 'beneficio' field is missing for contract types 2 and 3.
        """
        try:
            contract = values.get('contrato')
            if contract:
                if contract.tipoProduto != 1 and not value:
                    raise ValueError(
                        'Array de beneficio é obrigatória para contrato do tipoProduto diferente de 1'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Array de beneficio é obrigatória para contrato do tipoProduto diferente de 1 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Array de beneficio é obrigatória para contrato do tipoProduto diferente de 1'
            )

    @validator('beneficio', pre=True, always=True, check_fields=False)
    def validate_nu_registration_founder(cls, value, values):
        """
        Validates the 'nuMatriculaInstituidor' field in the 'beneficio' array based on the values of 'contrato'
        and 'categoriaSituacao' fields.

        Args:
            value (dict): The value of the 'beneficio' array.
            values (dict): The values of all fields in the model.

        Returns:
            dict: The validated 'beneficio' array.

        Raises:
            ValueError: If 'nuMatriculaInstituidor' is required for a specific contract type and situation category.
        """
        try:
            if value:
                contract = values.get('contrato')
                nu_registration_founder = value.get('nuMatriculaInstituidor')
                situation_category = value.get('categoriaSituacao')

                if contract:
                    if (
                        contract.tipoProduto == 8
                        and not nu_registration_founder
                        and int(situation_category) == 3
                    ):
                        raise ValueError(
                            'Campo nuMatriculaInstituidor no array de beneficio é obrigatória para contrato do tipoProduto'
                            ' 8 e categoriaSituacao igual a 3'
                        )
                    return value
        except Exception as e:
            logger.error(
                'Campo nuMatriculaInstituidor no array de beneficio é obrigatória para contrato do tipoProduto'
                f' 8 e categoriaSituacao igual a 3 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo nuMatriculaInstituidor no array de beneficio é obrigatória para contrato do tipoProduto 8 e'
                ' categoriaSituacao igual a 3'
            )

    @validator('contratosOrigem', pre=True, always=True, check_fields=False)
    def validate_source_contracts_item(cls, value, values):
        """
        Validate the 'contratosOrigem' field based on the contract type.

        Args:
            value: The value of the 'contratosOrigem' field.
            values: A dictionary containing all the values of the model.

        Returns:
            The validated 'contratosOrigem' value.

        Raises:
            ValueError: If the 'contratosOrigem' field is missing for contract types 2 and 3.
        """
        try:
            contract = values.get('contrato')
            if contract:
                if contract.tipoProduto in {2, 3, 4} and not value:
                    raise ValueError(
                        'Array de contratosOrigem é obrigatória para contrato do tipoProduto iguais a 2, 3 e 4'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Array de contratosOrigem é obrigatória para contrato do tipoProduto iguais a 2, 3 e 4 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Array de contratosOrigem é obrigatória para contrato do tipoProduto iguais a 2, 3 e 4'
            )

    @validator('dadosBancariosSacado', pre=True, always=True, check_fields=False)
    def validate_bank_details_withdrawn_item_cpf(cls, value, values):
        """
        Validates the 'nuCpfTitular' field within the 'dadosBancariosSacado' array.

        Args:
            cls: The class containing the validator.
            value (dict): The value of the 'dadosBancariosSacado' field to be validated.
            values (dict): The values of all fields in the model.

        Raises:
            ValueError: If 'nuCpfTitular' is missing in the 'dadosBancariosSacado' array for contracts
                        other than those with 'tipoProduto' equal to 5.

        Returns:
            dict: The validated 'dadosBancariosSacado' value.
        """
        try:
            try:
                contract = values.get('contrato')
                cpf = value.get('nuCpfTitular')
            except Exception as e:
                logger.info(
                    f'Não encotrado valores de nuCpfTitular | Payload: {values} | Error: {e}'
                )
                pass

            if contract:
                if contract.tipoProduto != 5 and not cpf:
                    raise ValueError(
                        'Campo nuCpfTitular no array de dadosBancariosSacado é obrigatória para todos contratos exceto do tipoProduto igual a 5.'
                    )
                if contract.tipoProduto == 5 and not cpf:
                    value['nuCpfTitular'] = None
                return value
        except Exception as e:
            logger.error(
                f'Campo nuCpfTitular no array de dadosBancariosSacado é obrigatória para todos contratos exceto do tipoProduto igual a 5. | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo nuCpfTitular no array de dadosBancariosSacado é obrigatória para todos contratos exceto do tipoProduto igual a 5.'
            )

    @validator('dadosBancariosSacado', pre=True, always=True, check_fields=False)
    def validate_bank_details_withdrawn_item_cnpj(cls, value, values):
        """
        Validates the 'nuCnpjTitular' field within the 'dadosBancariosSacado' array.

        Args:
            cls: The class containing the validator.
            value (dict): The value of the 'dadosBancariosSacado' field to be validated.
            values (dict): The values of all fields in the model.

        Raises:
            ValueError: If 'nuCnpjTitular' is missing in the 'dadosBancariosSacado' array for contracts
                        other than those with 'tipoProduto' equal to 5.

        Returns:
            dict: The validated 'dadosBancariosSacado' value.
        """
        try:
            contract = values.get('contrato')
            cnpj = value.get('nuCnpjTitular')

            if contract:
                if contract.tipoProduto == 5 and not cnpj:
                    raise ValueError(
                        'Campo nuCnpjTitular no array de dadosBancariosSacado é obrigatória para contratos do tipoProduto igual a 5.'
                    )
                if contract.tipoProduto != 5 and not cnpj:
                    value['nuCnpjTitular'] = None
                return value
        except Exception as e:
            logger.error(
                f'Campo nuCnpjTitular no array de dadosBancariosSacado é obrigatória para contratos do tipoProduto igual a 5. | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Campo nuCnpjTitular no array de dadosBancariosSacado é obrigatória para todos contratos do tipoProduto igual a 5.'
            )

    @validator('retornoFGTS', pre=True, always=True, check_fields=False)
    def validate_return_fgts_item(cls, value, values):
        """
        Validates the 'retornoFGTS' array based on the contract type.

        Args:
            cls: The class containing the validator.
            value (list): The value of the 'retornoFGTS' field to be validated.
            values (dict): The values of all fields in the model.

        Raises:
            ValueError: If 'retornoFGTS' array is missing for contracts with 'tipoProduto' equal to 1.

        Returns:
            list: The validated 'retornoFGTS' array.
        """
        try:
            contract = values.get('contrato')
            if contract:
                if contract.tipoProduto == 1 and not value:
                    raise ValueError(
                        'Array de retornoFGTS é obrigatória para contrato do tipoProduto igual a 1'
                    )

                return value
        except Exception as e:
            logger.error(
                f'Array de retornoFGTS é obrigatória para contrato do tipoProduto igual a 1 | Payload: {values} | Error: {e}'
            )
            raise ValueError(
                'Array de retornoFGTS é obrigatória para contrato do tipoProduto igual a 1'
            )

import json


def process_payload(payload):
    """
    Process the given payload dictionary.

    This function converts the payload dictionary to a JSON string, then loads it back into a dictionary.
    It retrieves specific fields from this dictionary and removes them if their values are `None`.

    Args:
        payload (dict): The payload dictionary containing contract data.

    Returns:
        dict: The processed payload dictionary without the fields having `None` values.
    """
    data = json.dumps(payload.dict())
    data = json.loads(data)

    cliente = data.get('cliente')
    representative = data.get('representante')
    benefit = data.get('beneficio')
    origin_contracts = data.get('contratosOrigem')
    bank_data_payer = data.get('dadosBancariosSacado')
    attachments = data.get('anexos')
    fgts_return = data.get('retornoFGTS')

    if representative is None or representative == {}:
        del data['representante']
    if benefit is None or benefit == {}:
        del data['beneficio']
    if origin_contracts is None or origin_contracts == []:
        del data['contratosOrigem']
    if bank_data_payer is None or bank_data_payer == {}:
        del data['dadosBancariosSacado']
    if attachments is None or attachments == []:
        del data['anexos']
    if fgts_return is None or fgts_return == {}:
        del data['retornoFGTS']
    if cliente:
        if cliente.get('empresa') is None or cliente.get('empresa') == 'None':
            del data['cliente']['empresa']

    return data

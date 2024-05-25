import hashlib
import json


def make_hash(data):
    """
    Generates a hash value for the provided data.

    Parameters:
        data (any): The data to be hashed.

    Returns:
        str: The hash value in hexadecimal format.
    """
    # Convert the data to a sorted JSON string

    serialized_data = json.dumps(data, sort_keys=True)

    # Calculate the hash of the JSON string using SHA-256 (you can choose another algorithm if preferred)
    hash_object = hashlib.sha256(serialized_data.encode())

    # Return the hash in hexadecimal format
    return hash_object.hexdigest()


def make_duplicity_hash(nu_contrato_facta: str, nu_contrato_ccb: str):
    """
    Generate specific duplicity hash.
    """
    return make_hash(
        {
            'nuContratoFacta': str(nu_contrato_facta),
            'nuContratoCCB': str(nu_contrato_ccb),
        }
    )


def make_eligiblity_hash(nu_cpf: str, dt_contrato: str, vr_total: float, prazo: int):
    """
    Generate specific eligiblity hash.
    """
    return make_hash(
        {
            'nuCpf': nu_cpf,
            'dtContrato': dt_contrato,
            'vrTotal': vr_total,
            'prazo': prazo,
        }
    )


def generate_hash(
    payload,
):
    """
    Generates duplicity and eligibility hashes for a given contract payload.

    Parameters:
        payload (dict): The contract payload containing relevant data for hash generation.

    Returns:
        tuple: A tuple containing the duplicity hash and eligibility hash.
    """
    total_amount = 0
    for installment in payload.parcela:
        vr_parcela = float(installment.vrParcela if installment.vrParcela else 0)
        total_amount += vr_parcela

    duplicity_hash = make_duplicity_hash(
        payload.contrato.nuContratoCedente, payload.contrato.nuContratoCCB
    )
    eligibility_hash = make_eligiblity_hash(
        payload.cliente.nuCpf,
        payload.contrato.dtContrato,
        total_amount,
        len(payload.parcela),
    )

    return duplicity_hash, eligibility_hash


def generate_hash_oferta(
    payload,
):
    """
    Generates duplicity and eligibility hashes for a given contract payload.

    Parameters:
        payload (dict): The contract payload containing relevant data for hash generation.

    Returns:
        tuple: A tuple containing the duplicity hash and eligibility hash.
    """
    total_amount = 0
    for installment in payload['parcela']:
        vr_parcela = float(installment['vrParcela'] if installment['vrParcela'] else 0)
        total_amount += vr_parcela

    duplicity_hash = make_duplicity_hash(
        payload['contrato']['nuContratoCedente'], payload['contrato']['nuContratoCCB']
    )
    eligibility_hash = make_eligiblity_hash(
        payload['cliente']['nuCpf'],
        payload['contrato']['dtContrato'],
        total_amount,
        len(payload['parcela']),
    )

    return duplicity_hash, eligibility_hash

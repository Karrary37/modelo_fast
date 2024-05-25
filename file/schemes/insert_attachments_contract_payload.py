from typing import List
from pydantic import BaseModel
from .attachments_payload import AttachmentsItem


class InsertAttachmentsContractsPayload(BaseModel):
    nuContratoCedente: str
    nuContratoCCB: str
    anexos: List[AttachmentsItem]

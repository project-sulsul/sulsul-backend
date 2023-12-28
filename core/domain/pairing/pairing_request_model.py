import peewee

from core.domain.base_entity import BaseEntity


class PairingRequest(BaseEntity):
    type = peewee.CharField(max_length=10, null=False)  # 술, 안주
    subtype = peewee.CharField(max_length=100, null=True)  # 육류, 마른안주 등
    name = peewee.CharField(max_length=100, null=False, unique=True)

    class Meta:
        table_name = "pairing_request"

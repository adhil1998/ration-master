from common.functions import ChoiceAdapter


class UnitType(ChoiceAdapter):
    KG = 100
    LITRE = 200
    PACK = 300


class TokenStatus(ChoiceAdapter):
    INITIATED = 100
    COMPLETED = 200
    CANCELED = 300


MAX_TOKEN = 102

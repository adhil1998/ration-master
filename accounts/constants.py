from common.functions import ChoiceAdapter


class UserType(ChoiceAdapter):
    ADMIN = 100
    SHOP = 200
    CARD = 300


class OTPType(ChoiceAdapter):
    LOGIN = 100
    VERIFY = 200


class GenderType(ChoiceAdapter):
    MALE = 100
    FEMALE = 200
    OTHERS = 300

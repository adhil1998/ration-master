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


class CardType(ChoiceAdapter):
    YELLOW = 100
    PINK = 200
    WHITE = 300
    BLUE = 400


class AgeGroupType(ChoiceAdapter):
    ADULT = 100
    CHILD = 200

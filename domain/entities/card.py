from pydantic.dataclasses import dataclass
from pydantic import validator
from pydantic.fields import Field

from domain.value_objects.card import PAN, CV2, ExpirationDate
from domain.entities.bank import Account
from domain.entities import Model
from domain.exceptions import CardError


class Card(Model):
    expiration_date: ExpirationDate = ExpirationDate.generate_three_years()
    pan: PAN = PAN.generate()
    cv2: CV2 = CV2.generate()
    account: Account

    @classmethod
    def issue(cls, account: Account):
        return Card(
            account=account
        )

    @property
    def balance(self):
        return self.account.balance

    @property
    def currency(self):
        return self.account.currency

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise CardError.NotCardType()
        return self.pan == other.pan and self.expiration_date == other.expiration_date \
            and self.cv2 == other.cv2
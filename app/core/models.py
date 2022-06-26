import enum
import logging
import sqlalchemy as sa
import sqlalchemy.orm as so


from typing import List, Optional
from sqlalchemy import ForeignKey, event
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
import datetime
import uuid

from sqlalchemy_utils import ChoiceType

from app.core.engine import local_session

logger = logging.getLogger('uvicorn')

Base: DeclarativeMeta = declarative_base()


class Type(str, enum.Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'


class ShopUnits(Base):
    """
    Товар или категория, в зависимости от параметра type
    """

    __tablename__ = 'ShopUnits'

    id = sa.Column(sa.String, unique=True, nullable=False, primary_key=True, default=str(uuid.uuid1()))
    name = sa.Column(sa.String, nullable=False)
    date = sa.Column(sa.DateTime(timezone=datetime.timezone.utc), nullable=False)
    parentID = sa.Column(sa.String, ForeignKey('shop_unit.id'), nullable=True, default=None, index=True)
    type = sa.Column(ChoiceType(Type, impl=sa.String()), nullable=False)
    price = sa.Column(sa.Integer, nullable=True)
    children: List['ShopUnits'] = so.relationship('ShopUnits',
                                                  backref=so.backref('parent', remote_side='ShopUnits.id'),
                                                  uselist=True, cascade='all, delete'
                                                  )

    def get_child(self, index: int = 0):
        if len(self.children) > index:
            return self.children[index]
        return None

    def __repr__(self) -> str:
        return f'ShopUnit_name {self.name}, ShopUnit_id: {self.id}'


@event.listens_for(ShopUnits, 'after_insert')
def do_something(su: ShopUnits):
    if su.parentID is not None:
        session = local_session()
        parent = session.query(ShopUnits).filter_by(id=su.parentID).one()
        parent.date = su.date
        session.add(parent)
        session.commit()


def calculate_category_price(category: ShopUnits) -> \
        Optional[int]:
    logger.warning('CALCULATING BEGIN')
    ctgr_with_price = [[category, 0]]
    n, w = 0, 0
    logger.info(ctgr_with_price)
    while len(ctgr_with_price):
        logger.info(ctgr_with_price)
        last, index = ctgr_with_price[-1]
        ctgr_with_price[-1][1] += 1
        child = last.get_child(index)
        if child and child.type == Type.OFFER:
            n += 1
            w += child.price
        elif child:
            ctgr_with_price.append([child, 0])
        else:
            ctgr_with_price.pop()
    if n:
        return int(round(w / n))
    return None


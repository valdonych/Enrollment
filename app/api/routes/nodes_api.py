from fastapi import HTTPException, APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.core.models import ShopUnits
from app.core.engine import get_session
from uuid import UUID
from app.api.schemas.shop_unit_schema import ShopUnitSchema
from typing import Union
from math import floor
from app.core.models import Type
router = APIRouter()


@cbv(router)
class Nodes:
    s: Session = Depends(get_session)

    @router.get('/nodes/{id}', response_model=ShopUnitSchema, response_model_by_alias=True,
                name='Получает информацию об элементе по идентификатору',
                tags=['Базовые задачи'])
    def get_shop_unit(self,
                      id: Union[UUID, str],
                      session: Session = Depends(get_session),
                      ):

        if id is not UUID:

            show_unit = (session.query(ShopUnits)).filter(id=id).one_or_none()

            if show_unit is None:
                raise HTTPException(status_code=404, detail='Item not found')

            shopunit: ShopUnitSchema = ShopUnitSchema.from_orm(show_unit)
            if shopunit.type == show_unit.CATEGORY:
                su = [[shopunit, 0, 0, 0]]
                while len(su):
                    last, index = su[-1][0], su[-1][1]
                    child = last.get_child(index)
                    if child is None:
                        last.price = int(floor(su[-1][3] / su[-1][2]))
                        if len(su) > 1:
                            su[-2][3] += su[-1][3]
                            su[-2][2] += su[-1][2]
                        su.pop()
                    else:
                        su[-1][1] += 1
                        if child.type == Type.OFFER:
                            su[-1][2] += 1
                            su[-1][3] += child.price
                        else:
                            su.append([child, 0, 0, 0])
            return shopunit





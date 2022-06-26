from fastapi import HTTPException, APIRouter, Depends, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from loguru import logger
from app.core.models import ShopUnits
from app.core.engine import get_session
from app.api.schemas.shop_unit_schema import ShopUnitImportRequest

router = APIRouter()


@cbv(router)
class Import:

    @router.post('/import',
                 name='Добавляет новые товары или категории',
                 status_code=200,
                 tags=['Базовые задачи'])
    def import_shop_unit(self, items: ShopUnitImportRequest,
                         s: Session = Depends(get_session)
                         ) -> Response:

        for units in items.items:
            units.date = items.update_date
            shop_unit_model = s.query(ShopUnits).filter(
                ShopUnits.id == units.id).one_or_none()
            if shop_unit_model is not None:
                logger.warning('find shopunit in base')
                if shop_unit_model.type != units.type:
                    raise HTTPException(status_code=400, detail='Validation Failed')
                for var, value in vars(units).items():
                    setattr(shop_unit_model, var, value) if value else None
                s.add(shop_unit_model)
            else:
                s.add(ShopUnits(**units.dict()))
            s.commit()
        return Response(status_code=200)


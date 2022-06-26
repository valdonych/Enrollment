from fastapi import HTTPException, status, APIRouter, Depends, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.core.models import ShopUnits
from app.core.engine import get_session
from uuid import UUID
from starlette.status import HTTP_200_OK

router = APIRouter()


@cbv(router)
class Delete:
    s: Session = Depends(get_session)

    @router.delete('/delete/{id}')
    def delete_shop_unit(self,
                         id: str,
                         session: Session = Depends(get_session),
                         ):

        if id is UUID:
            delete_unit = session.query(ShopUnits).filter(ShopUnits.id == id)

            if delete_unit.first() is not None:
                delete_unit.delete()
                session.commit()
                return Response(status_code=HTTP_200_OK)

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Item not found'
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Validation Failed'
            )




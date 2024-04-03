from fastapi import APIRouter

from .. import schemas
from ..util import get_item_list

router = APIRouter(tags=["maps"])


@router.get(
    "/maps/",
    response_model=schemas.ItemList[schemas.MapListItem]
)
def get_maps():
    return get_item_list(
        "padoa.thredds.models.Map",
        schemas.MapListItem
    )


@router.get(
    "/user-downloads/",
    response_model=schemas.ItemList[schemas.UserDownloadListItem])
def get_user_downloads():
    return get_item_list(
        "padoa.thredds.models.UserDownload",
        schemas.UserDownloadListItem
    )

from fastapi import APIRouter

from .. import schemas

router = APIRouter(tags=["places"])


@router.get(
    "/cities/",
    response_model=schemas.ItemList[schemas.CityListItem]
)
def get_cities():
    from padoa.places import models
    items = []
    for db_city in models.Cities.objects.all():
        items.append(
            schemas.CityListItem(
                id=db_city.id,
                name=db_city.name,
                latlng=schemas.CityLocation(
                    lng=db_city.centroid.x, lat=db_city.centroid.y)
            )
        )
    return schemas.ItemList[schemas.CityListItem](
        count=len(items),
        results=items,
    )

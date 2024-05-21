from fastapi import APIRouter
from fastapi.responses import FileResponse

from .. import schemas

router = APIRouter(tags=["ncss"])


@router.post(
    "/time-series", response_model=schemas.ItemList[schemas.TimeSeriesListItem]
)
def create_time_series(
    time_series: schemas.TimeSeriesCreate,
):
    """### Create a new time series

    Returns a time series and also stores the request in the database, for the
    purpose of gathering usage data.
    """
    ...


@router.post(
    "/datasets",
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/netcdf": {}},
            "description": "Return a NetCDF file with the dataset",
        }
    },
)
def request_netcdf_download(dataset: schemas.DatasetReadIn) -> FileResponse:
    """### Download a dataset as a NetCDF file

    Returns the file and also stores the request in the database, for the purpose of
    gathering usage data.
    """
    ...

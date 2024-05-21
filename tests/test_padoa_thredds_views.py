import pytest
from django.contrib.gis.geos import GEOSGeometry

from padoa.thredds import models as tm
from padoa.forecastattributes import models as fam


@pytest.mark.django_db(transaction=True)
@pytest.mark.xfail(reason="Not implemented yet")
@pytest.mark.parametrize(
    "url_list_path",
    [
        pytest.param("legacy/maps/ncss/timeserie/"),
    ],
)
def test_ncsstimeserie_list(test_client, url_list_path):
    num_items = 3
    variable = fam.Variable.objects.create(id="fakevar1", name="Fake var 1")
    forecast_model = fam.ForecastModel.objects.create(
        id="fakeforecastmodel1", name="Fake forecast model 1"
    )
    scenario = fam.Scenario.objects.create(id="fakescenario1", name="Fake scenario 1")
    data_series = fam.DataSeries.objects.create(
        id="fakedataseries1", name="Fake data series 1"
    )
    year_period = fam.YearPeriod.objects.create(
        id="fakeyearperiod1", name="Fake year period 1"
    )
    value_type = fam.ValueType.objects.create(
        id="fakevaluetype1", name="Fake value type 1"
    )

    created_ids = []
    for i in range(1, num_items + 1):
        # regardless of the model definition:
        # - spatialbounds must be provided, otherwise serialization fails
        # - palette must be provided, otherwise serialization fails
        instance = tm.Map.objects.create(
            variable=variable,
            forecast_model=forecast_model,
            scenario=scenario,
            data_series=data_series,
            year_period=year_period,
            time_window=None,
            value_type=value_type,
            layer_id=f"fakelayerid{i}",
            path="/some/fake/path",
            spatialbounds=GEOSGeometry("POLYGON(( 10 10, 10 20, 20 20, 20 15, 10 10))"),
            palette="fakepalette",
        )
        created_ids.append(instance.id)
    response = test_client.get(
        url_list_path, data={"ids": ",".join(str(i) for i in created_ids)}
    )
    print(f"{response.json()=}")
    assert response.status_code == 200
    assert False

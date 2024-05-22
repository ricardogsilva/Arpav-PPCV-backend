import pytest

from padoa.forecastattributes import models


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "model_class, list_url_path",
    [
        pytest.param(models.Variable, "/legacy/forcastattributes/variables/"),
        pytest.param(
            models.ForecastModel, "/legacy/forcastattributes/forecast_models/"
        ),
        pytest.param(models.Scenario, "/legacy/forcastattributes/scenarios/"),
        pytest.param(models.DataSeries, "/legacy/forcastattributes/data_series/"),
        pytest.param(models.YearPeriod, "/legacy/forcastattributes/year_periods/"),
        pytest.param(models.TimeWindow, "/legacy/forcastattributes/time_windows/"),
        pytest.param(models.ValueType, "/legacy/forcastattributes/value_types/"),
    ],
)
def test_list_instances(test_client, model_class, list_url_path):
    num_items = 3
    for i in range(1, num_items + 1):
        model_class.objects.create(
            id=f"fake{model_class.__name__.lower()}{i}",
            name=f"Fake {model_class.__name__} {i}",
            description=f"This is a fake {model_class.__name__}, useful for testing",
            order_item=i,
        )
    response = test_client.get(list_url_path)
    assert response.status_code == 200
    contents = response.json()
    assert contents.get("count") == num_items
    assert len(contents.get("results")) == num_items
    for i in range(1, num_items + 1):
        for model_ in contents["results"]:
            if model_.get("id") == f"fake{model_class.__name__.lower()}{i}":
                assert model_["name"] == f"Fake {model_class.__name__} {i}"
                assert model_["description"] == (
                    f"This is a fake {model_class.__name__}, useful for testing"
                )
                assert model_["order_item"] == i
                break
        else:
            print(f"Did not find instance #{i}")
            assert False


# these are disabled because changing django-rest-framework page size with
# pytest_django's `settings` fixture does not seem to work.
# @pytest.mark.django_db
# @pytest.mark.parametrize("model_class, list_url_path", [
#     pytest.param(models.Variable, "/forcastattributes/variables/"),
#     pytest.param(models.ForecastModel, "/forcastattributes/forecast_models/"),
#     pytest.param(models.Scenario, "/forcastattributes/scenarios/"),
#     pytest.param(models.DataSeries, "/forcastattributes/data_series/"),
#     pytest.param(models.YearPeriod, "/forcastattributes/year_periods/"),
#     pytest.param(models.TimeWindow, "/forcastattributes/time_windows/"),
#     pytest.param(models.ValueType, "/forcastattributes/value_types/"),
# ])
# def test_list_instances_with_pagination_has_next(
#         client,
#         settings,
#         model_class,
#         list_url_path
# ):
#     page_size = 5
#     num_items = page_size + 3
#     settings.REST_FRAMEWORK["PAGE_SIZE"] = page_size
#     for i in range(1, num_items + 1):
#         model_class.objects.create(
#             id=f"fake{model_class.__name__.lower()}{i}",
#             name=f"Fake {model_class.__name__} {i}",
#             description=f"This is a fake {model_class.__name__}, useful for testing",
#             order_item=i
#         )
#     response = client.get(list_url_path)
#     assert response.status_code == 200
#     contents = response.json()
#     print(f"{contents=}")
#     assert contents.get("count") == num_items
#     assert len(contents.get("results")) == page_size
#     assert contents.get("next") is not None
#     assert contents.get("previous") is None
#
#
# @pytest.mark.django_db
# @pytest.mark.parametrize("model_class, list_url_path", [
#     pytest.param(models.Variable, "/forcastattributes/variables/"),
#     pytest.param(models.ForecastModel, "/forcastattributes/forecast_models/"),
#     pytest.param(models.Scenario, "/forcastattributes/scenarios/"),
#     pytest.param(models.DataSeries, "/forcastattributes/data_series/"),
#     pytest.param(models.YearPeriod, "/forcastattributes/year_periods/"),
#     pytest.param(models.TimeWindow, "/forcastattributes/time_windows/"),
#     pytest.param(models.ValueType, "/forcastattributes/value_types/"),
# ])
# def test_list_instances_with_pagination_has_previous(
#         client,
#         settings,
#         model_class,
#         list_url_path
# ):
#     page_size = 5
#     num_items = page_size + 3
#     settings.REST_FRAMEWORK["PAGE_SIZE"] = page_size
#     for i in range(1, num_items + 1):
#         model_class.objects.create(
#             id=f"fake{model_class.__name__.lower()}{i}",
#             name=f"Fake {model_class.__name__} {i}",
#             description=f"This is a fake {model_class.__name__}, useful for testing",
#             order_item=i
#         )
#     response = client.get(list_url_path, data={"page": 2})
#     assert response.status_code == 200
#     contents = response.json()
#     print(f"contents: {contents}")
#     assert contents.get("count") == num_items
#     assert len(contents.get("results")) == num_items - page_size
#     assert contents.get("next") is None
#     assert contents.get("previous") is not None

import pytest

from padoa.places import models


@pytest.mark.django_db(transaction=True)
def test_list_cities(test_client):
    num_items = 3
    fake_region = models.Regions.objects.create(
        id=1,
        name="fakeregion",
        geometry="MULTIPOLYGON(((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))",
        centroid="Point(0 0)"
    )
    fake_province = models.Provinces.objects.create(
        id=10,
        name="fakeprovince",
        region=fake_region,
        geometry="MULTIPOLYGON(((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))",
        centroid="Point(10 10)",
    )
    centroids = {}
    for i in range(1, num_items + 1):
        centroid = {"longitude": i, "latitude": i+3}
        centroids[i] = centroid
        models.Cities.objects.create(
            id=100+i,
            name=f"Fake city {i}",
            prov_code="fakeprovincecode",
            region=fake_region,
            province=fake_province,
            geometry="MULTIPOLYGON(((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))",
            centroid=f"Point({centroid['longitude']} {centroid['latitude']})"
        )
    response = test_client.get("/legacy/places/cities/")
    assert response.status_code == 200
    contents = response.json()
    assert contents.get("count") == num_items
    assert len(contents.get("results")) == num_items
    for i in range(1, num_items + 1):
        print(f"looking for city #{i}...")
        for model_ in contents["results"]:
            if model_.get("id") == 100 + i:
                expected_centroid = centroids[i]
                assert model_["name"] == f"Fake city {i}"
                assert model_["latlng"] == {
                    "lng": expected_centroid["longitude"],
                    "lat": expected_centroid["latitude"]
                }
                break
        else:
            print(f"Did not find instance #{i}")
            assert False

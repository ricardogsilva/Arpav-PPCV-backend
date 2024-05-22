import httpx


def test_refresh_monthly_measurements_with_new_measurement(
    httpx_mock,
    cli_runner,
    cli_app,
    sample_variables,
    sample_stations,
    sample_monthly_measurements,
):
    target_station = sample_stations[0]
    target_variable = sample_variables[0]
    execution_args = [
        "observations-harvester",
        "refresh-monthly-measurements",
        "--station",
        str(target_station.code),
        "--variable",
        target_variable.name,
    ]
    httpx_mock.add_response(
        json={
            "data": [
                {
                    "valore": 2.23,
                    "anno": 2021,
                },
            ],
        },
        status_code=200,
    )
    result = cli_runner.invoke(cli_app, execution_args)
    print(f"{result.stdout=}")
    print(f"{result.stderr=}")
    assert result.exit_code == 0


def test_refresh_monthly_measurements_with_existing_measurement(
    httpx_mock,
    cli_runner,
    cli_app,
    sample_variables,
    sample_stations,
    sample_monthly_measurements,
):
    target_measurement = sample_monthly_measurements[0]
    target_station = target_measurement.station
    target_variable = target_measurement.variable
    target_year = target_measurement.date.year
    target_month = target_measurement.date.month
    execution_args = [
        "observations-harvester",
        "refresh-monthly-measurements",
        "--station",
        str(target_station.code),
        "--variable",
        target_variable.name,
    ]

    def custom_response(request: httpx.Request) -> httpx.Response:
        if request.url.params["periodo"] == str(target_month):
            result_response = httpx.Response(
                status_code=200,
                json={
                    "data": [
                        {
                            "valore": 2.23,
                            "anno": target_year,
                        },
                    ],
                },
            )
        else:
            result_response = httpx.Response(status_code=200, json={"data": []})
        return result_response

    httpx_mock.add_callback(custom_response)

    result = cli_runner.invoke(cli_app, execution_args)
    assert result.exit_code == 0
    assert "Created 0 monthly measurements" in result.stdout

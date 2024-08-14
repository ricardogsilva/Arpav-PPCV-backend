import prefect
import typer

from .flows import observations as observations_flows

app = typer.Typer()


@app.command()
def start_periodic_tasks(
    ctx: typer.Context,
    refresh_stations: bool = False,
    refresh_monthly_measurements: bool = False,
    refresh_seasonal_measurements: bool = False,
    refresh_yearly_measurements: bool = False,
):
    to_serve = []
    if refresh_stations:
        stations_refresher_deployment = (
            observations_flows.refresh_stations.to_deployment(
                name="stations_refresher",
            )
        )
        to_serve.append(stations_refresher_deployment)
    if refresh_monthly_measurements:
        monthly_measurement_refresher_deployment = (
            observations_flows.refresh_monthly_measurements.to_deployment(
                name="monthly_measurement_refresher",
            )
        )
        to_serve.append(monthly_measurement_refresher_deployment)
    if refresh_seasonal_measurements:
        seasonal_measurement_refresher_deployment = (
            observations_flows.refresh_seasonal_measurements.to_deployment(
                name="seasonal_measurement_refresher",
            )
        )
        to_serve.append(seasonal_measurement_refresher_deployment)
    if refresh_yearly_measurements:
        yearly_measurement_refresher_deployment = (
            observations_flows.refresh_yearly_measurements.to_deployment(
                name="yearly_measurement_refresher",
            )
        )
        to_serve.append(yearly_measurement_refresher_deployment)
    prefect.serve(*to_serve)

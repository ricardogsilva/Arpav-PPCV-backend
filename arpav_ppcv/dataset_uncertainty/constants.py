import dataclasses


@dataclasses.dataclass
class UncertaintyDatasetMetadata:
    netcdf_variable_name: str
    standard_name: str
    long_name: str
    attribute_ref: str = "http://www.uncertml.org/statistics/variance"  # noqa


@dataclasses.dataclass
class ForecastDatasetMetadata:
    netcdf_variable_name: str
    standard_name: str
    long_name: str
    attribute_ref: str
    uncertainty: UncertaintyDatasetMetadata
    common_variables: tuple[str] = (
        "time",
        "lon",
        "lat",
        "height"
    )


KNOWN_DATASETS = {
    "tas": ForecastDatasetMetadata(
        netcdf_variable_name="tas",
        standard_name="air_temperature_anomaly",
        long_name="Near-Surface air temperature anomaly",
        attribute_ref="http://www.uncertml.org/statistics/mean",
        uncertainty=UncertaintyDatasetMetadata(
            netcdf_variable_name="tas-agree",
            standard_name="air_temperature_anomaly_standard_error",  # this is not an official standard name
            # long_name="Model agreement of near-surface air temperature anomaly",
            long_name="air_temperature_anomaly uncertainty_visualization",
        )
    )
}

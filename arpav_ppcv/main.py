"""Command-line interface for the project."""

import dataclasses
import enum
import itertools
from pathlib import Path

import requests
import typer


@dataclasses.dataclass
class ForecastTemporalPeriodMetadata:
    name: str
    code: str


class ForecastTemporalPeriod(enum.Enum):
    TW1 = ForecastTemporalPeriodMetadata(name="2021 - 2050", code="tw1")
    TW2 = ForecastTemporalPeriodMetadata(name="2071 - 2100", code="tw2")


@dataclasses.dataclass
class ForecastSeasonMetadata:
    name: str
    code: str


class ForecastSeason(enum.Enum):
    DJF = ForecastSeasonMetadata(name="Winter", code="DJF")
    MAM = ForecastSeasonMetadata(name="Spring", code="MAM")
    JJA = ForecastSeasonMetadata(name="Summer", code="JJA")
    SON = ForecastSeasonMetadata(name="Autumn", code="SON")


@dataclasses.dataclass
class ForecastModelMetadata:
    name: str
    code: str
    thredds_base_path: str


@dataclasses.dataclass
class ForecastScenarioMetadata:
    name: str
    code: str


class ForecastScenario(enum.Enum):
    RCP26 = ForecastScenarioMetadata(name="RCP26", code="rcp26")
    RCP45 = ForecastScenarioMetadata(name="RCP45", code="rcp45")
    RCP85 = ForecastScenarioMetadata(name="RCP85", code="rcp85")


class ForecastAnomalyVariablePathPattern(enum.Enum):
    TAS_ENSEMBLE = "ensembletwbc/clipped/tas_avg_anom_{period}_{scenario}_{season}_VFVGTAA.nc"
    TASMIN_ENSEMBLE = "ensembletwbc/clipped/tasmin_avg_anom_{period}_{scenario}_{season}_VFVGTAA.nc"
    TASMAX_ENSEMBLE = "ensembletwbc/clipped/tasmax_avg_anom_{period}_{scenario}_{season}_VFVGTAA.nc"
    PR_ENSEMBLE = "ensembletwbc/clipped/pr_avg_percentage_{period}_{scenario}_{season}_VFVGTAA.nc"
    TR_ENSEMBLE = "ensembletwbc/clipped/ecatran_20_avg_{period}_{scenario}_ls_VFVG.nc"
    SU30_ENSEMBLE = "ensembletwbc/clipped/ecasuan_30_avg_{period}_{scenario}_ls_VFVG.nc"
    FD_ENSEMBLE = "ensembletwbc/clipped/ecafdan_0_avg_{period}_{scenario}_ls_VFVG.nc"
    HWDI_ENSEMBLE = "ensembletwbc/clipped/heat_waves_anom_avg_55_{period}_{scenario}_JJA_VFVGTAA.nc"
    TAS_ECEARTHCCLM4817 = "taspr5rcm/clipped/tas_EC-EARTH_CCLM4-8-17_{scenario}_seas_{period}{season}_VFVGTAA.nc"
    TASMIN_ECEARTHCCLM4817 = "taspr5rcm/clipped/tasmin_EC-EARTH_CCLM4-8-17_{scenario}_seas_{period}{season}_VFVGTAA.nc"
    TASMAX_ECEARTHCCLM4817 = "taspr5rcm/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_seas_{period}{season}_VFVGTAA.nc"
    HWDI_ECEARTHCCLM4817 = "indici5rcm/clipped/heat_waves_anom_EC-EARTH_CCLM4-8-17_{scenario}_JJA_55_{period}_VFVGTAA.nc"


app = typer.Typer()


@app.command()
def import_anomaly_forecast_datasets(target_dir: Path):
    download_url_pattern = (
        "https://thredds.arpa.veneto.it/thredds/fileServer/{path}"
    )
    session = requests.Session()
    seasonal_patterns = []
    annual_patterns = []
    for pattern in ForecastAnomalyVariablePathPattern:
        if all(
                (
                        "{season}" in pattern.value,
                        "{scenario}" in pattern.value,
                        "{period}" in pattern.value,
                )
        ):
            seasonal_patterns.append(pattern)
        else:
            annual_patterns.append(pattern)

    paths = []
    for seasonal_pattern in seasonal_patterns:
        combinator = itertools.product(
            ForecastScenario,
            ForecastTemporalPeriod,
            ForecastSeason,
        )
        for scenario, period, season in combinator:
            path = seasonal_pattern.value.format(
                scenario=scenario.value.code,
                period=period.value.code,
                season=season.value.code
            )
            paths.append((seasonal_pattern, path))
    for annual_pattern in annual_patterns:
        combinator = itertools.product(
            ForecastScenario,
            ForecastTemporalPeriod,
        )
        for scenario, period in combinator:
            path = annual_pattern.value.format(
                scenario=scenario.value.code,
                period=period.value.code,
            )
            paths.append((annual_pattern, path))
    for pattern, path in paths:
        print(f"Processing {pattern.name!r}...")
        output_path = target_dir / path
        if not output_path.exists():
            print(f"Saving {output_path!r}...")
            download_url = download_url_pattern.format(path=path)
            response = session.get(download_url, stream=True)
            response.raise_for_status()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("wb") as fh:
                for chunk in response.iter_content():
                    fh.write(chunk)
        else:
            print(f"path already exists ({output_path!r}) - skipping")
    print("Done!")

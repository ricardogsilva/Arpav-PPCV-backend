import dataclasses
import enum
from pathlib import Path
from typing import Annotated

import netCDF4
import typer

from . import (
    constants,
    operations,
)


_KNOWN_DATASET_CHOICES = enum.Enum(
    "KNOWN_DATASET_TYPES",
    " ".join(n for n in constants.KNOWN_DATASETS), module=__name__)
app = typer.Typer()


@dataclasses.dataclass
class _ErrorNetcdfFile:
    old_name: str
    new_name: str
    new_var_long_name: str
    uncertainty_attribute_ref: str


@app.command()
def main(
        main_netcdf: Path,
        error_netcdf: Path,
        output_netcdf: Path,
        dataset_name: Annotated[_KNOWN_DATASET_CHOICES, typer.Argument()]
):
    ds_meta = constants.KNOWN_DATASETS[dataset_name]
    with (
        netCDF4.Dataset(output_netcdf, mode="w") as out_ds,
        netCDF4.Dataset(main_netcdf) as main_ds,
        netCDF4.Dataset(error_netcdf) as error_ds,
    ):
        operations.merge_netcdf_files(
            main_ds=main_ds,
            error_ds=error_ds,
            out_ds=out_ds,
            ds_meta=ds_meta,
        )
        out_ds[ds_meta.netcdf_variable_name].ref = ds_meta.attribute_ref
        out_ds[ds_meta.uncertainty.netcdf_variable_name].ref = ds_meta.uncertainty.attribute_ref

        operations.prepare_uncertainty_visualization_variable(out_ds, ds_meta)
        out_ds.Conventions = "CF-1.10"
        out_ds.title = "Test NetCDF File"
        operations.tweak_agree_values(
            out_ds[ds_meta.uncertainty.netcdf_variable_name])


if __name__ == "__main__":
    app()

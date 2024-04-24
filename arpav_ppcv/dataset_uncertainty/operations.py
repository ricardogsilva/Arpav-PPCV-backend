import netCDF4

from . import constants


def merge_netcdf_files(
        *,
        main_ds: netCDF4.Dataset,
        error_ds: netCDF4.Dataset,
        out_ds: netCDF4.Dataset,
        ds_meta: constants.ForecastDatasetMetadata,
) -> None:
    _copy_dimensions(main_ds, out_ds)
    _copy_variables(error_ds, out_ds)

    out_ds.renameVariable(
        ds_meta.netcdf_variable_name, ds_meta.uncertainty.netcdf_variable_name)

    for var_name in ds_meta.common_variables:
        out_ds[var_name][:] = main_ds[var_name][:]

    error_var = out_ds[ds_meta.uncertainty.netcdf_variable_name]
    error_var[:] = error_ds[ds_meta.netcdf_variable_name][:]

    main_var = out_ds.createVariable(
        ds_meta.netcdf_variable_name,
        main_ds[ds_meta.netcdf_variable_name].datatype,
        dimensions=main_ds[ds_meta.netcdf_variable_name].dimensions
    )
    main_var[:] = main_ds[ds_meta.netcdf_variable_name][:]

    for variable in main_ds.variables.values():
        _copy_variable_attributes(variable, out_ds[variable.name])

    _copy_variable_attributes(error_ds[ds_meta.netcdf_variable_name], error_var)

    main_var.standard_name = ds_meta.standard_name
    main_var.long_name = ds_meta.long_name
    error_var.standard_name = ds_meta.uncertainty.standard_name  # this is not an official standard name
    error_var.long_name = ds_meta.uncertainty.long_name


def _copy_dimensions(
        source: netCDF4.Dataset,
        destination: netCDF4.Dataset
) -> None:
    for dim in source.dimensions.values():
        destination.createDimension(dimname=dim.name, size=dim.size)


def _copy_variables(
        source: netCDF4.Dataset,
        destination: netCDF4.Dataset,
) -> None:
    for variable in source.variables.values():
        destination.createVariable(
            variable.name,
            variable.datatype,
            dimensions=variable.dimensions,
        )


def _copy_variable_attributes(
        source: netCDF4.Variable,
        destination: netCDF4.Variable
) -> None:
    exempt_attributes = {
        "_FillValue",
    }
    for name in source.ncattrs():
        if name not in exempt_attributes:
            setattr(destination, name, getattr(source, name))


def prepare_uncertainty_visualization_variable(
        ds: netCDF4.Dataset,
        ds_meta: constants.ForecastDatasetMetadata,
) -> None:
    uncertainty_var = ds.createVariable(
        varname="uncertainty-visualization",
        datatype="i1",
        dimensions=(),
    )
    uncertainty_var[:] = 1
    uncertainty_var.long_name = ds_meta.uncertainty.long_name
    uncertainty_var.ref = ds_meta.uncertainty.attribute_ref

    ancillary_variables = (
        ds_meta.netcdf_variable_name,
        ds_meta.uncertainty.netcdf_variable_name,
    )

    uncertainty_var.ancillary_variables = " ".join(ancillary_variables)


def tweak_agree_values(agree_var: netCDF4.Variable) -> None:
    contents = agree_var[:]
    contents[contents == 0] = 2
    contents[contents == 1] = 0
    contents[contents == 2] = 1
    agree_var[:] = contents[:]


def generate_sample_uncertainty_netcdf_file(
        template_ds: netCDF4.Dataset,
        target_ds: netCDF4.Dataset,
        template_variable_name: str,
        out_ds: netCDF4.Dataset,
        target_ds_meta: constants.ForecastDatasetMetadata
):
    _copy_dimensions(target_ds, out_ds)
    template_variable = template_ds[template_variable_name]
    uncertainty_variable = out_ds.createVariable(
        target_ds_meta.uncertainty.netcdf_variable_name,
        datatype=template_variable.datatype,
        dimensions=template_variable.dimensions
    )
    uncertainty_variable[:] = template_ds[template_variable_name][:]
    prepare_uncertainty_visualization_variable(out_ds, target_ds_meta)
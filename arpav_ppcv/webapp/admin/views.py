"""Views for the admin app.

The classes contained in this module are derived from
starlette_admin.contrib.sqlmodel.ModelView. This is done mostly for two reasons:

1. To be able to control database access and ensure we are using our handlers
   defined in `arpav_ppcv.database` - this is meant for achieving consistency
   throughout the code, as the API is also using the mentioned functions for
   interacting with the DB

2. To be able to present inline forms for editing related objects, as is the
   case with parameter configuration and its related values.

"""

import functools
import logging
from typing import Dict, Any, Union, Optional, List, Sequence

import anyio.to_thread
import starlette_admin
from starlette.requests import Request
from starlette_admin.contrib.sqlmodel import ModelView

from ... import database
from ...schemas import (
    coverages,
    base,
)
from . import (
    fields,
    schemas as read_schemas,
)


logger = logging.getLogger(__name__)


def possible_values_choices_loader(request: Request) -> Sequence[tuple[str, str]]:
    all_conf_parameter_values = database.collect_all_configuration_parameter_values(
        request.state.session
    )
    result = []
    for conf_param_value in all_conf_parameter_values:
        repr_value = " - ".join((
            conf_param_value.configuration_parameter.name, conf_param_value.name))
        result.append((repr_value, repr_value))
    return result


def related_observation_variable_choices_loader(
        request: Request) -> Sequence[tuple[str, str]]:
    all_obs_variables = database.collect_all_variables(request.state.session)
    return [(v.name, v.name) for v in all_obs_variables]


def coverage_configurations_choices_loader(
        request: Request) -> Sequence[tuple[str, str]]:
    all_cov_confs = database.collect_all_coverage_configurations(request.state.session)
    result = []
    for cov_conf in all_cov_confs:
        result.append((cov_conf.name, cov_conf.name))
    return result


class ConfigurationParameterView(ModelView):
    identity = "configuration_parameters"
    name = "Configuration Parameter"
    label = "Configuration Parameters"
    icon = "fa fa-blog"
    pk_attr = "id"

    exclude_fields_from_list = (
        "id",
    )
    exclude_fields_from_detail = (
        "id",
    )

    fields = (
        fields.UuidField("id"),
        starlette_admin.StringField(
            "name",
            help_text=(
                "Name for the configuration parameter. Must only use alphanumeric "
                "characters and the underscore. If you use the special name "
                "'year_period', then the system will use this parameter to "
                "perform database queries."
            )
        ),
        starlette_admin.StringField("description"),
        starlette_admin.ListField(
            field=starlette_admin.CollectionField(
                "allowed_values",
                fields=(
                    fields.UuidField(
                        "id",
                        read_only=True,
                        # disabled=True,
                        exclude_from_list=True,
                        exclude_from_detail=True,
                        exclude_from_create=True,
                        exclude_from_edit=False,
                ),
                    starlette_admin.StringField("name"),
                    starlette_admin.StringField(
                        "description",
                        exclude_from_list=True,
                    ),
                )
            )
        )
    )

    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        # note: we need to cast the value, which is a uuid.UUID, to a string
        # because starlette_admin just assumes that the value of a model's
        # pk attribute is always JSON serializable so it doesn't bother with
        # calling the respective field's `serialize_value()` method
        result = await super().get_pk_value(request, obj)
        return str(result)

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        try:
            data = await self._arrange_data(request, data)
            await self.validate(request, data)
            config_param_create = coverages.ConfigurationParameterCreate(
                name=data["name"],
                description=data["description"],
                allowed_values=[
                    coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                        name=av["name"],
                        description=av["description"]
                    ) for av in data["allowed_values"]
                ]
            )
            db_configuration_parameter = await anyio.to_thread.run_sync(
                database.create_configuration_parameter,
                request.state.session,
                config_param_create
            )
            configuration_parameter_read = read_schemas.ConfigurationParameterRead(
                **db_configuration_parameter.model_dump(
                    exclude={"allowed_values"}
                ),
                allowed_values=[
                    read_schemas.ConfigurationParameterValueRead(**av.model_dump())
                    for av in db_configuration_parameter.allowed_values
                ]
            )
            logger.debug("About to leave the create instance")
            logger.debug(f"{configuration_parameter_read=}")
            return configuration_parameter_read
        except Exception as e:
            return self.handle_exception(e)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        try:
            data = await self._arrange_data(request, data, True)
            await self.validate(request, data)
            config_param_update = coverages.ConfigurationParameterUpdate(
                name=data.get("name"),
                description=data.get("description"),
                allowed_values=[
                    coverages.ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit(
                        id=av["id"] or None,
                        name=av.get("name"),
                        description=av.get("description")
                    ) for av in data["allowed_values"]
                ]
            )
            db_configuration_parameter = await anyio.to_thread.run_sync(
                database.get_configuration_parameter,
                request.state.session,
                pk
            )
            db_configuration_parameter = await anyio.to_thread.run_sync(
                database.update_configuration_parameter,
                request.state.session,
                db_configuration_parameter,
                config_param_update
            )
            conf_param_read = read_schemas.ConfigurationParameterRead(
                **db_configuration_parameter.model_dump(),
                allowed_values=[
                    read_schemas.ConfigurationParameterValueRead(**av.model_dump())
                    for av in db_configuration_parameter.allowed_values
                ]
            )
            return conf_param_read
        except Exception as e:
            logger.exception("something went wrong")
            self.handle_exception(e)

    async def find_by_pk(
            self,
            request: Request,
            pk: Any
    ) -> read_schemas.ConfigurationParameterRead:
        db_conf_param = await anyio.to_thread.run_sync(
            database.get_configuration_parameter,
            request.state.session,
            pk
        )
        return read_schemas.ConfigurationParameterRead(
            **db_conf_param.model_dump(),
            allowed_values=[
                read_schemas.ConfigurationParameterValueRead(**av.model_dump())
                for av in db_conf_param.allowed_values
            ]
        )

    async def find_all(
            self,
            request: Request,
            skip: int = 0,
            limit: int = 100,
            where: Union[Dict[str, Any], str, None] = None,
            order_by: Optional[List[str]] = None,
    ) -> Sequence[read_schemas.ConfigurationParameterRead]:
        list_params = functools.partial(
            database.list_configuration_parameters,
            limit=limit,
            offset=skip,
            include_total=False
        )
        db_conf_params, _ = await anyio.to_thread.run_sync(
            list_params, request.state.session)
        result = []
        for db_conf_param in db_conf_params:
            result.append(
                read_schemas.ConfigurationParameterRead(
                    **db_conf_param.model_dump(),
                    allowed_values=[
                        read_schemas.ConfigurationParameterValueRead(**av.model_dump())
                        for av in db_conf_param.allowed_values
                    ]
                )
            )
        return result


class CoverageConfigurationView(ModelView):
    identity = "coverage_configurations"
    name = "Coverage Configuration"
    label = "Coverage Configurations"
    icon = "fa fa-blog"
    pk_attr = "id"
    fields = (
        fields.UuidField("id"),
        starlette_admin.StringField("name"),
        starlette_admin.StringField("netcdf_main_dataset_name"),
        starlette_admin.StringField("thredds_url_pattern"),
        starlette_admin.StringField("coverage_id_pattern", disabled=True),
        starlette_admin.StringField("unit"),
        starlette_admin.StringField("palette"),
        starlette_admin.FloatField("color_scale_min"),
        starlette_admin.FloatField("color_scale_max"),
        fields.RelatedObservationsVariableField(
            "observation_variable",
            help_text="Related observation variable",
            choices_loader=related_observation_variable_choices_loader,
        ),
        starlette_admin.EnumField(
            "observation_variable_aggregation_type",
            enum=base.ObservationAggregationType
        ),
        starlette_admin.ListField(
            field=fields.PossibleConfigurationParameterValuesField(
                "possible_values", choices_loader=possible_values_choices_loader)
        ),
        fields.RelatedCoverageconfigurationsField(
            "uncertainty_lower_bounds_coverage_configuration",
            choices_loader=coverage_configurations_choices_loader,
            help_text=(
                "Coverage configuration to be used when looking for coverages "
                "which have the lower uncertainty bounds values"
            )
        ),
        fields.RelatedCoverageconfigurationsField(
            "uncertainty_upper_bounds_coverage_configuration",
            choices_loader=coverage_configurations_choices_loader,
            help_text=(
                "Coverage configuration to be used when looking for coverages "
                "which have the upper uncertainty bounds values"
            )
        ),
    )

    exclude_fields_from_list = (
        "id",
        "netcdf_main_dataset_name",
        "coverage_id_pattern",
        "possible_values",
        "unit",
        "palette",
        "color_scale_min",
        "color_scale_max",
        "observation_variable",
        "observation_variable_aggregation_type",
        "uncertainty_lower_bounds_coverage_configuration",
        "uncertainty_upper_bounds_coverage_configuration",
    )
    exclude_fields_from_edit = (
        "coverage_id_pattern",
    )

    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        # note: we need to cast the value, which is a uuid.UUID, to a string
        # because starlette_admin just assumes that the value of a model's
        # pk attribute is always JSON serializable so it doesn't bother with
        # calling the respective field's `serialize_value()` method
        result = await super().get_pk_value(request, obj)
        return str(result)

    def _serialize_instance(self, instance: coverages.CoverageConfiguration):
        obs_variable = instance.related_observation_variable
        if obs_variable is not None:
            observation_variable = read_schemas.ObservationVariableRead(
                **obs_variable.model_dump())
        else:
            observation_variable = None
        uncertainty_lower_cov_conf = instance.uncertainty_lower_bounds_coverage_configuration
        if uncertainty_lower_cov_conf is not None:
            uncertainty_lower_bounds_coverage_configuration = (
                read_schemas.CoverageConfigurationReadListItem(
                    id=uncertainty_lower_cov_conf.id,
                    name=uncertainty_lower_cov_conf.name)
            )
        else:
            uncertainty_lower_bounds_coverage_configuration = None
        uncertainty_upper_cov_conf = instance.uncertainty_upper_bounds_coverage_configuration
        if uncertainty_upper_cov_conf is not None:
            uncertainty_upper_bounds_coverage_configuration = (
                read_schemas.CoverageConfigurationReadListItem(
                    id=uncertainty_upper_cov_conf.id,
                    name=uncertainty_upper_cov_conf.name)
            )
        else:
            uncertainty_upper_bounds_coverage_configuration = None
        return read_schemas.CoverageConfigurationRead(
            **instance.model_dump(
                exclude={"observation_variable_aggregation_type"}
            ),
            observation_variable_aggregation_type=(
                    instance.observation_variable_aggregation_type or
                    base.ObservationAggregationType.SEASONAL
            ),
            observation_variable=observation_variable,
            possible_values=[
                read_schemas.ConfigurationParameterPossibleValueRead(
                    configuration_parameter_value_id=pv.configuration_parameter_value_id,
                    configuration_parameter_value_name=pv.configuration_parameter_value.name)
                for pv in instance.possible_values
            ],
            uncertainty_lower_bounds_coverage_configuration=uncertainty_lower_bounds_coverage_configuration,
            uncertainty_upper_bounds_coverage_configuration=uncertainty_upper_bounds_coverage_configuration,
        )


    async def find_by_pk(
            self,
            request: Request,
            pk: Any
    ) -> read_schemas.CoverageConfigurationRead:
        db_cov_conf = await anyio.to_thread.run_sync(
            database.get_coverage_configuration,
            request.state.session,
            pk
        )
        return self._serialize_instance(db_cov_conf)

    async def find_all(
            self,
            request: Request,
            skip: int = 0,
            limit: int = 100,
            where: Union[Dict[str, Any], str, None] = None,
            order_by: Optional[List[str]] = None,
    ) -> Sequence[read_schemas.CoverageConfigurationRead]:
        list_cov_confs = functools.partial(
            database.list_coverage_configurations,
            limit=limit,
            offset=skip,
            include_total=False
        )
        db_cov_confs, _ = await anyio.to_thread.run_sync(
            list_cov_confs, request.state.session)
        result = []
        for db_cov_conf in db_cov_confs:
            result.append(self._serialize_instance(db_cov_conf))
        return result

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        session = request.state.session
        try:
            data = await self._arrange_data(request, data)
            await self.validate(request, data)
            logger.debug(f"{data=}")
            possible_values_create = []
            for possible_value in data["possible_values"]:
                param_name, param_value = possible_value.partition(" - ")[::2]
                conf_param = database.get_configuration_parameter_by_name(
                    session, param_name)
                conf_param_value = [
                    pv for pv in conf_param.allowed_values if pv.name == param_value][0]
                possible_values_create.append(
                    coverages.ConfigurationParameterPossibleValueCreate(
                        configuration_parameter_value_id=conf_param_value.id)
                )
            related_obs_variable = database.get_variable_by_name(
                session, data["observation_variable"])
            if (
                    uncertainty_lower_name := data.get(
                        "uncertainty_lower_bounds_coverage_configuration")
            ) is not None:
                db_uncertainty_lower = database.get_coverage_configuration_by_name(
                    session, uncertainty_lower_name)
                uncertainty_lower_id = db_uncertainty_lower.id
            else:
                uncertainty_lower_id = None
            if (
                    uncertainty_upper_name := data.get(
                        "uncertainty_upper_bounds_coverage_configuration")
            ) is not None:
                db_uncertainty_upper = database.get_coverage_configuration_by_name(
                    session, uncertainty_upper_name)
                uncertainty_upper_id = db_uncertainty_upper.id
            else:
                uncertainty_upper_id = None
            cov_conf_create = coverages.CoverageConfigurationCreate(
                name=data["name"],
                netcdf_main_dataset_name=data["netcdf_main_dataset_name"],
                thredds_url_pattern=data["thredds_url_pattern"],
                unit=data["unit"],
                palette=data["palette"],
                color_scale_min=data["color_scale_min"],
                color_scale_max=data["color_scale_max"],
                possible_values=possible_values_create,
                observation_variable_id=(
                    related_obs_variable.id if related_obs_variable else None),
                observation_variable_aggregation_type=data.get(
                    "observation_variable_aggregation_type"),
                uncertainty_lower_bounds_coverage_configuration_id=uncertainty_lower_id,
                uncertainty_upper_bounds_coverage_configuration_id=uncertainty_upper_id,
            )
            db_cov_conf = await anyio.to_thread.run_sync(
                database.create_coverage_configuration,
                session,
                cov_conf_create
            )
            return self._serialize_instance(db_cov_conf)
        except Exception as e:
            return self.handle_exception(e)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        session = request.state.session
        try:
            data = await self._arrange_data(request, data, True)
            await self.validate(request, data)

            possible_values = []
            for pv in data["possible_values"]:
                param_name, param_value = pv.rpartition(" - ")[::2]
                conf_param = database.get_configuration_parameter_by_name(session, param_name)
                conf_param_value = [pv for pv in conf_param.allowed_values if pv.name == param_value][0]
                possible_values.append(
                    coverages.ConfigurationParameterPossibleValueUpdate(
                        configuration_parameter_value_id=conf_param_value.id)
                )
            related_obs_variable = database.get_variable_by_name(
                session, data["observation_variable"])
            if (
                    uncertainty_lower_name := data.get(
                        "uncertainty_lower_bounds_coverage_configuration")
            ) is not None:
                db_uncertainty_lower = database.get_coverage_configuration_by_name(
                    session, uncertainty_lower_name)
                uncertainty_lower_id = db_uncertainty_lower.id
            else:
                uncertainty_lower_id = None
            if (
                    uncertainty_upper_name := data.get(
                        "uncertainty_upper_bounds_coverage_configuration")
            ) is not None:
                db_uncertainty_upper = database.get_coverage_configuration_by_name(
                    session, uncertainty_upper_name)
                uncertainty_upper_id = db_uncertainty_upper.id
            else:
                uncertainty_upper_id = None
            cov_conv_update = coverages.CoverageConfigurationUpdate(
                name=data.get("name"),
                netcdf_main_dataset_name=data.get("netcdf_main_dataset_name"),
                thredds_url_pattern=data.get("thredds_url_pattern"),
                unit=data.get("data"),
                palette=data.get("palette"),
                color_scale_min=data.get("color_scale_min"),
                color_scale_max=data.get("color_scale_max"),
                possible_values=possible_values,
                observation_variable_id=(
                    related_obs_variable.id if related_obs_variable else None),
                observation_variable_aggregation_type=data.get(
                    "observation_variable_aggregation_type"),
                uncertainty_lower_bounds_coverage_configuration_id=uncertainty_lower_id,
                uncertainty_upper_bounds_coverage_configuration_id=uncertainty_upper_id,
            )
            db_coverage_configuration = await anyio.to_thread.run_sync(
                database.get_coverage_configuration,
                session,
                pk
            )
            db_coverage_configuration = await anyio.to_thread.run_sync(
                database.update_coverage_configuration,
                session,
                db_coverage_configuration,
                cov_conv_update
            )
            return self._serialize_instance(db_coverage_configuration)
        except Exception as e:
            self.handle_exception(e)

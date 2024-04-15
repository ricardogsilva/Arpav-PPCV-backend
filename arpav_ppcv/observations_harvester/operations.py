import httpx
import logging
import sqlmodel

from .. import (
    database,
)
from ..schemas import models

logger = logging.getLogger(__name__)


def harvest_variables(
        client: httpx.Client,
        db_session: sqlmodel.Session
) -> tuple[
    list[models.VariableCreate],
    list[tuple[models.Variable, models.VariableUpdate]]
]:
    """
    Queries remote API and returns a tuple with variables to create and update.
    """
    existing_variables = {v.name: v for v in database.collect_all_variables(db_session)}
    response = client.get(
        "https://api.arpa.veneto.it/REST/v1/provaclima/indi",
    )
    response.raise_for_status()
    to_create = []
    to_update = []
    for var_info in response.json().get("data", []):
        variable_create = models.VariableCreate(
            name=var_info["indicatore"],
            description=var_info["descrizione"],
        )
        if variable_create.name not in existing_variables:
            to_create.append(variable_create)
        else:
            existing_variable = existing_variables[variable_create.name]
            if existing_variable.description != variable_create.description:
                to_update.append(
                    (
                        existing_variable,
                        models.VariableUpdate(description=variable_create.description)
                    )
                )
    return to_create, to_update


def refresh_variables(
        client: httpx.Client,
        db_session: sqlmodel.Session
) -> tuple[list[models.Variable], list[models.Variable]]:
    to_create, to_update = harvest_variables(client, db_session)
    logger.info(f"About to create {len(to_create)} variables...")
    created_variables = database.create_many_variables(db_session, to_create)
    logger.info(f"About to update {len(to_update)} variables...")
    updated_variables = []
    for db_var, var_update in to_update:
        updated = database.update_variable(db_session, db_var, var_update)
        updated_variables.append(updated)
    return created_variables, updated_variables

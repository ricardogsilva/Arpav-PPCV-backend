import itertools
import re

from .. import config


def list_dataset_configurations(
        settings: config.ArpavPpcvSettings
) -> dict[str, config.ThreddsDatasetSettings]:
    return settings.thredds_server.datasets


def list_dataset_identifiers(
        dataset_config_identifier: str,
        dataset_config: config.ThreddsDatasetSettings
) -> list[str]:
    pattern_parts = re.findall(
        r"\{(\w+)\}",
        dataset_config.dataset_id_pattern.partition("-")[-1])
    values_to_combine = []
    for part in pattern_parts:
        part_allowed_values = dataset_config.allowed_values.get(part, [])
        values_to_combine.append(part_allowed_values)
    result = []
    for combination in itertools.product(*values_to_combine):
        dataset_id = "-".join((dataset_config_identifier, *combination))
        result.append(dataset_id)
    return result


from .. import config


def list_dataset_configurations(
        settings: config.ArpavPpcvSettings
) -> dict[str, config.ThreddsDatasetSettings]:
    return settings.thredds_server.datasets

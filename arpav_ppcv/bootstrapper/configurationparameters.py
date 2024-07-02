from ..schemas.coverages import (
    ConfigurationParameterCreate,
    ConfigurationParameterValueCreateEmbeddedInConfigurationParameter,
)


def generate_configuration_parameters() -> list[ConfigurationParameterCreate]:
    return [
        ConfigurationParameterCreate(
            name="scenario",
            display_name_english="Scenario",
            display_name_italian="Scenario",
            description_english="Climate model scenario",
            description_italian="Scenario del modello climatico",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp26",
                    display_name_english="RCP2.6",
                    display_name_italian="RCP2.6",
                    description_english=(
                        "Representation Concentration Pathway (RCP) scenario that "
                        "assumes climate forcing values of 2.6 W/m2"
                    ),
                    description_italian=(
                        "Scenario Representation Concentration Pathway (RCP) che "
                        "presuppone valori di forzante climatica di 2,6 W/m2"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp45",
                    display_name_english="RCP4.5",
                    display_name_italian="RCP4.5",
                    description_english=(
                        "Representation Concentration Pathway (RCP) scenario that "
                        "assumes climate forcing values of 4.5 W/m2"
                    ),
                    description_italian=(
                        "Scenario Representation Concentration Pathway (RCP) che "
                        "presuppone valori di forzante climatica di 4,5 W/m2"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp85",
                    display_name_english="RCP8.5",
                    display_name_italian="RCP8.5",
                    description_english=(
                        "Representation Concentration Pathway (RCP) scenario that "
                        "assumes climate forcing values of 8.5 W/m2"
                    ),
                    description_italian=(
                        "Scenario Representation Concentration Pathway (RCP) che "
                        "presuppone valori di forzante climatica di 8,5 W/m2"
                    ),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="time_window",
            display_name_english="Time window",
            display_name_italian="Finestra temporale",
            description_english="",
            description_italian="",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tw1",
                    display_name_english="TW1",
                    display_name_italian="TW1",
                    description_english=(
                        "Represents the first anomaly time window, which spans the "
                        "period 2021-2050, with regard to the 1976-2005 period"
                    ),
                    description_italian=(
                        "Rappresenta la prima finestra temporale di anomalia, che "
                        "abbraccia il periodo 2021-2050, rispetto al periodo 1976-2005"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tw2",
                    display_name_english="TW2",
                    display_name_italian="TW2",
                    description_english=(
                        "Represents the second anomaly time window, which spans the "
                        "period 2071-2100, with regard to the 1976-2005 period"
                    ),
                    description_italian=(
                        "Rappresenta la seconda finestra temporale di anomalia, che "
                        "abbraccia il periodo 2071-2100, rispetto al periodo 1976-2005"
                    ),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="year_period",
            display_name_english="Year period",
            display_name_italian="Periodo dell'anno",
            description_english="Yearly temporal aggregation period",
            description_italian="Periodo di aggregazione temporale annuale",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="DJF",
                    display_name_english="Winter",
                    display_name_italian="Inverno",
                    description_english=(
                        "Climatological winter season (December, January, February)"
                    ),
                    description_italian=(
                        "Stagione climatologica invernale (dicembre, gennaio, febbraio)"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="MAM",
                    display_name_english="Spring",
                    display_name_italian="Primavera",
                    description_english=(
                        "Climatological spring season (March, April, May)"
                    ),
                    description_italian=(
                        "Stagione climatologica primaverile (marzo, aprile, maggio)"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="JJA",
                    display_name_english="Summer",
                    display_name_italian="Estate",
                    description_english=(
                        "Climatological summer season (June, July, August)"
                    ),
                    description_italian=(
                        "Stagione climatologica estiva (giugno, luglio, agosto)"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="SON",
                    display_name_english="Autumn",
                    display_name_italian="Autunno",
                    description_english=(
                        "Climatological autumn season (September, October, November)"
                    ),
                    description_italian=(
                        "Stagione climatologica autunnale (settembre, ottobre, novembre)"
                    ),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="measure",
            display_name_english="Measurement type",
            display_name_italian="Tipo di misurazione",
            description_english="Type of climatological measurement",
            description_italian="Tipo di misurazione climatologica",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="absolute",
                    display_name_english="Absolute value",
                    display_name_italian="Valore assoluto",
                    description_english=(
                        "Represents the climatological variable's absolute value"
                    ),
                    description_italian=(
                        "Rappresenta il valore assoluto della variabile climatologica"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="anomaly",
                    display_name_english="Climatological anomaly",
                    display_name_italian="Anomalia climatologica",
                    description_english=(
                        "Represents climatological anomaly values for the variable"
                    ),
                    description_italian=(
                        "Rappresenta i valori di anomalia climatologica per la variabile"
                    ),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="climatological_model",
            display_name_english="Forecast model",
            display_name_italian="Modello di previsione",
            description_english=(
                "Numerical model used to generate climatological forecast datasets"
            ),
            description_italian=(
                "Modello numerico utilizzato per generare set di dati di previsione "
                "climatologica"
            ),
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="model_ensemble",
                    display_name_english="5 Model ensemble",
                    display_name_italian="Insieme di 5 modelli",
                    description_english=(
                        "Ensemble of five climatological models: EC-EARTH CCLM4-8-17, "
                        "EC-EARTH RACMO22E, EC-EARTH RCA4, HadGEM RACMO22E, "
                        "MPI-ESM-LR-REMO2009"
                    ),
                    description_italian=(
                        "Insieme di cinque modelli climatologici: EC-EARTH CCLM4-8-17, "
                        "EC-EARTH RACMO22E, EC-EARTH RCA4, HadGEM RACMO22E, "
                        "MPI-ESM-LR-REMO2009"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="ec_earth_cclm_4_8_17",
                    display_name_english="EC-EARTH CCLM4-8-17",
                    display_name_italian="EC-EARTH CCLM4-8-17",
                    description_english="EC-Earth CCLM4-8-17 model",
                    description_italian="Modello EC-Earth CCLM4-8-17",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="ec_earth_racmo22e",
                    display_name_english="EC-EARTH RACMO22E",
                    display_name_italian="EC-EARTH RACMO22E",
                    description_english="EC-Earth RACMO22E model",
                    description_italian="Modello EC-Earth RACMO22E",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="ec_earth_rca4",
                    display_name_english="EC-EARTH RCA4",
                    display_name_italian="EC-EARTH RCA4",
                    description_english="EC-Earth RCA4 model",
                    description_italian="Modello EC-Earth RCA4",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="hadgem2_racmo22e",
                    display_name_english="HadGEM RACMO22E",
                    display_name_italian="HadGEM RACMO22E",
                    description_english="HadGEM RACMO22E model",
                    description_italian="Modello HadGEM RACMO22E",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="mpi_esm_lr_remo2009",
                    display_name_english="MPI-ESM-LR-REMO2009",
                    display_name_italian="MPI-ESM-LR-REMO2009",
                    description_english="MPI-ESM-LR-REMO2009 model",
                    description_italian="Modello MPI-ESM-LR-REMO2009",
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="aggregation_period",
            display_name_english="Temporal aggregation period",
            display_name_italian="Periodo di aggregazione temporale",
            description_english="Aggregation period for climatological datasets",
            description_italian="Periodo di aggregazione per i set di dati climatologici",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="30yr",
                    display_name_english="30 Years",
                    display_name_italian="30 anni",
                    description_english="Datasets contain aggregation of 30 years",
                    description_italian=(
                        "I set di dati contengono un'aggregazione di 30 anni"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="annual",
                    display_name_english="Annual",
                    display_name_italian="Annuale",
                    description_english=(
                        "Datasets contain aggregation of yearly values"
                    ),
                    description_italian=(
                        "I set di dati contengono aggregazioni di valori annuali"
                    ),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="uncertainty_type",
            display_name_english="Uncertainty type",
            display_name_italian="Tipologia dei limiti di incertezza",
            description_english="Type of uncertainty that this configuration represents",
            description_italian="Tipo di incertezza che questa configurazione rappresenta",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="upper_bound",
                    display_name_english="Uncertainty upper bounds",
                    display_name_italian="Limiti superiori dell'incertezza",
                    description_english=(
                        "Dataset contains upper bound uncertainty-related values"
                    ),
                    description_italian=(
                        "Il set di dati contiene valori relativi all'incertezza del "
                        "limite superiore"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="lower_bound",
                    display_name_english="Uncertainty lower bounds",
                    display_name_italian="Limiti inferiori dell'incertezza",
                    description_english=(
                        "Dataset contains lower bound uncertainty-related values"
                    ),
                    description_italian=(
                        "Il set di dati contiene valori relativi all'incertezza del "
                        "limite inferiore"
                    ),
                ),
            ],
        ),
    ]

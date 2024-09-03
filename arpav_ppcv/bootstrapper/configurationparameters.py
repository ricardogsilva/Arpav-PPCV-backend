from ..schemas.coverages import (
    ConfigurationParameterCreate,
    ConfigurationParameterValueCreateEmbeddedInConfigurationParameter,
)


def generate_configuration_parameters() -> list[ConfigurationParameterCreate]:
    return [
        ConfigurationParameterCreate(
            name="observation_variable",
            display_name_english="Variable",
            display_name_italian="Variabile",
            description_english="Observation variable",
            description_italian="Variabile di osservazione",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tdd",
                    display_name_english="Average temperature",
                    display_name_italian="Temperatura media",
                    description_english="Average of average temperatures",
                    description_italian="Media delle temperature medie",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tnd",
                    display_name_english="Minimum temperature",
                    display_name_italian="Temperatura minima",
                    description_english="Average of minimum temperatures",
                    description_italian="Media delle temperature minime",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="txd",
                    display_name_english="Maximum temperature",
                    display_name_italian="Temperatura massima",
                    description_english="Average of maximum temperatures",
                    description_italian="Media delle temperature massime",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tr",
                    display_name_english="Tropical nights",
                    display_name_italian="Notti tropicali",
                    description_english=(
                        "Number of days with minimum temperature higher than 20°C"
                    ),
                    description_italian=(
                        "Numero di giorni con temperatura minima maggiore di 20°C"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="su30",
                    display_name_english="Hot days",
                    display_name_italian="Giorni caldi",
                    description_english=(
                        "Number of days with maximum temperature above 30°C"
                    ),
                    description_italian=(
                        "Numero di giorni con temperatura massima maggiore di 30°C"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="fd",
                    display_name_english="Frosty days",
                    display_name_italian="Giorni di gelo",
                    description_english=(
                        "Number of days with minimum temperature below 0°C"
                    ),
                    description_italian=(
                        "Numero di giorni con temperatura minima minore di 0°C"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="hdds",
                    display_name_english="Heating degree days",
                    display_name_italian="Gradi giorno di riscaldamento",
                    description_english=(
                        "Sum of 20°C minus the average daily temperature if the "
                        "average daily temperature is less than 20°C."
                    ),
                    description_italian=(
                        "Somma di 20°C meno la temperatura media giornaliera se la "
                        "temperatura media giornaliera è minore di 20°C."
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="cdds",
                    display_name_english="Cooling degree days",
                    display_name_italian="Gradi giorno di raffrescamento",
                    description_english=(
                        "Sum of the average daily temperature minus 21°C if the average "
                        "daily temperature is greater than 24°C."
                    ),
                    description_italian=(
                        "Somma della temperatura media giornaliera meno 21°C se la "
                        "temperatura media giornaliera è maggiore di 24°C."
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="prcptot",
                    display_name_english="Precipitation",
                    display_name_italian="Precipitazione",
                    description_english=("Daily precipitation near the ground"),
                    description_italian=("Precipitazione giornaliera vicino al suolo"),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="climatological_variable",
            display_name_english="Variable",
            display_name_italian="Variabile",
            description_english="Climatological variable",
            description_italian="Variabile climatologica",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="cdd",
                    display_name_english="CDD",
                    display_name_italian="CDD",
                    description_english="Consecutive Dry Days",
                    description_italian="Giorni secchi",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="cdds",
                    display_name_english="CDDs",
                    display_name_italian="CDDs",
                    description_english="Cooling degree days",
                    description_italian="Gradi giorno di raffrescamento",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="fd",
                    display_name_english="FD",
                    display_name_italian="FD",
                    description_english="Frozen Days",
                    description_italian="Giorni di gelo",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="hdds",
                    display_name_english="HDDs",
                    display_name_italian="HDDs",
                    description_english="Heating degree days",
                    description_italian="Gradi giorno di riscaldamento",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="hwdi",
                    display_name_english="HWDI",
                    display_name_italian="HWDI",
                    description_english="Duration of heat waves",
                    description_italian="Durata delle ondate di calore",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="pr",
                    display_name_english="PR",
                    display_name_italian="PR",
                    description_english="Rainfall",
                    description_italian="Precipitazione",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="r95ptot",
                    display_name_english="R95pTOT",
                    display_name_italian="R95pTOT",
                    description_english="Extreme rainfall",
                    description_italian="Precipitazione estrema",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="snwdays",
                    display_name_english="SNWDAYS",
                    display_name_italian="SNWDAYS",
                    description_english="Days with new snow",
                    description_italian="Giorni con neve nuova",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="su30",
                    display_name_english="SU30",
                    display_name_italian="SU30",
                    description_english="Hot days",
                    description_italian="Giorni caldi",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tas",
                    display_name_english="TAS",
                    display_name_italian="TAS",
                    description_english="Mean temperature",
                    description_italian="Temperatura media",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tasmax",
                    display_name_english="TASMAX",
                    display_name_italian="TASMAX",
                    description_english="Maximum temperature",
                    description_italian="Temperatura massima",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tasmin",
                    display_name_english="TASMIN",
                    display_name_italian="TASMIN",
                    description_english="Minimum temperature",
                    description_italian="Temperatura minima",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tr",
                    display_name_english="TR",
                    display_name_italian="TR",
                    description_english="Tropical nights",
                    description_italian="Notti tropicali",
                ),
            ],
        ),
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
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="year",
                    display_name_english="Year",
                    display_name_italian="Anno",
                    description_english="Whole year",
                    description_italian="L'intero anno",
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
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="barometro_climatico",
                    display_name_english="Climate barometer",
                    display_name_italian="Barometro climatico",
                    description_english="Regional overview",
                    description_italian="Panoramica regionale",
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
        ConfigurationParameterCreate(
            name="collection",
            display_name_english="Dataset collection",
            display_name_italian="Raccolta di set di dati",
            description_english="The collection that the dataset belongs to",
            description_italian="La raccolta a cui appartiene il set di dati",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="historical",
                    display_name_english="Historical data",
                    display_name_italian="Dati storici",
                    description_english=("Datasets obtained from historical data"),
                    description_italian=("Set di dati ottenuti da dati storici"),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="forecast",
                    display_name_english="Forecast data",
                    display_name_italian="Dati di previsione",
                    description_english=("Datasets obtained from forecasts"),
                    description_italian=("Set di dati ottenuti dalle previsioni"),
                ),
            ],
        ),
    ]

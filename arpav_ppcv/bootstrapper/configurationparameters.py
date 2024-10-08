from ..schemas.base import CoreConfParamName
from ..schemas.coverages import (
    ConfigurationParameterCreate,
    ConfigurationParameterValueCreateEmbeddedInConfigurationParameter,
)


def generate_configuration_parameters() -> list[ConfigurationParameterCreate]:
    return [
        ConfigurationParameterCreate(
            name=CoreConfParamName.HISTORICAL_VARIABLE.value,
            display_name_english="Variable",
            display_name_italian="Variabile",
            description_english="Historical variable",
            description_italian="Variabile storica",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="tdd",
                    display_name_english="Average temperature",
                    display_name_italian="Temperatura media",
                    description_english="Average of average temperatures",
                    description_italian="Media delle temperature medie",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="tnd",
                    display_name_english="Minimum temperature",
                    display_name_italian="Temperatura minima",
                    description_english="Average of minimum temperatures",
                    description_italian="Media delle temperature minime",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="txd",
                    display_name_english="Maximum temperature",
                    display_name_italian="Temperatura massima",
                    description_english="Average of maximum temperatures",
                    description_italian="Media delle temperature massime",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="tr",
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
                    internal_value="su30",
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
                    internal_value="fd",
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
                    internal_value="hdds",
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
                    internal_value="cdds",
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
                    internal_value="prcptot",
                    display_name_english="Precipitation",
                    display_name_italian="Precipitazione",
                    description_english="Daily precipitation near the ground",
                    description_italian="Precipitazione giornaliera vicino al suolo",
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name=CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value,
            display_name_english="Variable",
            display_name_italian="Variabile",
            description_english="Climatological variable",
            description_italian="Variabile climatologica",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="cdd",
                    display_name_english="CDD",
                    display_name_italian="CDD",
                    description_english="Consecutive Dry Days",
                    description_italian="Giorni secchi",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="cdds",
                    display_name_english="CDDs",
                    display_name_italian="CDDs",
                    description_english="Cooling degree days",
                    description_italian="Gradi giorno di raffrescamento",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="fd",
                    display_name_english="FD",
                    display_name_italian="FD",
                    description_english="Frozen Days",
                    description_italian="Giorni di gelo",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="hdds",
                    display_name_english="HDDs",
                    display_name_italian="HDDs",
                    description_english="Heating degree days",
                    description_italian="Gradi giorno di riscaldamento",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="hwdi",
                    display_name_english="HWDI",
                    display_name_italian="HWDI",
                    description_english="Duration of heat waves",
                    description_italian="Durata delle ondate di calore",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="pr",
                    display_name_english="PR",
                    display_name_italian="PR",
                    description_english="Rainfall",
                    description_italian="Precipitazione",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="r95ptot",
                    display_name_english="R95pTOT",
                    display_name_italian="R95pTOT",
                    description_english="Extreme rainfall",
                    description_italian="Precipitazione estrema",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="snwdays",
                    display_name_english="SNWDAYS",
                    display_name_italian="SNWDAYS",
                    description_english="Days with new snow",
                    description_italian="Giorni con neve nuova",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="su30",
                    display_name_english="SU30",
                    display_name_italian="SU30",
                    description_english="Hot days",
                    description_italian="Giorni caldi",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="tas",
                    display_name_english="TAS",
                    display_name_italian="TAS",
                    description_english="Mean temperature",
                    description_italian="Temperatura media",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="tasmax",
                    display_name_english="TASMAX",
                    display_name_italian="TASMAX",
                    description_english="Maximum temperature",
                    description_italian="Temperatura massima",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="tasmin",
                    display_name_english="TASMIN",
                    display_name_italian="TASMIN",
                    description_english="Minimum temperature",
                    description_italian="Temperatura minima",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="tr",
                    display_name_english="TR",
                    display_name_italian="TR",
                    description_english="Tropical nights",
                    description_italian="Notti tropicali",
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name=CoreConfParamName.SCENARIO.value,
            display_name_english="Scenario",
            display_name_italian="Scenario",
            description_english="Climate model scenario",
            description_italian="Scenario del modello climatico",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="rcp26",
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
                    internal_value="rcp45",
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
                    internal_value="rcp85",
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
                    internal_value="tw1",
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
                    internal_value="tw2",
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
                    name="winter",
                    internal_value="DJF",
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
                    name="spring",
                    internal_value="MAM",
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
                    name="summer",
                    internal_value="JJA",
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
                    name="autumn",
                    internal_value="SON",
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
                    internal_value="year",
                    name="all_year",
                    display_name_english="Year",
                    display_name_italian="Anno",
                    description_english="Whole year",
                    description_italian="L'intero anno",
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="historical_year_period",
            display_name_english="year period - historical data",
            display_name_italian="periodo dell'anno - dati storici",
            description_english="Yearly temporal aggregation period for historical data",
            description_italian=(
                "Periodo di aggregazione temporale annuale per i dati storici"
            ),
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="S01",
                    name="winter",
                    display_name_english="Winter",
                    display_name_italian="Inverno",
                    description_english="Winter season",
                    description_italian="Stagione invernale",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="S02",
                    name="spring",
                    display_name_english="Spring",
                    display_name_italian="Primavera",
                    description_english="Spring season",
                    description_italian="Stagione primaverile",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="S03",
                    name="summer",
                    display_name_english="Summer",
                    display_name_italian="Estate",
                    description_english="Summer season",
                    description_italian="Stagione estiva",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="S04",
                    name="autumn",
                    display_name_english="Autumn",
                    display_name_italian="Autunno",
                    description_english="Autumn season",
                    description_italian="Stagione autunnale",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="A00",
                    name="all_year",
                    display_name_english="Year",
                    display_name_italian="Anno",
                    description_english="Whole year",
                    description_italian="L'intero anno",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M01",
                    name="january",
                    display_name_english="January",
                    display_name_italian="Gennaio",
                    description_english="Month of January",
                    description_italian="mese di gennaio",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M02",
                    name="february",
                    display_name_english="February",
                    display_name_italian="Febbraio",
                    description_english="Month of february",
                    description_italian="mese di febbraio",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M03",
                    name="march",
                    display_name_english="March",
                    display_name_italian="Marzo",
                    description_english="Month of march",
                    description_italian="mese di marzo",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M04",
                    name="april",
                    display_name_english="April",
                    display_name_italian="Aprile",
                    description_english="Month of april",
                    description_italian="mese di aprile",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M05",
                    name="may",
                    display_name_english="May",
                    display_name_italian="Maggio",
                    description_english="Month of may",
                    description_italian="mese di maggio",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M06",
                    name="june",
                    display_name_english="June",
                    display_name_italian="Giugno",
                    description_english="Month of sune",
                    description_italian="mese di giugno",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M07",
                    name="july",
                    display_name_english="July",
                    display_name_italian="Luglio",
                    description_english="Month of july",
                    description_italian="mese di luglio",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M08",
                    name="august",
                    display_name_english="August",
                    display_name_italian="Agosto",
                    description_english="Month of august",
                    description_italian="mese di agosto",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M09",
                    name="september",
                    display_name_english="September",
                    display_name_italian="Settembre",
                    description_english="Month of september",
                    description_italian="mese di settembre",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M10",
                    name="october",
                    display_name_english="October",
                    display_name_italian="Ottobre",
                    description_english="Month of october",
                    description_italian="mese di ottobre",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M11",
                    name="november",
                    display_name_english="November",
                    display_name_italian="Novembre",
                    description_english="Month of november",
                    description_italian="mese di novembre",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="M12",
                    name="december",
                    display_name_english="December",
                    display_name_italian="Dicembre",
                    description_english="Month of december",
                    description_italian="mese di dicembre",
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name=CoreConfParamName.MEASURE.value,
            display_name_english="Measurement type",
            display_name_italian="Tipo di misurazione",
            description_english="Type of climatological measurement",
            description_italian="Tipo di misurazione climatologica",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="absolute",
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
                    internal_value="anomaly",
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
            name=CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
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
                    internal_value="model_ensemble",
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
                    internal_value="ec_earth_cclm_4_8_17",
                    display_name_english="EC-EARTH CCLM4-8-17",
                    display_name_italian="EC-EARTH CCLM4-8-17",
                    description_english="EC-Earth CCLM4-8-17 model",
                    description_italian="Modello EC-Earth CCLM4-8-17",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="ec_earth_racmo22e",
                    display_name_english="EC-EARTH RACMO22E",
                    display_name_italian="EC-EARTH RACMO22E",
                    description_english="EC-Earth RACMO22E model",
                    description_italian="Modello EC-Earth RACMO22E",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="ec_earth_rca4",
                    display_name_english="EC-EARTH RCA4",
                    display_name_italian="EC-EARTH RCA4",
                    description_english="EC-Earth RCA4 model",
                    description_italian="Modello EC-Earth RCA4",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="hadgem2_racmo22e",
                    display_name_english="HadGEM RACMO22E",
                    display_name_italian="HadGEM RACMO22E",
                    description_english="HadGEM RACMO22E model",
                    description_italian="Modello HadGEM RACMO22E",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="mpi_esm_lr_remo2009",
                    display_name_english="MPI-ESM-LR-REMO2009",
                    display_name_italian="MPI-ESM-LR-REMO2009",
                    description_english="MPI-ESM-LR-REMO2009 model",
                    description_italian="Modello MPI-ESM-LR-REMO2009",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="barometro_climatico",
                    display_name_english="Climate barometer",
                    display_name_italian="Barometro climatico",
                    description_english="Regional overview",
                    description_italian="Panoramica regionale",
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name=CoreConfParamName.AGGREGATION_PERIOD.value,
            display_name_english="Temporal aggregation period",
            display_name_italian="Periodo di aggregazione temporale",
            description_english="Aggregation period for climatological datasets",
            description_italian="Periodo di aggregazione per i set di dati climatologici",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="30yr",
                    display_name_english="30 Years",
                    display_name_italian="30 anni",
                    description_english="Datasets contain aggregation of 30 years",
                    description_italian=(
                        "I set di dati contengono un'aggregazione di 30 anni"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="annual",
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
                    internal_value="upper_bound",
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
                    internal_value="lower_bound",
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
            name=CoreConfParamName.ARCHIVE.value,
            display_name_english="Dataset archive",
            display_name_italian="archivio di dataset",
            description_english="The archive that the dataset belongs to",
            description_italian="L'archivio a cui appartiene il set di dati",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="historical",
                    display_name_english="Historical data",
                    display_name_italian="Dati storici",
                    description_english=("Datasets obtained from historical data"),
                    description_italian=("Set di dati ottenuti da dati storici"),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="forecast",
                    display_name_english="Forecast data",
                    display_name_italian="Dati di previsione",
                    description_english=("Datasets obtained from forecasts"),
                    description_italian=("Set di dati ottenuti dalle previsioni"),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="climatological_standard_normal",
            display_name_english="Climatological standard normal",
            display_name_italian="Standard climatologico normale",
            description_english="Standard climatological normal periods",
            description_italian="Periodi normali climatologici standard",
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="1981-2010",
                    display_name_english="CN 1981-2010",
                    display_name_italian="CN 1981-2010",
                    description_english=(
                        "Climatological standard normal for the period 1981-2010"
                    ),
                    description_italian=(
                        "Normale standard climatologica per il periodo 1981-2010"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="1991-2020",
                    display_name_english="CN 1991-2020",
                    display_name_italian="CN 1991-2020",
                    description_english=(
                        "Climatological standard normal for the period 1991-2020"
                    ),
                    description_italian=(
                        "Normale standard climatologica per il periodo 1991-2020"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    internal_value="2001-2030",
                    display_name_english="CN 2001-2030",
                    display_name_italian="CN 2001-2030",
                    description_english=(
                        "Climatological standard normal for the period 2001-2030"
                    ),
                    description_italian=(
                        "Normale standard climatologica per il periodo 2001-2030"
                    ),
                ),
            ],
        ),
    ]

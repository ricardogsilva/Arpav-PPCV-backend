from ..schemas.observations import VariableCreate


def generate_variable_configurations() -> list[VariableCreate]:
    return [
        VariableCreate(
            name="TDd",
            display_name_english="Mean temperature",
            display_name_italian="Temperatura media",
            description_english="Average daily air temperature near the ground",
            description_italian=(
                "Temperatura media giornaliera dell'aria vicino al suolo"
            ),
            unit_english="ºC",
        ),
        VariableCreate(
            name="TXd",
            display_name_english="Max temperature",
            display_name_italian="Temperatura massima",
            description_english="Maximum daily air temperature near the ground",
            description_italian=(
                "Temperatura massima giornaliera dell'aria vicino al suolo"
            ),
            unit_english="ºC",
        ),
        VariableCreate(
            name="TNd",
            display_name_english="Minimum temperature",
            display_name_italian="Temperatura minima",
            description_english="Minimum daily air temperature near the ground",
            description_italian=(
                "Temperatura minima giornaliera dell'aria vicino al suolo"
            ),
            unit_english="ºC",
        ),
        VariableCreate(
            name="PRCPTOT",
            display_name_english="Rainfall",
            display_name_italian="Precipitazione",
            description_english="Daily precipitation near the ground",
            description_italian="Precipitazioni giornaliere in prossimità del suolo",
            unit_english="mm",
        ),
        VariableCreate(
            name="TR",
            display_name_english="Tropical nights",
            display_name_italian="Notti tropicali",
            description_english=(
                "Number of days with minimum temperature greater than 20 °C"
            ),
            description_italian=(
                "Numero di giorni con temperatura minima superiore a 20 °C"
            ),
            unit_english="days",
            unit_italian="giorni",
        ),
        VariableCreate(
            name="SU30",
            display_name_english="Hot days",
            display_name_italian="Giorni caldi",
            description_english=(
                "Number of days with maximum temperature greater than 30 °C"
            ),
            description_italian=(
                "Numero di giorni con temperatura massima superiore a 30 °C"
            ),
            unit_english="days",
            unit_italian="giorni",
        ),
        VariableCreate(
            name="FD",
            display_name_english="Cold days",
            display_name_italian="Giorni di gelo",
            description_english=(
                "Number of days with minimum temperature less than 0 °C"
            ),
            description_italian=(
                "Numero di giorni con temperatura minima inferiore a 0 °C"
            ),
            unit_english="days",
            unit_italian="giorni",
        ),
    ]

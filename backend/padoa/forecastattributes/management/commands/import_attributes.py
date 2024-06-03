from django.core.management import BaseCommand
from padoa.forecastattributes import models
from padoa.forecastattributes import serializers
from django.conf import settings
from padoa.thredds.models import Map


# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Complete refresh of the attributes',
        )

    # Show this when the user types help
    help = "My test command"

    import_data = {
        "Variable" : [
            {
                "id": "TAS",
                "name": "Temperatura media (TAS)",
                "description": "Temperatura media giornaliera dell’aria vicino al suolo",
                "order_item": 1
            },
            {
                "id": "TASMIN",
                "name": "Temperatura minima (TASMIN)",
                "description": "Temperatura minima giornaliera dell’aria vicino al suolo",
                "order_item": 2
            },
            {
                "id": "TASMAX",
                "name": "Temperatura massima (TASMAX)",
                "description": "Temperatura massima giornaliera dell’aria vicino al suolo",
                "order_item": 3
            },
            {
                "id": "TR",
                "name": "Notti Tropicali (TR)",
                "description": "Numero di giorni con temperatura minima maggiore di 20°C",
                "order_item": 4
            },
            {
                "id": "SU30",
                "name": "Giorni Caldi (SU30)",
                "description": "Numero di giorni con temperatura massima maggiore di 30°C",
                "order_item": 5
            },
            {
                "id": "FD",
                "name": "Giorni di Gelo (FD)",
                "description": "Numero di giorni con temperatura minima minore di 0°C",
                "order_item": 6
            },
            {
                "id": "HWDI",
                "name": "Durata delle ondate di calore (HWDI)",
                "description": "Numero di giorni in cui la temperatura massima è maggiore di 5°C rispetto alla media per almeno 5 giorni consecutivi.",
                "order_item": 7
            },
            {
                "id": "PR",
                "name": "Precipitazione (PR)",
                "description": "Precipitazione giornaliera vicino al suolo",
                "order_item": 8
            },
            {
                "id": "R95pTOT",
                "name": "Precipitazione estrema (R95pTOT)",
                "description": "Precipitazione totale cumulata al di sopra del 95o percentile del periodo di riferimento",
                "order_item": 9
            },
            {
                "id": "CDD",
                "name": "Giorni secchi (CDD)",
                "description": "Numero massimo di giorni consecutivi asciutti (precipitazione giornaliera inferiore a 1 mm)",
                "order_item": 10
            },
            {
                "id": "SNWDAYS",
                "name": "Giorni con neve nuova (SNWDAYS)",
                "description": "Numero di giorni con temperatura media minore di 2°C e precipitazione giornaliera maggiore di 1 mm",
                "order_item": 11
            }
        ],
        "ForecastModel" : [
            {
                # "id": "ens5ym",
                "id": "ens5",
                "name": "Ensemble 5rcm",
                "description": "",
            },
            # {
            #     "id": "ensymbc", #ensymbc
            #     "name": "Ensemble 5rcm BC",
            #     "description": "",
            # },
            {
                "id": "EC-EARTH_CCLM4-8-17", #EC-EARTH_CCLM4-8-17ym
                "name": "EC-EARTH_CCLM4-8-17",
                "description": "",
            },
            # {
            #     "id": "EC-EARTH_CCLM4-8-17", #EC-EARTH_CCLM4-8-17ymbc
            #     "name": "EC-EARTH_CCLM4-8-17bc",
            #     "description": "",
            # },
            {
                "id": "EC-EARTH_RACMO22E",  #EC-EARTH_RACMO22Eym
                "name": "EC-EARTH_RACMO22E",
                "description": "",
            },
            # {
            #     "id": "EC-EARTH_RACMO22E", #EC-EARTH_RACMO22Eymbc
            #     "name": "EC-EARTH_RACMO22Ebc",
            #     "description": "",
            # },
            {
                "id": "EC-EARTH_RCA4", #EC-EARTH_RCA4ym
                "name": "EC-EARTH_RCA4",
                "description": "",
            },
            # {
            #     "id": "EC-EARTH_RCA4bc", #EC-EARTH_RCA4ymbc
            #     "name": "EC-EARTH_RCA4bc",
            #     "description": "",
            # },
            {
                "id": "HadGEM2-ES_RACMO22E", #HadGEM2-ES_RACMO22Eym
                "name": "HadGEM2-ES_RACMO22E",
                "description": "",
            },
            # {
            #     "id": "HadGEM2-ES_RACMO22E", #HadGEM2-ES_RACMO22Eymbc
            #     "name": "HadGEM2-ES_RACMO22Ebc",
            #     "description": "",
            # },
            {
                "id": "MPI-ESM-LR_REMO2009", #MPI-ESM-LR_REMO2009ym
                "name": "MPI-ESM-LR_REMO2009",
                "description": "",
            },
            # {
            #     "id": "MPI-ESM-LR_REMO2009bc", #MPI-ESM-LR_REMO2009ymbc
            #     "name": "MPI-ESM-LR_REMO2009bc",
            #     "description": "",
            # },






            # {
            #     "id": "Ensemble 5rcmbc",
            #     "name": "Ensemble 5rcmbc",
            #     "description": "",
            # },
            # {
            #     "id": "Ensemble 5rcm BCbc",
            #     "name": "Ensemble 5rcm BCbc",
            #     "description": "",
            # },
            # {
            #     "id": "EC-EARTH_CCLM4-8-17bc",
            #     "name": "EC-EARTH_CCLM4-8-17bc",
            #     "description": "",
            # },
            # {
            #     "id": "EC-EARTH_CCLM4-8-17bcbc",
            #     "name": "EC-EARTH_CCLM4-8-17bcbc",
            #     "description": "",
            # },
            # {
            #     "id": "EC-EARTH_RACMO22Ebc",
            #     "name": "EC-EARTH_RACMO22Ebc",
            #     "description": "",
            # },
            # {
            #     "id": "Ensemble",
            #     "name": "Ensemble",
            #     "description": "",
            # },
            # {
            #     "id": "Ensemble_BC",
            #     "name": "Ensemble BC",
            #     "description": "",
            # },
            # {
            #     "id": "NCC-NorESM1-M_HIRHAM5",
            #     "name": "NCC-NorESM1-M_HIRHAM5",
            #     "description": "",
            # },
        ],
        "Scenario" : [
            {
                "id": "Rcp26",
                "name": "rcp2.6",
                "description": "",
            },
            {
                "id": "Rcp45",
                "name": "rcp4.5",
                "description": "",
            },
            {
                "id": "Rcp85",
                "name": "rcp8.5",
                "description": "",
            }
        ],
        "DataSeries" : [
            {
                "id": "yes",
                "name": "Media annuale",
                "description": "",
            },
            {
                "id": "no",
                "name": "Media Trentennale",
                "description": "",
            }
        ],
        "YearPeriod" : [
            {
                "id": "annual",
                "name": "Anno",
                "description": "",
            },
            {
                "id": "djf",
                "name": "Inverno",
                "description": "",
            },
            {
                "id": "mam",
                "name": "Primavera",
                "description": "",
            },
            {
                "id": "jja",
                "name": "Estate",
                "description": "",
            },
            {
                "id": "son",
                "name": "Autunno",
                "description": "",
            },
        ],
        "TimeWindow" : [
            {
                "id": "tw1",
                "name": "2021-2050",
                "description": "Anomalia 2021-2050 rispetto a 1976-2005",
            },
            {
                "id": "tw2",
                "name": "2071-2100",
                "description": "Anomalia 2071-2100 rispetto a 1976-2005",
            }
        ],
        "ValueType" : [
            {
                "id": "anomaly",
                "name": "Anomalia",
                "description": "",
            },
            {
                "id": "absolute",
                "name": "Valore assoluto",
                "description": "",
            }
        ]
    }

    def handle(self, *args, **options):
        if options['clear']:
            Map.objects.all().delete()

        for table,records in self.import_data.items():
            model = getattr(models, table)
            if options['clear']:
                model.objects.all().delete()
            for data in records:
                # serializer = getattr(serializers, table+"Serializer")(data=data)
                # serializer.is_valid(raise_exception=True)
                # serializer.save()
                model.objects.update_or_create(id=data['id'], defaults=data)

        self.stdout.write("Doing All The Things!")

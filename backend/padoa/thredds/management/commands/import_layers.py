import json
from django.contrib.gis.geos import Polygon
from threddsclient import download_urls, opendap_urls, read_url, read_xml, crawl
from threddsclient.nodes import DirectDataset, Dataset, CollectionDataset
from django.core.management import BaseCommand
from django.conf import settings
import time, os, sys, traceback
from padoa.thredds.utils import getOpenDapUrl, getWmsCapabilities, getLayerAttributes, openDapUrl, getThreddsDirectory, getLayerMinMax, getWmsPath
from padoa.forecastattributes.models import *
from padoa.thredds.models import *
from dateutil import parser
# from padoa.thredds.utils import NCSSQuery
from padoa.thredds.utils import getWmsMetadata


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--refresh',
            action='store_true',
            help='Complete refresh of the layers',
        )
    skipping_models = [
        # 'ecafdan',
        # 'ecasuan',
        # 'ecatran',
    ]
    forecastmodel_aliases = {
        'ensymbc': 'ens5',
        'ensembletwbc': 'ens5',
        'EC-EARTH_CCLM4-8-17': 'EC-EARTH_CCLM4-8-17',
    }
    layer_variable_aliases = [
        'heat_wave_duration_index_wrt_mean_of_reference_period',
        'consecutive_dry_days_index_per_time_period',
    ]
    variable_aliases = {
        'heat_waves': 'HWDI',
        'pr_change_cumulative': 'R95pTOT',
        'FD_0': 'FD',
        'ecafdan': 'FD',
        'SU_30': 'SU30',
        'ecasuan': 'SU30',
        'TR_20': 'TR',
        'ecatran': 'TR',
    }
    forecastmodels = []
    dimtypemap = {
        'Serie annuali e stagionali': {
            'DataSeries': 'yes',
            'directories': {
                'Ensemble 5rcm': 'ens5ym',
                'Ensemble 5rcm BC': 'ensymbc',
                'EC-EARTH_CCLM4-8-17': 'EC-EARTH_CCLM4-8-17ym',
                'EC-EARTH_CCLM4-8-17bc': 'EC-EARTH_CCLM4-8-17ymbc',
                'EC-EARTH_RACMO22E': 'EC-EARTH_RACMO22Eym',
                'EC-EARTH_RACMO22Ebc': 'EC-EARTH_RACMO22Eymbc',
                'EC-EARTH_RCA4': 'EC-EARTH_RCA4ym',
                'EC-EARTH_RCA4bc': 'EC-EARTH_RCA4ymbc',
                'HadGEM2-ES_RACMO22E': 'HadGEM2-ES_RACMO22Eym',
                'HadGEM2-ES_RACMO22Ebc': 'HadGEM2-ES_RACMO22Eymbc',
                'MPI-ESM-LR_REMO2009': 'MPI-ESM-LR_REMO2009ym',
                'MPI-ESM-LR_REMO2009bc': 'MPI-ESM-LR_REMO2009ymbc',
            }
        },
         'Anomalie trentennali': {
            'DataSeries': 'no',
            'directories': {
                'Ensemble 5rcm BC': 'ensembletwbc',
                'Temperatura e precipitazione 5rcm': 'taspr5rcm',
                'Indici climatici 5rcm': 'indici5rcm',
             }
        },
    }
    settings = {
            'TAS': {
                'anomaly': {
                    'unit': '°C',
                    'palette': 'seq-YlOrRd',
                    'minmax': [0,6]
                },
                'absolute': {
                    'unit': '°C',
                    'palette': 'seq-YlOrRd',
                    'minmax': [-3,32]
                },
            },
            'TASMAX': {
                'anomaly': {
                    'unit': '°C',
                    'palette': 'seq-YlOrRd',
                    'minmax': [0,6]
                },
                'absolute': {
                    'unit': '°C',
                    'palette': 'seq-YlOrRd',
                    'minmax': [7,37]
                },
            },
            'TASMIN': {
                'anomaly': {
                    'unit': '°C',
                    'palette': 'seq-YlOrRd',
                    'minmax': [0,6]
                },
                'absolute': {
                    'unit': '°C',
                    'palette': 'seq-YlOrRd',
                    'minmax': [-13,27]
                },
            },
            'SU30': {
                'anomaly': {
                    'unit': 'gg',
                    'palette': 'seq-YlOrRd',
                    'minmax': [-5,75]
                },
                'absolute': {
                    'unit': 'gg',
                    'palette': 'seq-YlOrRd',
                    'minmax': [0,100]
                },
            },
            'TR': {
                'anomaly': {
                    'unit': 'gg',
                    'palette': 'seq-YlOrRd',
                    'minmax': [-5,75]
                },
                'absolute': {
                    'unit': 'gg',
                    'palette': 'seq-YlOrRd',
                    'minmax': [0,120]
                },
            },
            'HWDI': {
                'anomaly': {
                    'unit': 'gg',
                    'palette': 'seq-YlOrRd',
                    'minmax': [0,50]
                },
                # 'absolute': {
                #     'minmax': [-50,50]
                # },
            },
            'FD': {
                'anomaly': {
                    'unit': 'gg',
                    'palette': 'seq-YlOrRd-inv',
                    'minmax': [-85,5]
                },
                'absolute': {
                    'unit': 'gg',
                    'palette': 'seq-Blues-inv',
                    'minmax': [0,200]
                },
            },
            'PR': {
                'anomaly': {
                    'unit': '%',
                    'palette': 'div-BrBG',
                    'minmax': [-40,40]
                },
                'absolute': {
                    'unit': 'mm',
                    'palette': 'seq-BuYl-inv',
                    'minmax': [0,3200],
                    'annualminmax': [0,3200],
                    'seasonalminmax': [0,800],
                },
            },
            'R95pTOT': {
                'anomaly': {
                    'unit': '%',
                    'palette': 'div-BrBG',
                    'minmax': [-160,160]
                },
            },
            'CDD': {
                'anomaly': {
                    'unit': 'gg',
                    'palette': 'div-BrBG-inv',
                    'minmax': [-40,40]
                },
            },
            'SNWDAYS': {
                'anomaly': {
                    'unit': 'gg',
                    'palette': 'seq-YlOrBr-inv',
                    'minmax': [-50,0]
                },
                'absolute': {
                    'unit': 'gg',
                    'palette': 'seq-BuYl-inv',
                    'minmax': [0,100] # TODO: WARNING!!!!
                },
            },

        }

    # Show this when the user types help
    help = "My test command"



    def handle(self, *args, **options):
        self.forecastmodels = list(map(lambda x: x.id, ForecastModel.objects.only('id').all()))
        self.scenarios = list(map(lambda x: x.id, Scenario.objects.only('id').all()))
        self.variables = list(map(lambda x: x.id, Variable.objects.only('id').all()))
        self.year_periods = list(map(lambda x: x.id, YearPeriod.objects.only('id').all()))
        self.timewindows = list(map(lambda x: x.id, TimeWindow.objects.only('id').all()))

        # path = 'ensembletwbc/eca_cdd_an_avg_tw1_rcp85_MAM_ls.nc'
        # wmscap = getLayerAttributes(path)
        # layer = wmscap['Layer']
        # print(json.dumps(layer))
        # attributes = self.getAttributes(layer, dimtype='Anomalie trentennali',url_path=path)
        # attributes = self.getAttributes(layer, dimtype='Serie annuali e stagionali',url_path=path)
        # print(attributes)
        # return 0
        for dimtype, items in self.dimtypemap.items():
            print('=============================== '+dimtype+' ===============================')
            for dirname, dirpath in items['directories'].items():
                dir = getThreddsDirectory(dirpath)
                print('    *************************** '+ dir.name + ' => ' + dir.url)
                for datasetcollection in dir.datasets:
                    time.sleep(0.3)
                    for dataset in datasetcollection.datasets:

                        try:
                            if not options['refresh'] and Map.objects.filter(path=dataset.url_path).count() > 0:
                                print('    L____________________ DONE: '+dataset.url_path)
                                continue
                            print('    L__________________________ '+dataset.url_path)
                            if len([m for m in self.skipping_models if m.lower() in dataset.url_path.lower()]) > 0:
                                print('    *** Skipping model ' + dataset.url_path)
                                continue

                            layer = attributes = False
                            wmscap = getLayerAttributes(dataset.url_path)
                            layer = wmscap['Layer']
                            # print(json.dumps(layer))
                            attributes = self.getAttributes(layer, dimtype=dimtype,url_path=dataset.url_path)
                            if type(attributes) == bool and attributes == False:
                                print('        skipping.. ' + dataset.url_path)
                                continue
                            # TODO: saving...
                            Map.objects.update_or_create(path=attributes['path'], defaults=attributes)
                        except Exception as e:
                            print('********************* Error: ')
                            print(e.__dict__)
                            tb_str = "".join(traceback.format_tb(e.__traceback__))
                            print("".join(tb_str))
                            print(json.dumps(layer))
                            # exit(1)
                            continue

    def getAttributes(self, layer, dimtype, url_path):
        # print(json.dumps(layer))
        # exit()
        # wmspath = getWmsPath(url_path)
        # value_type_id = 'absolute' if 'bc' in url_path and not '_an' in url_path and dimtype != 'Anomalie trentennali' else 'anomaly'
        value_type_id = 'absolute' if not '_an' in url_path and not 'an_' in url_path and dimtype != 'Anomalie trentennali' else 'anomaly'
        dataseries_id = self.dimtypemap[dimtype]['DataSeries']
        if type(layer['Layer']['Layer']) == list:
            layer = next(filter(lambda x: x['Name'] in self.layer_variable_aliases , layer['Layer']['Layer']))
        else:
            layer = layer['Layer']['Layer']
        layer_id = layer['Name']
        elevation = None
        if type(layer['Dimension']) == list:
            try:
                elevation = list(filter(lambda x: x['@name'] == 'elevation', layer['Dimension']))[0]
                elevation = int(elevation['@default'].split('.')[0])
            except:
                print('        *** Elevation not found')
                pass
        if dataseries_id == 'yes':
            tw_id = None
            if type(layer['Dimension']) == list:
                timedimension = list(filter(lambda x: x['@name'] == 'time', layer['Dimension']))[0]
            else:
                timedimension = layer['Dimension']
            timedimension = timedimension['#text'].split(',')
            time_start = timedimension[0].split('/')[0]
            # print(time_start)
            latest_time = timedimension[-1].split('/')
            time_end = latest_time[1] if len(latest_time) > 1 else latest_time[0]
            # print(time_end)
            time_interval = latest_time[-1]
            # print('        time_interval: ' + time_interval)
            # exit(json.dumps([time_start,time_end,time_interval]))
        else:
            time_interval = None
            if type(layer['Dimension']) == list:
                timedimension = list(filter(lambda x: x['@name'] == 'time', layer['Dimension']))[0]
                time_start = time_end = timedimension['@default']
            else:
                timedimension = layer['Dimension']
                time_start = time_end = timedimension['@default']
            tw_id = [m for m in self.timewindows if m.lower() in url_path.split('/')[1].lower()]
            if len(tw_id) == 0:
                print("tw_id NOT FOUND " + url_path)
                raise Exception("tw_id NOT FOUND " + url_path)
            if len(tw_id) > 1:
                print("TOO MANY forecast_model_id FOUND " + url_path)
                raise Exception("TOO MANY forecast_model_id FOUND " + url_path)
            tw_id = tw_id[0]
        bbox = layer['BoundingBox']
        base_dir = url_path.split('/')[0]
        if base_dir in self.forecastmodel_aliases.keys():
            forecast_model_id = self.forecastmodel_aliases[base_dir]
        else:
            forecast_model_id = [m for m in self.forecastmodels if m.lower() in url_path.lower()]
            if len(forecast_model_id) == 0:
                print("    *** Skipping model for forecast_model_id NOT FOUND " + url_path)
                return False
                # raise Exception("forecast_model_id NOT FOUND " + url_path)
            elif len(forecast_model_id) > 1:
                print("    *** Skipping model for TOO MANY forecast_model_id FOUND " + url_path)
                return False
                # raise Exception("TOO MANY forecast_model_id FOUND " + url_path)
            forecast_model_id = forecast_model_id[0]

        variable_aliases = [m for m in self.variable_aliases.keys() if m.lower() in url_path.lower()]
        if len(variable_aliases) > 0:
            variable_id = self.variable_aliases[variable_aliases[0]]
        else:
            variable_id = [m for m in self.variables if m.lower() in url_path.lower()]
            if len(variable_id) == 0:
                print("    *** Skipping model for variable_id NOT FOUND " + url_path)
                return False
                # raise Exception("variable_id NOT FOUND " + url_path)
            elif len(variable_id) > 1:
                # print("TOO MANY variable_id FOUND " + url_path)
                looking_for_exact_var = [m for m in self.variables if m.lower() == url_path.split('/')[1].split('_')[0].lower()]
                if len(looking_for_exact_var) != 1:
                    print(looking_for_exact_var)
                    print("    *** Skipping model for TOO MANY variable_id FOUND " + url_path)
                    return False
                    # raise Exception("TOO MANY variable_id FOUND " + url_path)
                variable_id = looking_for_exact_var
                # raise Exception("TOO MANY variable_id FOUND " + url_path)
            variable_id = variable_id[0]


        scenario_id = [m for m in self.scenarios if m.lower() in url_path.lower()]
        if len(scenario_id) == 0:
            print("    *** Skipping model for MODEL NOT FOUND " + url_path)
            return False
            # raise Exception("MODEL NOT FOUND " + url_path)
        elif len(scenario_id) > 1:
            print("    *** Skipping model for TOO MANY MODEL FOUND " + url_path)
            return False
            # raise Exception("TOO MANY MODEL FOUND " + url_path)
        scenario_id = scenario_id[0]

        year_period_id = [m for m in self.year_periods if m.lower() in url_path.lower()]
        if len(year_period_id) == 0:
            year_period_id = ['annual']
        elif len(year_period_id) > 1:
            print(year_period_id)
            print("    *** Skipping model for TOO MANY year_periods FOUND " + url_path)
            return False
        year_period_id = year_period_id[0]
        # min_max = getLayerMinMax(url_path, layer)
        # color_scale_min = min_max['min']
        # color_scale_max = min_max['max']
        # print(variable_id)
        # print(value_type_id)
        if year_period_id == 'annual' and 'annualminmax' in self.settings[variable_id][value_type_id]:
            print('        annualminmax')
            color_scale_min = self.settings[variable_id][value_type_id]['annualminmax'][0]
            color_scale_max = self.settings[variable_id][value_type_id]['annualminmax'][1]
        elif 'seasonalminmax' in self.settings[variable_id][value_type_id]:
            print('        seasonalminmax')
            color_scale_min = self.settings[variable_id][value_type_id]['seasonalminmax'][0]
            color_scale_max = self.settings[variable_id][value_type_id]['seasonalminmax'][1]
        else:
            color_scale_min = self.settings[variable_id][value_type_id]['minmax'][0]
            color_scale_max = self.settings[variable_id][value_type_id]['minmax'][1]
        # if self.settings[variable_id][value_type_id]
        palette = self.settings[variable_id][value_type_id]['palette']
        unit = self.settings[variable_id][value_type_id]['unit']
        if variable_id in ['TAS', 'TASMIN', 'TASMAX']:
            ts = getWmsMetadata(url_path, layer_id)
            if ts['units'] == 'K' and value_type_id != 'anomaly':
                print('        *** Converting from celsius to K')
                unit = 'K'
                color_scale_min = color_scale_min + 273
                color_scale_max = color_scale_max + 273

        if time_start[5:7] == '02' and time_start[8:10] > '28':
            print('        *** Adjusting time_start to 28th of February')
            time_start = time_start[:8] + '28' + time_start[10:]
        if time_end[5:7] == '02' and time_end[8:10] > '28':
            print('        *** Adjusting time_end to 28th of February')
            time_end = time_end[:8] + '28' + time_end[10:]
        time_start = parser.parse(time_start)
        # if time_start.month == 2 and time_start.day > 28:
        #     time_start = time_start.replace(day=28)
        time_end = parser.parse(time_end)
        # if time_end.month == 2 and time_end.day > 28:
        #     time_end = time_end.replace(day=28)

        return {
            'spatialbounds': Polygon.from_bbox((bbox["@minx"], bbox["@miny"], bbox["@maxx"], bbox["@maxy"])),
            # xmin, ymin, xmax, ymax
            'csr': bbox["@CRS"],
            'variable_id': variable_id,
            'forecast_model_id': forecast_model_id,
            'scenario_id': scenario_id,
            'data_series_id': dataseries_id,
            'year_period_id': year_period_id,
            'time_window_id': tw_id,
            'value_type_id': value_type_id,
            'time_start': time_start,
            'time_end': time_end,
            'time_interval': time_interval,
            'layer_id': layer_id,
            'path': url_path,
            'color_scale_min': color_scale_min,
            'color_scale_max': color_scale_max,
            # 'layer_url': wmspath,
            'palette': palette,
            'unit': unit,
            'elevation': elevation,
        }

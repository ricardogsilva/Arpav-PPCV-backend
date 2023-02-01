# import geohash, json
# from django.contrib.gis.geos import Polygon
# from django.db.models import CharField, Value
# from django.db.models.aggregates import Aggregate
#
#
# def get_geohash_from_position(latitude, longitude, precision=7):
#     geo_hash = str(geohash.encode(latitude, longitude, precision))
#     return geo_hash
#
# def get_position_from_geohash(geo_hash):
#     # position = geohash.decode_exactly(geo_hash)
#     position = geohash.decode(geo_hash)
#     return position
#
# def get_poligon_from_geohash(geo_hash):
#     position = geohash.bbox(geo_hash)
#     polygon = Polygon.from_bbox((position.get('w'), position.get('s'), position.get('e'), position.get('n')))
#     return json.loads(polygon.geojson)
#
# class GroupConcat(Aggregate):
#     function = 'GROUP_CONCAT'
#     template = '%(function)s(%(expressions)s)'
#
#     def __init__(self, expression, delimiter, order_by=None, **extra):
#         output_field = extra.pop('output_field', CharField())
#         delimiter = Value(delimiter)
#
#         super(GroupConcat, self).__init__(
#             expression, delimiter, output_field=output_field, **extra)
#
#     def as_postgresql(self, compiler, connection):
#         self.function = 'STRING_AGG'
#         return super(GroupConcat, self).as_sql(compiler, connection)

from django.contrib.gis.geos import GEOSGeometry, GEOSException


class ConvertGeometry:
    def __init__(self, data, geometry_type):
        self.data = data
        self.geometry_type = geometry_type

    def convert_geometry(self):
        if self.geometry_type == 'polygon':
            return self._convert_polygon()
        if self.geometry_type == 'linestring':
            return self._convert_linestring()
        if self.geometry_type == 'point':
            return self._convert_point()

    def _convert_polygon(self):
        '''
         Get the polygon from the  array
         Convert the polygon in Polygon object
        '''

        polygon_raw_string = ''
        for i in self.data:
            if i in polygon_raw_string:
                pass
            else:
                polygon_raw_string += i
                polygon_raw_string += ' , '

        polygon_raw_string += self.data[0]
        wkt = "POLYGON(("+polygon_raw_string+"))"
        try:
            polygon = GEOSGeometry(wkt)
            polygon.srid = 4326
        except GEOSException:
            polygon = None
        return polygon

    def _convert_linestring(self):
        '''
         Get the route from the  array
         Convert the route in LineString object
        '''

        linestring_raw = ''
        k = 0
        for i in self.data:
            k += 1
            if i in linestring_raw:
                pass
            else:
                linestring_raw += i
                linestring_raw += ','
        wkt = "LineString({})".format(linestring_raw).replace(',)', ')')
        try:
            linestring = GEOSGeometry(wkt)
            linestring.srid = 4326
        except GEOSException:
            linestring = None
        return linestring

    def _convert_point(self):
        '''
         Get the point lat , lng
         Convert the point in Point object
        '''

        lng = self.data[0]
        lat = self.data[1]
        wkt = "POINT({} {})".format(lng, lat)
        print(wkt)
        try:
            point = GEOSGeometry(wkt)
            point.srid = 4326
        except GEOSException:
            point = None
        return point

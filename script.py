import traceback
from osgeo import ogr
import json

# path to csv file with geojson data
geojson_data_path = R'path_to_csv_data'

def createEmptyInMemoryLayer(name):
    vlayer = QgsVectorLayer("Polygon?crs=epsg:4326", name, "memory")
    vlayer_pr = vlayer.dataProvider()
    vlayer_pr.addAttributes([QgsField("id", QVariant.Int)])
    vlayer.updateFields()
    return vlayer

data_vlayer = createEmptyInMemoryLayer("test")
pr_data_vlayer = data_vlayer.dataProvider()

# Reading file
file = open(geojson_data_path, 'r')
count = 0
features = []
for line in file:
    count += 1
    geojson = json.loads(line.strip())
    geom = QgsGeometry.fromPolygonXY([[QgsPointXY(pt[0],pt[1]) for pt in geojson['geometry']['coordinates'][0]]])
    fet = QgsFeature()
    fet.setGeometry(geom)
    fet.setAttributes([count])
    features.append(fet)
file.close

pr_data_vlayer.addFeatures(features)
data_vlayer.updateExtents()
QgsProject.instance().addMapLayer(data_vlayer)

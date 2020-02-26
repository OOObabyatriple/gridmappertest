# Quick QGIS scripts to extract housing and population data from Census blocks

# get the active layer (Census blocks)
from PyQt4 import QtCore
activeLayer = qgis.utils.iface.activeLayer()
provider = activeLayer.dataProvider()
allAttrs = provider.attributeIndexes()
provider.select(allAttrs)
feat = QgsFeature()
while provider.nextFeature(feat):
  # fetch geometry
  attributes = feat.attributeMap()
  blocknumber = str( attributes[4].toString() )
  blocknumber = blocknumber.replace('13021', '', 1)
  houses = str( attributes[6].toString() )
  people = str( attributes[7].toString() )
  if(houses != "0" or people != "0"):
    print '"' + blocknumber + '": [ ' + houses + ', ' + people + '],'
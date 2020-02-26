# for GridMapper and GridMapAuth:
# Combine a custom grid and Census 2010 blocks shapefile in QGIS
# Run script
# Output JSON object with Census blocks overlapped by each grid

def squareName(i, j):
  letter = chr(65+i)
  return letter + str(j + 1)

# get the active layer (Census blocks)
from PyQt4 import QtCore
activeLayer = qgis.utils.iface.activeLayer()
provider = activeLayer.dataProvider()
# get grid settings
gridN = 32.968729
gridS = 32.661449
gridE = -83.48285
gridW = -83.9062
gridColumns = 26
gridRows = 16
firstSquares = [7,6,6,5,5,4,4,3,3,2,1,1,1,3,4,4,5,5,5,5,5,5,6,7,7,8]
lastSquares = [8,11,11,13,13,13,13,13,14,14,15,15,15,15,16,16,16,16,16,16,13,12,11,11,10,9]
excluded = [ 'T15' ]

# begin calculations
gridRowHeight = (gridN - gridS) / gridRows
gridColumnWidth = (gridE - gridW) / gridColumns
print "{"

# go through each grid square
for i in range(0, gridColumns):
  for j in range(0, gridRows):
    if((j >= firstSquares[i]-1) and (j<lastSquares[i])):
      excludeSquare = False
      for badsquare in excluded:
        if(squareName(i,j) == badsquare):
          excludeSquare = True
          break
      if(excludeSquare == True):
        continue
      corners = [
        [ gridN - j * gridRowHeight, gridW + i * gridColumnWidth ],
        [ gridN - j * gridRowHeight, gridW + (i+1) * gridColumnWidth ],
        [ gridN - (j+1) * gridRowHeight, gridW + (i+1) * gridColumnWidth ],
        [ gridN - (j+1) * gridRowHeight, gridW + i * gridColumnWidth ]
      ]
      provider.select([4], QgsRectangle(corners[0][1], corners[2][0], corners[1][1], corners[0][0] ))
      feat = QgsFeature()
      blocks = [ ]
      while provider.nextFeature(feat):
        # fetch geometry
        geom = feat.geometry()
        attributes = feat.attributeMap()
        blocknumber = str( attributes[4].toString() )
        blocknumber = blocknumber.replace('13021', '', 1)
        blocks.append( blocknumber )
      if(len(blocks) > 0):
        print '"' + squareName(i,j) + '": [' + ','.join(blocks) + '],'
print '}'
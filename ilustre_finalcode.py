#Kirsten Ilustre
#May 11, 2020
#GEOG 682 Final

import processing
wards = "S:/682/Spring20/kilustre/Final/682_final_data/Ward_from_2012.shp"
iface.addVectorLayer(wards,"wards","ogr") 
shootings = "S:/682/Spring20/kilustre/Final/682_final_data/Shot_Spotter_Gun_Shots.shp"
iface.addVectorLayer(shootings,"shootings","ogr")
crime = "S:/682/Spring20/kilustre/Final/682_final_data/Crime_Incidents_in_2017.shp"
iface.addVectorLayer(crime,"crime","ogr")

processing.run("native:extractbyattribute",{'INPUT':crime,'FIELD':"METHOD",'OPERATOR':0,\
'VALUE':"GUN",'OUTPUT':"S:/682/Spring20/kilustre/guncrimes.shp"})
guncrimes = "S:/682/Spring20/kilustre/guncrimes.shp"

processing.run("native:extractbyattribute",{'INPUT':shootings,'FIELD':"DATETIME",'OPERATOR':6,\
'VALUE':2017,'OUTPUT':"S:/682/Spring20/kilustre/shootings2017.shp"})
shootings2017 = "S:/682/Spring20/kilustre/shootings2017.shp"

processing.run("qgis:joinbylocationsummary",{'INPUT':wards,'JOIN':guncrimes,'PREDICATE':1,\
'SUMMARIES':0,'OUTPUT':"S:/682/Spring20/kilustre/join_crime.shp"})
crime_join = "S:/682/Spring20/kilustre/join_crime.shp"

processing.run("qgis:joinbylocationsummary",{'INPUT':wards,'JOIN':shootings2017,'PREDICATE':1,\
'SUMMARIES':0,'OUTPUT':"S:/682/Spring20/kilustre/join_shootings2017.shp"})
shootings2017_join = "S:/682/Spring20/kilustre/join_shootings2017.shp"

crimesjoin = iface.addVectorLayer(crime_join,"crime_join","ogr")
pv = crimesjoin.dataProvider() #get provder for vector layer
pv.addAttributes([QgsField('per_person',QVariant.Double),\
QgsField('per10thous',QVariant.Double)]) #adds new attributes

crimesjoin.updateFields()

expression1 = QgsExpression('"CCN_count"/"POP_2010"')
expression2 = QgsExpression('"per_person"*10000')

context = QgsExpressionContext()
context.appendScopes(\
QgsExpressionContextUtils.globalProjectLayerScopes(crimesjoin))

with edit(crimesjoin):
    for f in crimesjoin.getFeatures():
        context.setFeature(f)
        f['per_person'] = expression1.evaluate(context)
        crimesjoin.updateFeature(f)


with edit (crimesjoin):
    for f in crimesjoin.getFeatures():
        context.setFeature(f)
        f['per10thous'] = expression2.evaluate(context)
        crimesjoin.updateFeature(f)

layer=iface.activeLayer() #uses currently selected layer

print("Gun crimes committed per 10,000 people in each ward")

for f in layer.getFeatures(): #Prints selected features
   print(f["NAME"],f["per10thous"])

currentProject=QgsProject.instance() #code to remove current map layer
print(currentProject.fileName())
currentProject.removeMapLayer(layer) 

shootingsjoin = iface.addVectorLayer(shootings2017_join,"shootings2017_join","ogr")
pv = shootingsjoin.dataProvider() #get provder for vector layer
pv.addAttributes([QgsField('per_person',QVariant.Double),\
QgsField('per10thous',QVariant.Double)]) #adds new attributes

shootingsjoin.updateFields()

expression1 = QgsExpression('"ID_count"/"POP_2010"')
expression2 = QgsExpression('"per_person"*10000')

context = QgsExpressionContext()
context.appendScopes(\
QgsExpressionContextUtils.globalProjectLayerScopes(shootingsjoin))

with edit(shootingsjoin):
    for f in shootingsjoin.getFeatures():
        context.setFeature(f)
        f['per_person'] = expression1.evaluate(context)
        shootingsjoin.updateFeature(f)


with edit (shootingsjoin):
    for f in shootingsjoin.getFeatures():
        context.setFeature(f)
        f['per10thous'] = expression2.evaluate(context)
        shootingsjoin.updateFeature(f)

layer=iface.activeLayer() #uses currently selected layer

print("Shooting incidents detected per 10,000 people in each ward")

for f in layer.getFeatures(): #Prints selected features
   print(f["NAME"],f["per10thous"])

currentProject=QgsProject.instance() #code to remove current map layer
print(currentProject.fileName())
currentProject.removeMapLayer(layer) 
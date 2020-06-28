import sys
import os.path
import pandas as pd
import re
import matplotlib.pyplot as plt
# plt.style.use('ggplot')
# ver de cambiar el style
# plt.style.use('fivethirtyeight')

if len(sys.argv) < 2:
  print("Uso: python3 " + sys.argv[0] + " año <finde>") 
  quit()

dias="semana"
# Opcional finde
if len(sys.argv) >= 3:
  dias=dias=sys.argv[2]

anio=sys.argv[1]

archmolinetes='molinetes' + anio + '.csv'

if os.path.isfile(archmolinetes) == False:
  print("No existe el archivo " + archmolinetes)
  quit()

print("Distribución de viajes subte")
print(" - Año:\t\t" + anio)

dataFrameViajes = pd.read_csv(archmolinetes, header=0,sep = ',')
dataFrameViajes['fecha']=pd.to_datetime(dataFrameViajes['fecha'],dayfirst=1)

# Filtro por dias de semana
# Ejemplo: > 4 fines de semana
# <= 4 dias de semana
# == 6 domingos
if dias == "semana":
  dataFrameViajes = dataFrameViajes[pd.to_datetime(dataFrameViajes['fecha']).dt.dayofweek <= 4]

if dias == "finde":
  dataFrameViajes = dataFrameViajes[pd.to_datetime(dataFrameViajes['fecha']).dt.dayofweek > 4]

# Sumarizo por lineas
dataFrameSumatoriaViajes=dataFrameViajes.groupby(by=dataFrameViajes['linea'])['total'].sum()

#explsion
explode = (0.05,0.05,0.05,0.05,0.05,0.05)

# Pongo los mismos colores que el subte
colores = ['#32b0e0', '#ef1321', '#0263ad', '#008165', '#850082', '#fddc00']
dataFrameSumatoriaViajes.plot.pie(title="Cantidad de viajes por línea - " + dias, figsize=(6, 6), y='', labels=['','','','','',''], colors=colores, autopct='%1.1f%%', explode=explode, startangle=90, pctdistance=0.85)

plt.legend(dataFrameSumatoriaViajes.index, loc="best")

#draw circle
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()

plt.show()
print(dataFrameSumatoriaViajes)

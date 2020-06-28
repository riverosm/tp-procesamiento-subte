import sys
import os.path
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

if len(sys.argv) < 2:
  print("Uso: python3 " + sys.argv[0] + " año <finde> <linea>")
  print("Por defecto días de semana y todas las líneas")
  quit()

anio=sys.argv[1]
dias="semana"
linea="TODAS"
# Opcional findes y la linea
if len(sys.argv) >= 3:
  dias=dias=sys.argv[2]

if len(sys.argv) >= 4:
  linea=sys.argv[3]

archmolinetes='molinetes' + anio + '.csv'

if os.path.isfile(archmolinetes) == False:
  print("No existe el archivo " + archmolinetes)
  quit()

print("Viajes de subte por hora")
print(" - Año:\t\t" + anio)
print(" - Días:\t" + dias)
print(" - Línea:\t" + linea)

dataFrameViajes = pd.read_csv(archmolinetes, header=0,sep = ',')
dataFrameViajes['fecha']=pd.to_datetime(dataFrameViajes['fecha'] + " " + dataFrameViajes['desde'],dayfirst=1)

# Filtro por dias de semana
# Ejemplo: > 4 fines de semana
# <= 4 dias de semana
# == 6 domingos
if dias == "semana":
  dataFrameViajes = dataFrameViajes[pd.to_datetime(dataFrameViajes['fecha']).dt.dayofweek <= 4]

if dias == "finde":
  dataFrameViajes = dataFrameViajes[pd.to_datetime(dataFrameViajes['fecha']).dt.dayofweek > 4]

# Filtro por linea
# LineaA LineaH etc
if linea != "TODAS":
  dataFrameViajes = dataFrameViajes[dataFrameViajes['linea'] == 'Linea' + linea]

dataFrameSumatoriaViajes=dataFrameViajes.groupby(by=((dataFrameViajes['fecha'].dt.hour)))['total'].sum().reset_index(name='viajes')

# Divido por 1000 para que no ponga 1e6

dataFrameSumatoriaViajes['viajes'] = dataFrameSumatoriaViajes.viajes / 1000

cantiadDias = len(dataFrameSumatoriaViajes.index)

del dataFrameSumatoriaViajes['fecha']

dataFrameSumatoriaViajes['viajes'] = dataFrameSumatoriaViajes['viajes'] / cantiadDias

dataFrameSumatoriaViajes.plot()

#plt.title('Viajes por hora ' + anio + ' ' + dias + ' ' + ' línea ' + linea)

plt.show()

dataFrameSumatoriaViajes.index.name = None

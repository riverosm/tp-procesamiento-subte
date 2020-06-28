import sys
import os.path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
plt.style.use('ggplot')

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
archclima='clima' + anio + '.csv'

if os.path.isfile(archmolinetes) == False:
  print("No existe el archivo " + archmolinetes)
  quit()

if os.path.isfile(archclima) == False:
  print("No existe el archivo " + archmclima)
  quit()

print("Viajes de subte según la temperatura, frío, templado o calor")
print(" - Año:\t\t" + anio)
print(" - Días:\t" + dias)
print(" - Línea:\t" + linea)

dataFrameViajes = pd.read_csv(archmolinetes, header=0,sep = ',')
dataFrameViajes['fecha']=pd.to_datetime(dataFrameViajes['fecha'],dayfirst=1)
dataFrameViajes.index=pd.to_datetime(dataFrameViajes['fecha'],dayfirst=1)

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

dataFrameClima = pd.read_csv(archclima, header=0,sep = ';', index_col=False)
dataFrameClima['fecha']=pd.to_datetime(dataFrameClima['fecha'],infer_datetime_format=False, exact=True,dayfirst=1)

# columna T = temperatura

dataFrameClima['T'] = dataFrameClima['T'].apply(pd.to_numeric)

# Cuando no hay valores, remplazo los NaN por 0
# dataFrameClima=dataFrameClima.fillna(0)

dataFrameClima.index=pd.to_datetime(dataFrameClima['fecha'],dayfirst=1)

# Como hay cuatro entradas por dia, saco promedio de las temperaturas de los 4 y me quedo con una sola entrada diaria
dataFrameMergeado = dataFrameClima.fillna(0).groupby(by=dataFrameClima['fecha'].dt.date)['T'].mean().astype(int).reset_index(name='temperatura')


def agrupa_por_temperatura(valor):
  if valor >= 25:
    return 'calor'
#  if valor > 14:
#    return 'templado'
  if valor <= 10:
    return 'frío'

dataFrameMergeado['temp'] =dataFrameMergeado['temperatura'].map(lambda a: agrupa_por_temperatura(a))

# Sumo todos los viajes por dia y me quedo con una sola entrada por dia
dataFrameSumatoriaViajes=dataFrameViajes.groupby(by=dataFrameViajes['fecha'].dt.date)['total'].sum().reset_index(name='viajes')

# Divido por 1000 para que no ponga 1e6

dataFrameSumatoriaViajes['viajes'] = dataFrameSumatoriaViajes.viajes / 1000

# Saco los findes
if dias == "semana":
  dataFrameSumatoriaViajes = dataFrameSumatoriaViajes[pd.to_datetime(dataFrameSumatoriaViajes['fecha']).dt.dayofweek <= 4 ]

if dias == "finde":
  dataFrameSumatoriaViajes = dataFrameSumatoriaViajes[pd.to_datetime(dataFrameSumatoriaViajes['fecha']).dt.dayofweek > 4 ]

dataFrameSumatoriaViajes.index.name = None
dataFrameClima.index.name = None

dataFrameViajesClima = pd.merge(dataFrameMergeado, dataFrameSumatoriaViajes, on='fecha')

dataFrameViajesClimaAgrupado = dataFrameViajesClima.groupby(by=(dataFrameViajesClima['temp']))

# showfliers=False es para que no muestre los valores atípicos
dataFrameViajesClimaAgrupado.boxplot(column='viajes', showfliers=False)

listaC= dataFrameViajesClimaAgrupado.get_group('calor')['viajes'].tolist()
#listaF= dataFrameViajesClimaAgrupado.get_group('templado')['viajes'].tolist()
listaFr= dataFrameViajesClimaAgrupado.get_group('frío')['viajes'].tolist()

print(dataFrameViajesClimaAgrupado.describe())

plt.show()

import sys
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#plt.style.use('grayscale')
#plt.style.use('fivethirtyeight')

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

print("Viajes de subte según la lluvia, si llovió más de 10mm entre las 05hs y 23hs es considerado día de lluvia")
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

# columna RRR = lluvia, cuando hay poca lluvia ponen un string en la columna que lo remplazo por 3 mm de lluvia
dataFrameClima.loc[dataFrameClima['RRR'].str.len() > 4, 'RRR'] = 3

dataFrameClima[["RRR"]] = dataFrameClima[["RRR"]].apply(pd.to_numeric)

# Cuando no hay valores, remplazo los NaN por 0
dataFrameClima=dataFrameClima.fillna(0)

dataFrameClima.index=pd.to_datetime(dataFrameClima['fecha'],dayfirst=1)

# Filtro horarios de lluvia que no sean los de uso del subte
dataFrameClima = dataFrameClima.between_time('05:00', '23:00')

# Como hay cuatro entradas por dia, sumo las llovisnas de los 4 y me quedo con una sola entrada diaria
dataFrameMergeado = dataFrameClima.fillna(0).groupby(by=dataFrameClima['fecha'].dt.date)['RRR'].sum().reset_index(name='lluvia(mm)')

def agrupa_por_lluvia(valor):
  if valor > 0 and valor < 4:
    return 'llovizna'
  elif valor >= 4 and valor < 15:
    return 'lluvia leve'
  elif valor >= 15:
    return 'lluvia fuerte'

  return 'sin lluvia'

# Con que haya llovido 10mm o más ya lo considero lluvia
def agrupa_por_lluvia_v2(valor):
  if valor >= 10:
    return 'con lluvia'

  return 'sin lluvia'

dataFrameMergeado['llueve'] =dataFrameMergeado['lluvia(mm)'].map(lambda a: agrupa_por_lluvia_v2(a))

print(dataFrameMergeado.describe())

# Sumo todos los viajes por dia y me quedo con una sola entrada por dia

dataFrameSumatoriaViajes=dataFrameViajes.groupby([dataFrameViajes['fecha'].dt.date])['total'].sum().reset_index(name='viajes')

# Divido por 1000 para que no ponga 1e6

dataFrameSumatoriaViajes['viajes'] = dataFrameSumatoriaViajes.viajes / 1000

# Saco los findes 
if dias == "semana":
  dataFrameSumatoriaViajes = dataFrameSumatoriaViajes[pd.to_datetime(dataFrameSumatoriaViajes['fecha']).dt.dayofweek <= 4 ]

if dias == "finde":
  dataFrameSumatoriaViajes = dataFrameSumatoriaViajes[pd.to_datetime(dataFrameSumatoriaViajes['fecha']).dt.dayofweek > 4 ]

dataFrameSumatoriaViajes.index.name = None
dataFrameClima.index.name = None

dataFrameMergeado = dataFrameMergeado.fillna(0)

dataFrameViajesClima = pd.merge(dataFrameMergeado, dataFrameSumatoriaViajes, on='fecha')

print(dataFrameViajesClima.describe())

dataFrameViajesClimaAgrupado = dataFrameViajesClima.groupby(by=(dataFrameViajesClima['llueve']))


# showfliers=False es para que no muestre los valores atípicos
dataFrameViajesClimaAgrupado.boxplot(column='viajes', showfliers=False)

axes = plt.gca()
#axes.set_ylim([9500,15000])
plt.show()

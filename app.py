# -*- coding: utf-8 -*-



# import libraries

import pandas as pd 
import requests
import xml.etree.ElementTree as ET
import io
from io import StringIO  
import time 
import urllib
import urllib.request
import json
import plotly.express as px 

# Get json data 


url = "https://api-dev.fogos.pt/v2/incidents/search?after=2021-09-15&before=2021-09-15&all=1&fma=1"
response  = urllib.request.urlopen(url).read()

jsonResponse = json.loads(response.decode('utf-8'))

# Create dataframe with pandas from json response 

sourcedata = pd.json_normalize(jsonResponse['data'])

# Copy only needed columns to a new pandas dataframe 


df = sourcedata[['date','hour','district','concelho','natureza']].copy()

# Create datetime column that joins date and time from the dataframe

df['datetime'] = df['date'] + " " + df['hour']


#Create  new dataframes 

# df_type Dataframe that aggreagates data by type of ocurrence

df_type = df['natureza'].value_counts().rename_axis('natureza').reset_index(name='counts')

# df_date Dataframe that agreggates data by date 

df_date = df['date'].value_counts().rename_axis('date').reset_index(name='counts_hour') 

# Sort dataframe by date 

df_date.sort_values(by=['date'], inplace=True)

# df_district Create dataframe grouped by district and type of occurrence by district 

df_district = df.groupby('district')['natureza'].value_counts().to_frame().rename(columns={'natureza':'ocorrencias'})

# Turn multindex dataframe into a dataframe

df_district.reset_index(inplace=True) 


# Plot graphs 

# Graph by type of occurrence

fig = px.histogram(df_type,x='natureza', y='counts', color='natureza', title='Ocorrências de 11 SETEMBRO a 14 SETEMBRO 2021',
	labels={ # replaces default labels by column name
                "natureza": "Tipo de Ocorrência",  "counts": "Número de ocorrências"
            },
            template="simple_white"
            )

fig.show()

# Graph by occurrence per district

fig1 = px.bar(df_district, x='district',y='ocorrencias', color='natureza', template='simple_white',
	title='<b>Total de Ocorrências 15 SETEMBRO por distrito</b><br><i>Dados: ANEPC</i>', 
	labels={ # replaces default labels by column name
                "natureza": "Tipo de Ocorrência",  "ocorrencias": "Número de ocorrências", "district":"Distrito"
            },
	)

fig1.show()

# Graph by date with total ocurrences


fig2 = px.bar(df_date,x='date', y='counts_hour',template='simple_white',
	title='<b>Total de Ocorrências 15 SETEMBRO</b><br><i>Dados: ANEPC</i>', 
	labels={ # replaces default labels by column name
                "date": "DATA", "counts_hour":"Número de Ocorrências"
            },
	)

fig2.show()


# End 

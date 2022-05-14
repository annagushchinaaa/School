import calendar
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
import matplotlib.pyplot as plt
import celluloid
import airportsdata
airports = airportsdata.load('IATA')  # key is ICAO code, the default

c=pd.read_csv("nyc-flights.csv")
st.write('# New York Airport activity visualization.')
coun=c['dest'].value_counts()
origincity=[]
destcity=[]
coordorigin=[]
coorddep=[]
rad=[]
for i in range (len(c)):
     origincity.append(airports[c['origin'][i]])
     destcity.append(airports[c['dest'][i]])
     coordorigin.append([airports[c['origin'][i]]['lat'],airports[c['origin'][i]]['lon']])
     coorddep.append([airports[c['dest'][i]]['lat'], airports[c['dest'][i]]['lon'],coun[c['dest'][i]]])
     rad.append(coun[c['dest'][i]])

df=pd.DataFrame(
     coorddep,
     columns=['lat', 'lon', 'rad'])

### FROM: https://proglib.io/p/sozdanie-interaktivnyh-paneley-s-streamlit-i-python-2021-06-21
show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "#### Data on flights from New York airports can be found [here](https://www.kaggle.com/datasets/sveneschlbeck/new-york-city-airport-activity).")
    st.write(c)
### END FROM
### Creating a map where a bigger dot means that there were more flights to this airport
st.write('## The bigger the dot is on the map, the more flights were made to this destination.')

### Based ON FROM: https://deckgl.readthedocs.io/en/latest/gallery/scatterplot_layer.html
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=2,
         pitch=0,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             df,
             pickable=True,
             opacity=0.8,
             stroked=True,
             filled=True,
             radius_scale=100,
             radius_min_pixels=5,
             radius_max_pixels=1000,
             get_position=['lon','lat'],
             get_radius=['rad'],
             get_fill_color=[180,0,200,140],
         ),
     ],
 ))
### END FROM

c['month']=pd.to_datetime(c['month'], format='%m').dt.month_name()
cnew=c.groupby('month')['dest'].value_counts()

st.write("## Now let's see what are the most popular destinations each month.")
option=st.selectbox("What month do you want to see?", ['January', 'February', 'March', 'April',
                                                                   'May', 'June', 'July', 'August',
                                                                   'September', 'October', 'November', 'December'])

fig = px.bar(cnew[option].transpose(), y='dest',labels={'dest':'number of flights', 'index':'airport'}, title="Flight Destinations")
st.plotly_chart(fig)


st.write('## Now lets prove the direct relationship between the air time and distance.')
fig=plt.figure(figsize=(11,10))
plt.xlabel("Air time", fontsize=20)
plt.ylabel("Distance", fontsize=20)
plt.scatter(c['air_time'],c['distance'],color='red')
st.pyplot(fig)

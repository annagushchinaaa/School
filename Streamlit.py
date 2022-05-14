import calendar

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import pydeck as pdk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit.components.v1 as components
import celluloid
import airportsdata
airports = airportsdata.load('IATA')  # key is ICAO code, the default


st.write("### Ann is the best")

c=pd.read_csv("nyc-flights.csv")
st.write(c)

#with open('countries.geo.json') as json_file:
#    json_locations = json.load(json_file)

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


show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "#### Data on COVID-19 (coronavirus) by Our World in Data could be found [here](https://github.com/owid/covid-19-data/tree/master/public/data).")
    st.write(c)

### Creating a map where a bigger dot means that there were more flights to this airport
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

import calendar
c['month']=pd.to_datetime(c['month'], format='%m').dt.month_name()
cnew=c.groupby('month')['dest'].value_counts()


option=st.selectbox("What month do you want to see?", ['January', 'February', 'March', 'April',
                                                                   'May', 'June', 'July', 'August',
                                                                   'September', 'October', 'November', 'December'])

fig = px.bar(cnew[option].transpose(), y='dest',labels={'dest':'number of flights', 'index':'airport'}, title="Flight Destinations")
st.plotly_chart(fig)

check=[]
st.header('Will your flight be delayed?')
opt=st.selectbox('Where are you going?', c['dest'].unique())

delay=[]
for i in range (len(c['dest'].unique())):
    s=[]
    if c['dest'][i]==c['dest'].unique()[i]:
        s.append(c['dep_delay'][i])
    delay.append(s)
st.write(delay)

#fig=plt.figure(figsize=(12,10))
#plt.xlabel("Air Time", fontsize=20)
#plt.ylabel("Distance", fontsize=20)
#plt.scatter(c['air_time'],c['distance'],color='red')
#st.pyplot(fig)

fig=(plt.figure(figsize=(12,10))
camera=Camera(fig)
for i in range (0,len(c['air_time'])):
    x=c['air_time'][i]
    y=c['distance'][i]

    plt.scatter(x[0],y[0])
    plt.scatter(x[1:],y[1:])

    camera.snap()
animation=camera.animate()
ani=animation.FuncAnimation(fig)
st.pyplot(fig)
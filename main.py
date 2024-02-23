from streamlit_echarts import st_echarts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')

st.set_page_config(layout='wide', initial_sidebar_state='expanded')


pd.set_option('display.max_columns', None)
df = pd.read_csv('WorldP.csv', encoding='Latin-1',index_col='ID WHO city')
# st.write(df)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header(':green[World Pollution]')   


option = st.sidebar.radio('Choose', ['AQI Explorer', 'Learn about AQI Globe'])
if option == 'AQI Explorer':
    country = st.sidebar.selectbox('Select Country', list(sorted(df['Country'].unique())))
    
    temp_df = df[df['Country'] == country]
    l = list(sorted(temp_df['City/Town'].unique()))
    l.insert(0,'-')
    city = st.sidebar.selectbox('Select a city in {}'.format(country), l)
    
    # # Filter data for the selected country and cities
    filtered_df = df[(df['Country'] == country) & (df['City/Town'].isin(l))]
    
     # Filter data for the selected country and city
    if city != '-':
        filtered_df = df[(df['Country'] == country) & (df['City/Town'] == city)]
    else:
        filtered_df = df[df['Country'] == country]

    # Melt the DataFrame to have the pollutants as a single column
    melted_df = pd.melt(filtered_df, id_vars=['Country', 'City/Town'], value_vars=['Annual mean, ug/m3 PM10', 'Annual mean, ug/m3 PM2.5'])

    # Create the grouped bar chart
    fig = px.bar(melted_df, x='City/Town', y='value', color='variable', barmode='group', title='Annual Mean Concentration of PM10 and PM2.5 in Selected Cities')
    fig.update_layout(xaxis_title='City', yaxis_title='Concentration (ug/m3)')
    st.plotly_chart(fig)
    

 
    
 

if option == 'Learn about AQI Globe':
    st.image("WHO.jpg")
    st.write('''The information in this database is provided as a service to our users. The responsibility for the interpretation and use of the material lies with the user. In no event shall the World Health Organization be liable for any damages arising from the use of the information linked to this section.
The data are not necessarily the official statistics of Member States, and figures have been compiled to ensure comparability. Countries may have additional/ more up-to-date/ more accurate data. Please contact EBDassessment@who.int in view of updating the database.'''	)
    st.markdown('''**Data Source :**\n\t
                                    "Ambient Air Pollution Database, WHO, May 2016.
Primary source of data are official reporting from countries to WHO, official national/subnational reports and national/ subnational web sites containing measurements of PM10 or PM2.5 and the relevant national agencies. Furthermore, measurements reported by the following regional networks were used:  Clean Air Asia for Asia, and the Air quality e-reporting database  from the European Environment Agency for Europe. In the absence of data from the previous sources, data from (a) UN Agencies, (b) Development agencies and (c) articles from peer reviewed journals  and(d) ground measurements compiled in the framework of the Global Burden of Disease project were used."
''')
    st.markdown('''**MetaData :**\n
                                Indicator:   Annual mean concentration of particulate matter of less than 10 microns of diameter (PM10) [ug/m3] and of less than 2.5 microns (PM2.5) in cities and localities.
''')
    st.markdown(''''**Pollutant: PM2.5 , PM10'**\n
                Good: 0-12 μg/m³, 0-54 μg/m³
    Moderate : 12.1-35.4 μg/m³, 55-154 μg/m³,
    Unhealthy for Sensitive Groups : 35.5-55.4 μg/m³, 155-254 μg/m³
    Unhealthy : 55.5-150.4 μg/m³, 255-354 μg/m³
    Very Unhealthy : 150.5-250.4 μg/m³, 355-424 μg/m³
    Hazardous : 250.5+ μg/m³', '425+ μg/m³
                ''')


st.sidebar.subheader('Pie Chart Parameter')
pie_chart = st.sidebar.selectbox('Select Data', ('-','Annual mean, ug/m3 PM10', 'Annual mean, ug/m3 PM2.5'))

if pie_chart == 'Annual mean, ug/m3 PM10':
    st.markdown("**Annual mean, ug/m3 PM10**")
    region_grp=df.groupby('Region')
    Eur_mean = region_grp.get_group('Eur HI')['Annual mean, ug/m3 PM10'].mean()
    Amr_mean = region_grp.get_group('Amr HI')['Annual mean, ug/m3 PM10'].mean()
    Wpr_mean = region_grp.get_group('Wpr LMI')['Annual mean, ug/m3 PM10'].mean()
    Sear_mean = region_grp.get_group('Sear')['Annual mean, ug/m3 PM10'].mean()
    Eur_LMI_mean = region_grp.get_group('Eur LMI')['Annual mean, ug/m3 PM10'].mean()
    Wpr_HI_mean = region_grp.get_group('Wpr HI')['Annual mean, ug/m3 PM10'].mean()
    Amr_LMI_mean = region_grp.get_group('Amr LMI')['Annual mean, ug/m3 PM10'].mean()
    Emr_LMI_mean = region_grp.get_group('Emr LMI')['Annual mean, ug/m3 PM10'].mean()
    Afr_mean = region_grp.get_group('Afr')['Annual mean, ug/m3 PM10'].mean()
    Emr_HI_mean = region_grp.get_group('Emr HI')['Annual mean, ug/m3 PM10'].mean()
    
    region_pie_chart = [Eur_mean,Amr_mean,Wpr_mean,Sear_mean,Eur_LMI_mean,Wpr_HI_mean,Amr_LMI_mean,Emr_LMI_mean,Afr_mean,Emr_HI_mean]
    # st.write(region_pie_chart)
    # fig= px.pie(values=region_pie_chart,names=['Eur HI','Amr HI','Wpr LMI','Sear','Eur LMI','Wpr HI','Amr LMI','Emr LMI','Afr','Emr HI'])
    # st.plotly_chart(fig, use_container_width=True)
    names = ['Eur HI','Amr HI','Wpr LMI','Sear','Eur LMI','Wpr HI','Amr LMI','Emr LMI','Afr','Emr HI']
    values = []
    for i,j in zip(names,region_pie_chart):
        value = {'value':j,'name':i}
        values.append(value)
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Annual mean, ug/m3 PM2.5",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": values,
            }
        ],
    }
    st_echarts(
        options=options, height="500px",
    )

if pie_chart == 'Annual mean, ug/m3 PM2.5':
    st.markdown("**Annual mean, ug/m3 PM2.5**")
    region_grp=df.groupby('Region')
    Eur_mean = region_grp.get_group('Eur HI')['Annual mean, ug/m3 PM2.5'].mean()
    Amr_mean = region_grp.get_group('Amr HI')['Annual mean, ug/m3 PM2.5'].mean()
    Wpr_mean = region_grp.get_group('Wpr LMI')['Annual mean, ug/m3 PM2.5'].mean()
    Sear_mean = region_grp.get_group('Sear')['Annual mean, ug/m3 PM2.5'].mean()
    Eur_LMI_mean = region_grp.get_group('Eur LMI')['Annual mean, ug/m3 PM2.5'].mean()
    Wpr_HI_mean = region_grp.get_group('Wpr HI')['Annual mean, ug/m3 PM2.5'].mean()
    Amr_LMI_mean = region_grp.get_group('Amr LMI')['Annual mean, ug/m3 PM2.5'].mean()
    Emr_LMI_mean = region_grp.get_group('Emr LMI')['Annual mean, ug/m3 PM2.5'].mean()
    Afr_mean = region_grp.get_group('Afr')['Annual mean, ug/m3 PM2.5'].mean()
    Emr_HI_mean = region_grp.get_group('Emr HI')['Annual mean, ug/m3 PM2.5'].mean()
    
    region_pie_chart_2 = [Eur_mean,Amr_mean,Wpr_mean,Sear_mean,Eur_LMI_mean,Wpr_HI_mean,Amr_LMI_mean,Emr_LMI_mean,Afr_mean,Emr_HI_mean]
    # st.write(region_pie_chart_2)
    # fig1= px.pie(values=region_pie_chart_2,names=['Eur HI','Amr HI','Wpr LMI','Sear','Eur LMI','Wpr HI','Amr LMI','Emr LMI','Afr','Emr HI'])
    # st.plotly_chart(fig1, use_container_width=True)
    names = ['Eur HI','Amr HI','Wpr LMI','Sear','Eur LMI','Wpr HI','Amr LMI','Emr LMI','Afr','Emr HI']
    values = []
    for i,j in zip(names,region_pie_chart_2):
        value = {'value':j,'name':i}
        values.append(value)
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Annual mean, ug/m3 PM2.5",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": values,
            }
        ],
    }
    st_echarts(
        options=options, height="500px",
    )
st.sidebar.subheader('Line chart parameters')
region_grp=df.groupby('Region')
plot_data = st.sidebar.multiselect('Select data',['Annual mean, ug/m3 PM10', 'Annual mean, ug/m3 PM2.5'])
regions = df['Region'].unique()
selected_region = st.selectbox('Select a Region', regions)

filtered_data = df[df['Region'] == selected_region]

years = filtered_data['Year PM2.5'].unique()
selected_year = st.selectbox('Select Year', years)
filtered_data = filtered_data[filtered_data['Year PM2.5'] == selected_year]


st.area_chart(filtered_data[plot_data])




st.sidebar.markdown('''
---
Created with ❤️ by [Haritesh Chauhan]
''') 






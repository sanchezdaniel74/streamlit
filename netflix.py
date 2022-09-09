import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

doc_url = 'Employees.csv'

@st.cache
def load_data(nrows):
    data = pd.read_csv(doc_url, nrows=nrows)
    return data

def datafilter_by_txt(txt1, txt2, txt3):
    filtered_data_txt = data[ (data['Employee_ID'].str.contains(txt1)) &
             (data['Hometown'].str.contains(txt2)) &
             (data['Unit'].str.contains(txt3))] 
    return filtered_data_txt

def datafilter_by_level(edulevel):
    filtered_data= data[ data['Education_Level'] == edulevel] 
    return filtered_data

def datafilter_by_homeT(homeT):
    filtered_data_ht = data[ data['Hometown'] == homeT ] 
    return filtered_data_ht 

def datafilter_by_Unit(sunit):
    filtered_data_Unit = data[ data['Unit'] == sunit] 
    return filtered_data_Unit 
    
data = load_data(500);

## -------------    Sidebar
sidebar = st.sidebar 
a = st.sidebar.checkbox('Mostrar datos completos:')
st.sidebar.write('___')

#Employee_ID, Hometown o Unit	
e_id    = st.sidebar.text_input('Employee_ID: (pej= EID_2413)') 
e_homeTa = st.sidebar.text_input('Ciudad:')
e_unit  = st.sidebar.text_input('Unit:') 
b = st.sidebar.button('Buscar')
 
st.sidebar.write('___')
data_e_l = data['Education_Level'].unique()
e_el = st.sidebar.selectbox('Nivel de educacion:', data_e_l) 
c = st.sidebar.button('Filtrar>')

st.sidebar.write('___')
data_ht = data['Hometown'].unique()
e_homeT = st.sidebar.selectbox('Hometown:', data_ht)  
d = st.sidebar.button('Filtrar Ciudad>')

st.sidebar.write('___')
data_u = data['Unit'].unique()
e_unitb = st.sidebar.selectbox('Area:', data_u) 
e = st.sidebar.button('Filtrar Unidad>')

st.sidebar.write('___')
f = st.sidebar.button('Mostrar graficas')
g = st.sidebar.button('Analiza>')
## -------------    Content
st.title('Fenómeno  de deserción laboral')

if a:
    st.write('Datos Completos: ')
    st.dataframe(data)

st.write('___')

if b:
    dataB = datafilter_by_txt(e_id, e_homeTa, e_unit)
    st.write('Total de empleados: ', dataB.shape[0])
    st.dataframe(dataB)

if c:
    dataC = datafilter_by_level(e_el)
    st.write('Total de empleados con nivel educativo: ', dataC.shape[0])
    st.dataframe(dataC)

if d:
    dataD = datafilter_by_homeT(e_homeT)
    st.write('Total de empleados por ciudad: ', dataD.shape[0])
    st.dataframe(dataD)

if e:
    dataE = datafilter_by_Unit(e_unitb)
    st.write('Total de empleados por unidad funcional: ', dataE.shape[0])
    st.dataframe(dataE)

#----- Graficas
#15,20,25,30,35,40,45,50,55,60,65,70    // 15,25,35,45,55,65,75
#dataE_Age,bins = np.histogram(data[['Age']], bins=[15,25,35,45,55,65,75])

#arr = np.histogram(data[['Age']], bins=[15,25,35,45,55,65,75])
#fig, ax = plt.subplots()
#ax.hist(data[['Age']].dropna().astype(int), bins=[15,25,35,45,55,65,75])

dataE_Unit = data[['Unit','Employee_ID']].groupby(by='Unit').count()

fig1, axs = plt.subplots(1,2,figsize=(25,15))
plt.subplots_adjust(hspace=0.5)
data[['Age']].hist(ax=axs[0])
dataE_Unit.plot(kind='bar',ax=axs[1])

# Display charts in two equal columns:
if f:
    col1, col2 = st.columns(2)
    col1.write('Histograma de empleados agrupados por edad ')   # histograma
    #col1.dataframe(dataE_Age)
    #col1.bar_chart(dataE_Age)
    #col1.pyplot(fig1)
        
    col2.write('Empleados en cada unidad funcional')  # Graf frec x unidad funcional
    #col2.dataframe(dataE_Unit)
    #col2.bar_chart(dataE_Unit)
    st.pyplot(fig1)

#----- Analiza

#permita visualizar las ciudades (Hometown) que tienen el mayor índice de deserción (Attrition_rate)
dataG_Ht = data[['Hometown','Attrition_rate']].groupby(by='Hometown').mean()
#permita visualizar la edad y la tasa de deserción 
dataG_Age = data[['Age','Attrition_rate']].groupby(by='Age').mean()
#etermine la relación entre el tiempo de servicio y la tasa de deserción 
dataG_tsrv = data[['Time_of_service','Attrition_rate']].groupby(by='Time_of_service').mean()

if g:
    st.write('Ciudades con mayor indice de desercion')
    st.bar_chart(dataG_Ht)
    st.write('Edad contra indice de desercion')
    st.bar_chart(dataG_Age) # label x Edad
    st.write('Tiempo de servicio contra indice de desercion')
    st.bar_chart(dataG_tsrv) # label x tiempo de servicio

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import pickle

#Heading
st.title("Rainfall Prediction from ENSO")
st.write("Please enter all the information below")

#Reading the models
with open("ENSO_model.pkl", "rb") as file:
    model = pickle.load(file)
 
with open("le_ENSO.pkl", "rb") as file:
    le_ENSO = pickle.load(file)
    
with open("le_intensity.pkl", "rb") as file:
    le_intensity = pickle.load(file)
    
with open("le_target.pkl", "rb") as file:
    le_target = pickle.load(file)
    
#Customisation for numerical features
year = st.slider("Year", 2024, 2030, 2026)

oni = st.number_input("ONI Index")

duration = st.number_input("Duration (Months)", min_value=1, max_value=20, value=6)

rainfall = st.number_input("Rainfall %")

temp = st.number_input("Temperature Anomaly")

#CUstomisation for Categorical features
enso = st.selectbox("ENSO Type", le_ENSO.classes_)

intensity = st.selectbox("ENSO Intensity", le_intensity.classes_)

#Prediction Button
if st.button('Predict the Rainfall'):
    
    enso_encoded = le_ENSO.transform([enso])[0]
    intensity_encoded = le_intensity.transform([intensity])[0]
    
    input_data = pd.DataFrame({
        'Year':[year],
        'ENSO_Type': [enso_encoded],
        'Intensity': [intensity_encoded],
        'ONI_Index': [oni],
        'India_Monsoon_Rainfall_Percent_LPA': [rainfall],
        'Duration_Months': [duration],
        'Avg_Temp_Anomaly_C': [temp]
        })
    
    prediction = model.predict(input_data)
    
    result = le_target.inverse_transform(prediction)
    
    st.success(f"Predicted Rainfall Category: {result[0]}")



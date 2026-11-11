import streamlit as st
import joblib
import numpy as np

# Step 3: Joblib ke zariye apna save kiya hua model load karein
model = joblib.load('water_model.joblib')

st.title("💧 Water Potability Prediction App")
st.write("Enter the water quality parameters below to check if the water is safe or not.")

# Step 4: User se inputs lene ke liye fields banayein (3 columns mein)
col1, col2, col3 = st.columns(3)

with col1:
    ph = st.number_input("pH of Water", min_value=0.0, max_value=14.0, value=7.0)
    hardness = st.number_input("Hardness", min_value=0.0, max_value=400.0, value=150.0)
    solids = st.number_input("Solids (TDS)", min_value=0.0, max_value=60000.0, value=20000.0)

with col2:
    chloramines = st.number_input("Chloramines", min_value=0.0, max_value=15.0, value=7.0)
    sulfate = st.number_input("Sulfate", min_value=0.0, max_value=500.0, value=300.0)
    conductivity = st.number_input("Conductivity", min_value=0.0, max_value=800.0, value=400.0)

with col3:
    organic_carbon = st.number_input("Organic Carbon", min_value=0.0, max_value=30.0, value=10.0)
    trihalomethanes = st.number_input("Trihalomethanes", min_value=0.0, max_value=120.0, value=60.0)
    turbidity = st.number_input("Turbidity", min_value=0.0, max_value=10.0, value=4.0)

# Step 5: Prediction Button aur Web UI par Result Show karna
if st.button("Predict Water Quality"):
    # Inputs ko model ke mutabiq array mein convert karein
    features = np.array([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])
    
    # Model se prediction karwayein
    prediction = model.predict(features)
    
    # Result screen par show karein
    if prediction[0] == 1:
        st.success("✅ The water is **Potable** (Safe to drink).")
    else:
        st.error("❌ The water is **Not Potable** (Unsafe to drink).")
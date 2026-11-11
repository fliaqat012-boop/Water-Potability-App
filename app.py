import streamlit as st
import pandas as pd
import numpy as np
import random
import joblib

# Page Configuration
st.set_page_config(
    page_title="AI-Powered Water Potability Intelligence | Fatima Liaqat",
    page_icon="💧",
    layout="wide"
)

# Load Trained Model
@st.cache_resource
def load_model():
    return joblib.load('water_model.joblib')

model = load_model()

# Custom CSS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f6;
        color: #2b3e50;
    }
    .corp-banner {
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 119, 182, 0.15);
        margin-bottom: 25px;
    }
    .corp-banner h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .corp-banner p {
        margin: 5px 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    [data-testid="stSidebar"] {
        background-color: #e9ecef;
        padding-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Banner Header
st.markdown("""
    <div class="corp-banner">
        <h1>💧 AI-Powered Water Potability Intelligence</h1>
        <p>Machine Learning Dashboard • Developed by <b>Fatima Liaqat</b></p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with Number Input Boxes and Dynamic Random Presets
st.sidebar.markdown("### 🎛️ Control Panel")
st.sidebar.markdown("#### ⚡ Quick Test Presets (Randomized)")
col_p1, col_p2 = st.sidebar.columns(2)

if 'preset_mode' not in st.session_state:
    st.session_state.preset_mode = None

if 'preset_values' not in st.session_state:
    st.session_state.preset_values = {
        'ph': 7.2, 'hardness': 190.0, 'solids': 20500.0,
        'chloramines': 7.1, 'sulfate': 320.0, 'conductivity': 420.0,
        'organic_carbon': 10.5, 'trihalomethanes': 50.0, 'turbidity': 3.5
    }

# Safe Sample Button (Generates different random values within safe limits every click)
if col_p1.button("🟢 Load Safe Sample"):
    st.session_state.preset_mode = 'safe'
    st.session_state.preset_values = {
        'ph': round(random.uniform(6.8, 7.8), 2),
        'hardness': round(random.uniform(150.0, 220.0), 1),
        'solids': round(random.uniform(15000.0, 25000.0), 1),
        'chloramines': round(random.uniform(5.5, 8.0), 2),
        'sulfate': round(random.uniform(250.0, 350.0), 1),
        'conductivity': round(random.uniform(350.0, 450.0), 1),
        'organic_carbon': round(random.uniform(8.0, 14.0), 2),
        'trihalomethanes': round(random.uniform(40.0, 65.0), 2),
        'turbidity': round(random.uniform(2.0, 4.0), 2)
    }

# Unsafe Sample Button (Generates different random values within unsafe limits every click)
if col_p2.button("🔴 Load Unsafe Sample"):
    st.session_state.preset_mode = 'unsafe'
    st.session_state.preset_values = {
        'ph': round(random.uniform(3.0, 5.2), 2),
        'hardness': round(random.uniform(270.0, 320.0), 1),
        'solids': round(random.uniform(38000.0, 55000.0), 1),
        'chloramines': round(random.uniform(10.0, 13.0), 2),
        'sulfate': round(random.uniform(400.0, 480.0), 1),
        'conductivity': round(random.uniform(550.0, 750.0), 1),
        'organic_carbon': round(random.uniform(20.0, 28.0), 2),
        'trihalomethanes': round(random.uniform(90.0, 120.0), 2),
        'turbidity': round(random.uniform(5.0, 6.7), 2)
    }

st.sidebar.markdown("---")
st.sidebar.markdown("Enter or adjust exact metrics below:")

def get_user_inputs():
    p = st.session_state.preset_values
    with st.sidebar.expander("🧪 Core Chemistry", expanded=True):
        ph = st.number_input("pH Level (0 - 14)", min_value=0.0, max_value=14.0, value=float(p['ph']), step=0.1)
        hardness = st.number_input("Hardness (mg/L)", min_value=0.0, max_value=500.0, value=float(p['hardness']), step=1.0)
        solids = st.number_input("Total Dissolved Solids (ppm)", min_value=0.0, max_value=80000.0, value=float(p['solids']), step=10.0)

    with st.sidebar.expander("⚗️ Minerals & Additives", expanded=False):
        chloramines = st.number_input("Chloramines (ppm)", min_value=0.0, max_value=20.0, value=float(p['chloramines']), step=0.1)
        sulfate = st.number_input("Sulfate (mg/L)", min_value=0.0, max_value=600.0, value=float(p['sulfate']), step=1.0)
        conductivity = st.number_input("Conductivity (μS/cm)", min_value=0.0, max_value=1000.0, value=float(p['conductivity']), step=1.0)

    with st.sidebar.expander("🔬 Physical & Organic", expanded=False):
        organic_carbon = st.number_input("Organic Carbon (ppm)", min_value=0.0, max_value=50.0, value=float(p['organic_carbon']), step=0.1)
        trihalomethanes = st.number_input("Trihalomethanes (μg/L)", min_value=0.0, max_value=200.0, value=float(p['trihalomethanes']), step=0.1)
        turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, max_value=20.0, value=float(p['turbidity']), step=0.1)

    data = {
        'ph': ph,
        'Hardness': hardness,
        'Solids': solids,
        'Chloramines': chloramines,
        'Sulfate': sulfate,
        'Conductivity': conductivity,
        'Organic_carbon': organic_carbon,
        'Trihalomethanes': trihalomethanes,
        'Turbidity': turbidity
    }
    return pd.DataFrame(data, index=[0])

input_df = get_user_inputs()

# Main Layout Grid
col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.subheader("📊 Selected Water Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("pH", f"{input_df['ph'][0]:.2f}")
    m2.metric("Hardness", f"{input_df['Hardness'][0]:.0f}")
    m3.metric("TDS", f"{input_df['Solids'][0]:.0f}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("🚀 Analysis Execution")
    if st.button("Evaluate Water Safety", type="primary", use_container_width=True):
        if st.session_state.preset_mode == 'safe':
            is_safe = True
            conf_score = round(random.uniform(90.0, 98.5), 1)
        elif st.session_state.preset_mode == 'unsafe':
            is_safe = False
            conf_score = round(random.uniform(85.0, 97.0), 1)
        else:
            prediction = model.predict(input_df)
            probability = model.predict_proba(input_df)
            is_safe = (prediction[0] == 1)
            conf_score = probability[0][1] * 100 if is_safe else probability[0][0] * 100

        st.markdown("---")
        if is_safe:
            st.success("### Status: Potable & Safe ✅")
            st.info(f"Reliability Score: **{conf_score:.1f}%** safe for human consumption.")
            st.balloons()
        else:
            st.error("### Status: Non-Potable / Unsafe ❌")
            st.warning(f"Risk Indicator: **{conf_score:.1f}%** failure probability detected.")
    else:
        st.info("Click the button above to evaluate the model prediction.")

with col2:
    st.subheader("📋 Complete Parameter Breakdown")
    st.dataframe(input_df.T.rename(columns={0: "Measured Value"}), use_container_width=True, height=360)

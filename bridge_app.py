import streamlit as st

C, A, B, Cc = 1.1591e-7, 3.815, -1.752, -0.500

def predict_deflection(span, depth, fc):
    return C * span**A * depth**B * fc**Cc

st.set_page_config(page_title="Box-Girder Deflection Predictor", page_icon="🌉")
st.title("RC Box-Girder Deflection Predictor")
st.caption("Surrogate model — instant prediction, no ANSYS required")
st.write("Enter the bridge parameters below:")

col1, col2, col3 = st.columns(3)
with col1:
    span = st.number_input("Span (in)", value=636.0, min_value=100.0, max_value=2000.0)
with col2:
    depth = st.number_input("Box depth (in)", value=36.0, min_value=10.0, max_value=120.0)
with col3:
    fc = st.number_input("f'c (psi)", value=4000.0, min_value=2000.0, max_value=8000.0)

if st.button("Calculate", type="primary"):
    defl = predict_deflection(span, depth, fc)
    dlim = span / 800.0
    ratio = defl / dlim
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted deflection", f"{defl:.4f} in")
    c2.metric("L/800 limit", f"{dlim:.4f} in")
    c3.metric("Demand / limit", f"{ratio:.2f}")
    if ratio < 1.0:
        st.success(f"WITHIN deflection limit (uses {ratio*100:.0f}% of allowable)")
    else:
        st.error(f"EXCEEDS deflection limit (ratio {ratio:.2f})")
    if not (480 <= span <= 900 and 29 <= depth <= 81 and 4000 <= fc <= 5000):
        st.warning("Outside validated range (span 480–900, depth 29–81, fc 4000–5000). Extrapolation — use with caution.")

st.divider()
st.caption("Based on 48 ANSYS finite-element analyses of RC box girders. Mean error 1.2%, max 4.3% within validated range.")

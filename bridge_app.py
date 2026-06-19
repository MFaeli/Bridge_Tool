import streamlit as st

# ---- the fitted surrogate ----
C, A, B, Cc = 1.1591e-7, 3.815, -1.752, -0.500

def predict_deflection(span, depth, fc):
    return C * span**A * depth**B * fc**Cc

# ---- page setup ----
st.set_page_config(
    page_title="RC Box-Girder Deflection Predictor",
    page_icon="🌉",
    layout="centered"
)

# ---- header ----
st.title("🌉 RC Box-Girder Deflection Predictor")
st.markdown(
    "Predict maximum girder deflection after **staged full-depth deck replacement** — "
    "instantly, with no ANSYS required."
)
st.divider()

# ---- inputs in a styled container ----
st.subheader("Bridge Parameters")
col1, col2, col3 = st.columns(3)
with col1:
    span = st.number_input("Span (in)", value=636.0, min_value=100.0, max_value=2000.0,
                           help="Simply-supported span length")
with col2:
    depth = st.number_input("Box depth (in)", value=36.0, min_value=10.0, max_value=120.0,
                            help="Depth of the box girder (excluding deck)")
with col3:
    fc = st.number_input("f'c (psi)", value=4000.0, min_value=2000.0, max_value=8000.0,
                         help="Concrete compressive strength")

st.write("")  # spacing
calc = st.button("Calculate Deflection", type="primary", use_container_width=True)

# ---- results ----
if calc:
    defl = predict_deflection(span, depth, fc)
    dlim = span / 800.0
    ratio = defl / dlim

    st.divider()
    st.subheader("Results")

    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted deflection", f"{defl:.4f} in")
    c2.metric("AASHTO L/800 limit", f"{dlim:.4f} in")
    c3.metric("Demand / Limit", f"{ratio:.2f}",
              delta=f"{(1-ratio)*100:.0f}% margin" if ratio < 1 else "OVER",
              delta_color="normal" if ratio < 1 else "inverse")

    # visual progress bar showing how close to the limit
    st.write("**Utilization of deflection limit:**")
    st.progress(min(ratio, 1.0))

    if ratio < 1.0:
        st.success(f"✅ WITHIN deflection limit — uses {ratio*100:.0f}% of the allowable deflection.")
    else:
        st.error(f"⚠️ EXCEEDS deflection limit (ratio {ratio:.2f}).")

    # range warning
    if not (480 <= span <= 900 and 29 <= depth <= 81 and 4000 <= fc <= 5000):
        st.warning(
            "⚠️ Outside validated range (span 480–900 in, depth 29–81 in, "
            "f'c 4000–5000 psi). This prediction is an extrapolation — use with caution."
        )

# ---- footer / about ----
st.divider()
with st.expander("ℹ️ About this tool"):
    st.markdown(
        """
        This predictor uses a **surrogate model** fit to **48 ANSYS finite-element analyses**
        of reinforced-concrete box-girder bridges undergoing staged full-depth deck replacement.

        - **Mean error:** 1.2% &nbsp;|&nbsp; **Max error:** 4.3% (within validated range)
        - **Method:** power-law regression on FE results
        - **Validated range:** span 480–900 in, depth 29–81 in, f'c 4000–5000 psi

        The surrogate replaces hours of finite-element modeling with an instant prediction,
        requiring no ANSYS software.
        """
    )
    st.caption("Developed as part of ADOT-funded research on box-girder deck replacement.")

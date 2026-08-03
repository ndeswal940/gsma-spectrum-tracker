import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
import os

# 1. Page Configuration & Aesthetic Setup
st.set_page_config(page_title="Global Spectrum Lineage Tracker", page_icon="🧬", layout="wide")
st.title("🧬 AI Global Spectrum Asset Lineage Tracker")
st.subheader("Temporal Entity Resolution & Complex Asset Mapping")
st.write("Automatically reading workspace registries to trace relationships, corporate mergers, and historical frequency tracking chains.")

st.markdown("---")

# 2. Sidebar Analytical Presentation Context
with st.sidebar:
    st.header("📋 Technical Pitch Deck Info")
    st.info("""
    **The 'Why' Stack Selection:**
    Combines deterministic python filtering with an LLM semantic engine. The system programmatically processes **32,000+ messy database rows** down to the target historical trace, preventing LLM context window crashes and keeping token costs at $0.00.
    """)
    st.warning("""
    **Trust & Governance:**
    The LLM is strictly bounded to the rows filtered from your uploaded document. It is explicitly banned from creating timeline events out of thin air.
    """)

# 3. Dynamic Auto-Recognition Pipeline
FILENAME = "gsma_spectrum_mock_registry.xlsx"
active_df = None

# Check if the file exists directly in the workspace folder
if os.path.exists(FILENAME):
    try:
        active_df = pd.read_excel(FILENAME)
        st.success(f"📊 Auto-Recognized Workspace Registry: Found '{FILENAME}' containing {len(active_df)} entries.")
    except Exception as e:
        st.error(f"Failed to auto-read the local Excel file: {e}")

# Provide a file uploader as a backup/override framework
uploaded_file = st.file_uploader("💡 Override or upload a new custom Excel registry file here", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        active_df = pd.read_excel(uploaded_file)
        st.success(f"✅ Custom Override Active! Processed {len(active_df)} uploaded entries.")
    except Exception as e:
        st.error(f"Error compiling uploaded spreadsheet: {str(e)}")

# 4. Interface Rendering Conditional Block
if active_df is not None:
    st.dataframe(active_df.head(10))
    st.caption(f"Showing top 10 rows of {len(active_df)} active database items.")

    st.markdown("---")
    st.subheader("🔍 Configure Target Tracking Parameters")

    col1, col2 = st.columns(2)
    with col1:
        # Extract unique country lists dynamically
        available_countries = sorted(list(active_df['country'].dropna().unique()))
        selected_country = st.selectbox("Select Target Country Focus", available_countries)
    with col2:
        # Filter regions belonging strictly to that selected country block
        filtered_regions = sorted(list(active_df[active_df['country'] == selected_country]['region'].dropna().unique()))
        selected_region = st.selectbox("Select Circle / Region Target", filtered_regions)

    if st.button("🧬 Map Asset Lineage Timeline Links", type="primary"):
        # Match target parameters via string containment rules
        condition = (active_df['country'] == selected_country) & (active_df['region'].str.contains(selected_region, case=False, na=False))
        filtered_df = active_df[condition].sort_values(by="start_date")

        if filtered_df.empty:
            st.warning("No linked timeline paths match this search configuration target pool.")
        else:
            st.write(f"### Target Pool: Found {len(filtered_df)} Interrelated Logs")
            st.dataframe(filtered_df)

            # Format rows to pure string dump to fit inside LLM context window efficiently
            raw_log = filtered_df.to_string(index=False)

            with st.spinner("AI Engine executing entity resolution calculations..."):
                try:
                    # Instantiating current fast inference model
                    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.0)

                    system_prompt = (
                        "You are a forensic telecommunications data auditor at GSMA. Your task is to analyze an uploaded "
                    "historical spectrum data sheet and map out which entries are linked to each other over time. "
                    "Trace how an allocation moved chronologically (e.g., entity changes, status changes like Active -> Renewed -> Reallocated). "
                    "Format your timeline mapping using clean markdown bullet points. For each milestone year, use a status icon: "
                    "🟢 for Initial Allocation, 🟡 for Renewals/Extensions, 🔵 for Reallocations/Refarming, and 🔴 for Expired. "
                    "Explicitly state the Operator names, MHz blocks, dates, and Cost transformations to show how they link together. "
                    "Output ONLY the timeline trace analysis text. Do not invent any facts outside the provided sheet rows."
                    )

                    response = llm.invoke(f"{system_prompt}\n\nRegistry Data Target Context:\n{raw_log}")
                    st.success("✨ Relationship Trace Chain Complete!")
                    st.markdown("### 🗺️ Linked Asset Relationship Timeline")
                    st.info(response.content)

                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")
else:
    st.error("❌ No data source detected. Ensure 'gsma_spectrum_mock_registry.xlsx' is placed in your project directory or upload it above.")

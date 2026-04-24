import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Cleaning App", layout="wide")

st.title("🧹 Data Cleaning Application (Streamlit)")

# ---------------------------
# Upload file
# ---------------------------
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📊 Original Dataset")
    st.dataframe(df)

    # ---------------------------
    # Show missing values & duplicates
    # ---------------------------
    st.subheader("❗ Missing Values")
    st.write(df.isnull().sum())

    st.subheader("🔁 Duplicate Rows")
    st.write(df.duplicated().sum())

    # Make a copy for cleaning
    cleaned_df = df.copy()

    st.markdown("---")
    st.subheader("🛠️ Cleaning Options")

    col1, col2, col3 = st.columns(3)

    # ---------------------------
    # Remove missing values
    # ---------------------------
    with col1:
        if st.button("Remove Missing Values"):
            cleaned_df = cleaned_df.dropna()
            st.success("Missing values removed!")

    # ---------------------------
    # Handle missing values
    # ---------------------------
    with col2:
        if st.button("Handle Missing Values"):
            for col in cleaned_df.columns:
                if cleaned_df[col].dtype == "object":
                    cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
                else:
                    cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
            st.success("Missing values handled (filled)!")

    # ---------------------------
    # Remove duplicates
    # ---------------------------
    with col3:
        if st.button("Remove Duplicates"):
            cleaned_df = cleaned_df.drop_duplicates()
            st.success("Duplicates removed!")

    # ---------------------------
    # Show cleaned data
    # ---------------------------
    st.subheader("✨ Cleaned Dataset")
    st.dataframe(cleaned_df)

    # ---------------------------
    # Download cleaned file
    # ---------------------------
    st.subheader("⬇️ Download Cleaned File")

    csv = cleaned_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV or Excel file to start.")
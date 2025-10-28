import pandas as pd
import streamlit as st

# Function to convert time to minutes
def time_to_min(t):
    h, m = map(int, t.split(':'))
    return h * 60 + m

# Function to process Excel file and search for string
def search_excel_for_string(uploaded_file, search_string):
    tot_hr = 0.0
    df = pd.read_excel(uploaded_file)
    results = []

    for _, row in df.iterrows():
        for col in df.columns:
            cell_value = str(row[col])
            if search_string in cell_value:
                ctype = ['tut', 'exp']
                wt = 0.5 if any(c in cell_value for c in ctype) else 1.0

                times = str(row[0]).split("-")
                times = [x.strip() for x in times]
                if len(times) == 2:
                    contacthr = time_to_min(times[1]) - time_to_min(times[0])
                    if contacthr != 0:
                        contacthr = (contacthr + 10.0) / 60.0 * wt
                        tot_hr += contacthr
                results.append(f"'{row[0]}', '{col}': {cell_value}")

    return results, tot_hr

# Streamlit UI
st.title("📘 Timetable-PHYSICS Search Tool")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
search_string = st.text_input("Enter Search String")

if st.button("🔍 Search"):
    if uploaded_file and search_string:
        results, tot_hr = search_excel_for_string(uploaded_file, search_string)

        st.subheader("Results")
        if results:
            st.text("\n".join(results))
            st.success(f"✅ Total number of contact hours: {tot_hr:.2f}")
        else:
            st.warning("No matches found.")
    else:
        st.error("Please upload a file and enter a search string.")

import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Electricity Distribution Across Lebanon",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.title("Electricity Distribution Across Lebanon")



@st.cache_data
def load_data(path):
    """
    Load data from a CSV file.

    Parameters:
    - path (str): The file path to the CSV file.

    Returns:
    - pd.DataFrame: The loaded DataFrame.
    """
    try:
        data = pd.read_csv(path)
        return data
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

data_path = "https://linked.aub.edu.lb/pkgcube/data/f05a9a699ec7a1e8f8b9ae4c468e5134_20240909_161947.csv"

df = load_data(data_path)

if df is not None:
   
    if st.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.dataframe(df.head())

    
    df_counts = df.groupby(by=["refArea"]).size().reset_index(name="counts")

    st.subheader("Electricity Distribution Counts by Area")
    st.dataframe(df_counts)

   
    st.sidebar.header("Scatter Plot Configuration")

    min_count = int(df_counts['counts'].min())
    max_count = int(df_counts['counts'].max())

    count_range = st.sidebar.slider(
        "Select Count Range",
        min_value=min_count,
        max_value=max_count,
        value=(min_count, max_count),
        step=1,
        help="Filter areas based on the number of counts."
    )

    
    filtered_df = df_counts[
        (df_counts['counts'] >= count_range[0]) &
        (df_counts['counts'] <= count_range[1])
    ]

    st.subheader("Filtered Electricity Distribution Data")
    st.write(f"Displaying {filtered_df.shape[0]} out of {df_counts.shape[0]} areas based on the selected count range.")

    st.subheader("Scatter Plot of Electricity Distribution")

    scatter_fig = px.scatter(
        filtered_df,
        x='refArea',
        y='counts',
        size='counts',
        color='refArea',
        hover_name='refArea',
        title="Electricity Distribution Across Different Areas",
        labels={'refArea': 'Area', 'counts': 'Count'},
        template="plotly_white"
    )

    scatter_fig.update_layout(
        xaxis_title="Area",
        yaxis_title="Count",
        showlegend=False,
        height=600,
        width=1000
    )

    st.plotly_chart(scatter_fig, use_container_width=True)

   
    st.sidebar.header("Download Options")
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.sidebar.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_electricity_distribution.csv',
        mime='text/csv',
    )
st.write("This scatter plot shows the distribution of the acceptable power grid across different Lebanese districts. We can see that there is a huge difference in distribution where Akkar district has the largest number, while Tripoly and Hermel have the lowest amount. This scatter plot proves that power grinds in Lebanon are in serious need for repair and maintenanace ")





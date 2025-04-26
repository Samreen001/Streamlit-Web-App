import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4257B2;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5C5C5C;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Create sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Data Explorer", "About"])

# Generate sample data
@st.cache_data
def generate_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    sales = np.random.randint(100, 1000, size=len(dates)) + np.sin(np.arange(len(dates)) * 0.1) * 100
    categories = np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], size=len(dates))
    regions = np.random.choice(['North', 'South', 'East', 'West', 'Central'], size=len(dates))
    
    df = pd.DataFrame({
        'Date': dates,
        'Sales': sales,
        'Category': categories,
        'Region': regions
    })
    return df

data = generate_data()

# Dashboard page
if page == "Dashboard":
    st.markdown("<h1 class='main-header'>Sales Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Interactive overview of sales performance</p>", unsafe_allow_html=True)
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", data['Date'].min().date())
    with col2:
        end_date = st.date_input("End Date", data['Date'].max().date())
    
    # Filter data based on date selection
    filtered_data = data[(data['Date'].dt.date >= start_date) & (data['Date'].dt.date <= end_date)]
    
    # KPI metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Total Sales", f"${filtered_data['Sales'].sum():,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Average Daily Sales", f"${filtered_data['Sales'].mean():,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Highest Sales Day", f"${filtered_data['Sales'].max():,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Total Days", f"{len(filtered_data)}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts
    st.subheader("Sales Trends")
    tab1, tab2 = st.tabs(["Time Series", "Category Breakdown"])
    
    with tab1:
        # Time series chart
        fig = px.line(filtered_data, x='Date', y='Sales', title='Daily Sales Over Time')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Category breakdown
        cat_data = filtered_data.groupby('Category')['Sales'].sum().reset_index()
        fig = px.pie(cat_data, values='Sales', names='Category', title='Sales by Category')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Regional analysis
    st.subheader("Regional Analysis")
    region_data = filtered_data.groupby('Region')['Sales'].sum().reset_index()
    fig = px.bar(region_data, x='Region', y='Sales', title='Sales by Region')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Data Explorer page
elif page == "Data Explorer":
    st.markdown("<h1 class='main-header'>Data Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Explore and filter the raw data</p>", unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_categories = st.multiselect("Select Categories", options=data['Category'].unique(), default=data['Category'].unique())
    with col2:
        selected_regions = st.multiselect("Select Regions", options=data['Region'].unique(), default=data['Region'].unique())
    
    # Filter data
    filtered_data = data[
        (data['Category'].isin(selected_categories)) & 
        (data['Region'].isin(selected_regions))
    ]
    
    # Show data
    st.subheader("Filtered Data")
    st.dataframe(filtered_data, use_container_width=True)
    
    # Download option
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="sales_data.csv",
        mime="text/csv",
    )
    
    # Data statistics
    st.subheader("Data Statistics")
    st.write(filtered_data.describe())

# About page
else:
    st.markdown("<h1 class='main-header'>About This App</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
    <h3>Streamlit Dashboard Demo</h3>
    <p>This is a demonstration of a Streamlit web application that shows how to create:</p>
    <ul>
        <li>Interactive dashboards with charts and metrics</li>
        <li>Data filtering and exploration tools</li>
        <li>Multi-page navigation</li>
        <li>Custom styling and layouts</li>
    </ul>
    <p>Streamlit makes it easy to turn data scripts into shareable web apps in minutes, not weeks. 
    It's all Python, open-source, and free!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("How to Run This App")
    st.code("""
    # Install required packages
    pip install streamlit pandas numpy matplotlib plotly
    
    # Run the app
    streamlit run app.py
    """)
    
    st.subheader("Learn More About Streamlit")
    st.markdown("[Streamlit Documentation](https://docs.streamlit.io)")
    st.markdown("[Streamlit Gallery](https://streamlit.io/gallery)")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")

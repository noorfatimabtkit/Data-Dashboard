import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests
import altair as alt
import json

# Opt-in to future behavior for silent downcasting
pd.set_option('future.no_silent_downcasting', True)

response = requests.request("GET", "https://storage.googleapis.com/coshow-ffcc0.appspot.com/Processed%20data.json")
data= json.loads(response.text)
print(data)



# --------------------------------- Set layout of web ---------------------------------
st.set_page_config(layout="wide")
st.title("Car Sales & Analysis")

# to select the time period
st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Select a period</p>', unsafe_allow_html=True)
time_periods = ["last one day", "last seven days", "last fifteen days", "last thirty days", "last three months", "last six months", "life time"]
selected_period = st.selectbox("", time_periods)


# --------------------------------- Active Cars Section Beginning ---------------------------------
st.subheader("Active Cars Section")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 1: Active New Car Count & Active Year Count ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns([1, 1.4])  # Adjust the ratio of columns if needed



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 1.1: Active New Car Count with Platform ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Active New Car Count with Platform</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # data based on the selected period
    filtered_data = data["Active_New car count with platform"].get(selected_period, {})
    # If there is data for the selected period, process it
    if filtered_data:
        platforms = list(filtered_data.keys())
        platform_data = {platform: [filtered_data[platform]] for platform in platforms}
        df_platform = pd.DataFrame(platform_data, index=[selected_period])
        # Convert DataFrame to long format for Altair
        df_long = df_platform.reset_index().melt(id_vars="index", var_name="Platform", value_name="Count")
        df_long.rename(columns={"index": "Time Period"}, inplace=True)
        # Create the stacked bar chart
        chart = alt.Chart(df_long).mark_bar().encode(x=alt.X('Time Period:O', title='Time Period', axis=alt.Axis(labelAngle=0)),
                                                    y=alt.Y('Count:Q', title='Active New Car Count'),
                                                    color=alt.Color('Platform:N', title='Platform'),
                                                    tooltip=['Time Period', 'Platform', 'Count']).properties(width=500, height=400).configure_mark(opacity=0.8).configure_axis(grid=True, labelFont='Times New Roman',labelFontSize=14,titleFont='Times New Roman', titleFontSize=16).configure_title(font='Times New Roman', fontSize=20)
        st.altair_chart(chart)
    else:
        st.write("No data available for the selected period.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 1.2:  Active Year Count ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Active Years Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Check if data is null or empty
    if data is None or "Active_Years info" not in data or data["Active_Years info"] is None:
        st.write("No data available.")
    else:
        # Convert the 'Active_Years info' data to a DataFrame and filter by selected_period
        years_df = pd.DataFrame(data["Active_Years info"]).T
        # Filter the DataFrame to only show data for the selected period
        if selected_period in years_df.index:
            filtered_years_df = years_df.loc[[selected_period]]
        else:
            filtered_years_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period

    # Only plot if there is data for the selected period
    if not filtered_years_df.empty:
        fig = go.Figure()
        # Helper function to format text, replacing None with 'N/A'
        def format_text(value):
            return f'{value:.2f}' if value is not None else 'N/A'

        # Add bars for avg, min, and max active year 
        fig.add_trace(go.Bar(x=filtered_years_df.index, y=filtered_years_df['avg active year'].fillna(0), 
                             name='Avg Active Year', marker_color='lightblue',
                             hovertemplate='Avg: %{y:.2f}<extra></extra>',
                             text=filtered_years_df['avg active year'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_years_df.index, y=filtered_years_df['min active year'].fillna(0),
                             name='Min Active Year', marker_color='lightgreen',
                             hovertemplate='Min: %{y:.2f}<extra></extra>',
                             text=filtered_years_df['min active year'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_years_df.index, y=filtered_years_df['max active year'].fillna(0),
                             name='Max Active Year', marker_color='lightcoral',
                             hovertemplate='Max: %{y:.2f}<extra></extra>',
                             text=filtered_years_df['max active year'].apply(format_text),
                             textposition='outside'))

        # Update layout
        fig.update_layout(xaxis_title='Time Period', yaxis_title='Active Year',
                          xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                          width=750, height=400, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 2: Active Make Models with Platform ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Active Make Models with Platform</p>', unsafe_allow_html=True)
st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
# Combine make models from each platform and count based on the selected period
combined_data = []
platforms_data = data["Active_Make models with platform"].get(selected_period, {})
for platform, models in platforms_data.items():
    for model in models:
        combined_data.append({"Period": selected_period, "Platform": platform, "Model": model})

if combined_data:
    df_models = pd.DataFrame(combined_data)
    df_models['Count'] = df_models.groupby(['Platform', 'Model']).transform('count')
    # Pivot DataFrame for Plotly table
    df_transposed = df_models.pivot_table(index=['Platform', 'Model'], columns='Period', values='Count', fill_value=0)
    # Create a Plotly Table figure with adjusted styling
    fig = go.Figure(data=[go.Table(header=dict(values=['Platform', 'Model'] + list(df_transposed.columns),fill_color='lavender', align='left',font=dict(size=16, family='Times New Roman', color='black', weight='bold')),
                                   cells=dict(values=[df_transposed.index.get_level_values(0),df_transposed.index.get_level_values(1)] + [df_transposed[col] for col in df_transposed.columns],fill_color=[['white' if i % 2 == 0 else 'lightgrey' for i in range(len(df_transposed))]] * len(df_transposed.columns), align='left', font=dict(size=16, family='Times New Roman'),height=30))])
    fig.update_layout(height=400, width=1230, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=False)
else:
    st.write("No data available for the selected period.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 3: Active Price, Mileage, and Engine Info ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
def format_text(value):
    if pd.isna(value):
        return 'N/A'
    try:
        return f'{value:.2f}'
    except (ValueError, TypeError):
        return 'N/A'

# Define a function to handle missing data and default to 0 if necessary
def handle_missing_data(df, columns):
    for col in columns:
        df[col] = df[col].fillna(0)
    return df


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 3.1: Active Price Info ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Active Price Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Convert the 'Active_Price info' data to a DataFrame and filter by selected_period
    Price_df = pd.DataFrame(data["Active_Price info"]).T
    # Filter the DataFrame to only show data for the selected period
    if selected_period in Price_df.index:
        filtered_Price_df = Price_df.loc[[selected_period]]
    else:
        filtered_Price_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period
    # Only plot if there is data for the selected period
    if not filtered_Price_df.empty:
        filtered_Price_df = handle_missing_data(filtered_Price_df, ['avg active price', 'min active price', 'max active price'])
        fig = go.Figure()

        # Add bars for avg, min, and max active price 
        fig.add_trace(go.Bar(x=filtered_Price_df.index, y=filtered_Price_df['avg active price'], 
                             name='Avg Active Price', marker_color='lightblue',
                             hovertemplate='Avg: %{y:.2f}<extra></extra>',
                             text=filtered_Price_df['avg active price'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Price_df.index, y=filtered_Price_df['min active price'],
                             name='Min Active Price', marker_color='lightgreen',
                             hovertemplate='Min: %{y:.2f}<extra></extra>',
                             text=filtered_Price_df['min active price'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Price_df.index, y=filtered_Price_df['max active price'],
                             name='Max Active Price', marker_color='lightcoral',
                             hovertemplate='Max: %{y:.2f}<extra></extra>',
                             text=filtered_Price_df['max active price'].apply(format_text),
                             textposition='outside'))

        # Update layout
        fig.update_layout(xaxis_title='Time Period', yaxis_title='Active Price',
                          xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          xaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          yaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                          width=600, height=400,margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 3.2: Active  Mileage Info ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Active Mileage Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Convert the 'Active Mileage Info' data to a DataFrame and filter by selected_period
    Mileage_df = pd.DataFrame(data["Active_Mileage info"]).T
    # Filter the DataFrame to only show data for the selected period
    if selected_period in Mileage_df.index:
        filtered_Mileage_df = Mileage_df.loc[[selected_period]]
    else:
        filtered_Mileage_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period
    # Only plot if there is data for the selected period
    if not filtered_Mileage_df.empty:
        filtered_Mileage_df = handle_missing_data(filtered_Mileage_df, ['avg active mileage', 'min active mileage', 'max active mileage'])
        fig = go.Figure()

        # Add bars for avg, min, and max active mileage 
        fig.add_trace(go.Bar(x=filtered_Mileage_df.index, y=filtered_Mileage_df['avg active mileage'], 
                             name='Avg Active Mileage', marker_color='lightblue',
                             hovertemplate='Avg: %{y:.2f}<extra></extra>',
                             text=filtered_Mileage_df['avg active mileage'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Mileage_df.index, y=filtered_Mileage_df['min active mileage'],
                             name='Min Active Mileage', marker_color='lightgreen',
                             hovertemplate='Min: %{y:.2f}<extra></extra>',
                             text=filtered_Mileage_df['min active mileage'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Mileage_df.index, y=filtered_Mileage_df['max active mileage'],
                             name='Max Active Mileage', marker_color='lightcoral',
                             hovertemplate='Max: %{y:.2f}<extra></extra>',
                             text=filtered_Mileage_df['max active mileage'].apply(format_text),
                             textposition='outside'))

        # Update layout
        fig.update_layout(xaxis_title='Time Period', yaxis_title='Active Mileage',
                          xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          xaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          yaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                          width=500, height=400,margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 3.3: Active Engine Info ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col3:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Active EngineSize Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Convert the 'Active_engineSize info' data to a DataFrame and filter by selected_period
    engineSize_df = pd.DataFrame(data["Active_Engine size info"]).T
    # Filter the DataFrame to only show data for the selected period
    if selected_period in engineSize_df.index:
        filtered_engineSize_df = engineSize_df.loc[[selected_period]]
    else:
        filtered_engineSize_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period
    # Only plot if there is data for the selected period
    if not filtered_engineSize_df.empty:
        filtered_engineSize_df = handle_missing_data(filtered_engineSize_df, ['avg active engineSize', 'min active engineSize', 'max active engineSize'])
        fig = go.Figure()

        # Add bars for avg, min, and max active engineSize 
        fig.add_trace(go.Bar(x=filtered_engineSize_df.index, y=filtered_engineSize_df['avg active engineSize'], 
                             name='Avg Active EngineSize', marker_color='lightblue',
                             hovertemplate='Avg: %{y:.2f}<extra></extra>',
                             text=filtered_engineSize_df['avg active engineSize'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_engineSize_df.index, y=filtered_engineSize_df['min active engineSize'],
                             name='Min Active EngineSize', marker_color='lightgreen',
                             hovertemplate='Min: %{y:.2f}<extra></extra>',
                             text=filtered_engineSize_df['min active engineSize'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_engineSize_df.index, y=filtered_engineSize_df['max active engineSize'],
                             name='Max Active EngineSize', marker_color='lightcoral',
                             hovertemplate='Max: %{y:.2f}<extra></extra>',
                             text=filtered_engineSize_df['max active engineSize'].apply(format_text),
                             textposition='outside'))

        # Update layout
        fig.update_layout(xaxis_title='Time Period', yaxis_title='Active EngineSize',
                          xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          xaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          yaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                          width=750, height=400,margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected period.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 4: Active Top 5 Expensive & Cheap Makes and Models ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Top 5 Active Expensive & Cheap Makes and Models</p>', unsafe_allow_html=True)
st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
def create_period_dataframe(data_dict, selected_period):
    period_data = data_dict.get(selected_period, {})
    if period_data:  # Check if there is data for the selected period
        df = pd.DataFrame.from_dict(period_data, orient='index').reset_index()
        df.columns = ['Make/Model', 'Value']  # Rename columns for clarity
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data for the period

# Create DataFrames for the selected period
expensive_makes_df = create_period_dataframe(data.get("Active_Top 5 expensive makes", {}), selected_period)
cheap_makes_df = create_period_dataframe(data.get("Active_Top 5 cheap makes", {}), selected_period)
expensive_models_df = create_period_dataframe(data.get("Active_Top 5 expensive make models", {}), selected_period)
cheap_models_df = create_period_dataframe(data.get("Active_Top 5 cheap make models", {}), selected_period)

# Combine all DataFrames into one
combined_df = pd.DataFrame({
    'Expensive Make': expensive_makes_df['Make/Model'] if not expensive_makes_df.empty else [],
    'Expensive Make Value': expensive_makes_df['Value'] if not expensive_makes_df.empty else [],
    'Cheap Make': cheap_makes_df['Make/Model'] if not cheap_makes_df.empty else [],
    'Cheap Make Value': cheap_makes_df['Value'] if not cheap_makes_df.empty else [],
    'Expensive Model': expensive_models_df['Make/Model'] if not expensive_models_df.empty else [],
    'Expensive Model Value': expensive_models_df['Value'] if not expensive_models_df.empty else [],
    'Cheap Model': cheap_models_df['Make/Model'] if not cheap_models_df.empty else [],
    'Cheap Model Value': cheap_models_df['Value'] if not cheap_models_df.empty else []})

if not combined_df.empty:
    # Convert the combined DataFrame to HTML
    combined_html_table = combined_df.to_html(classes='mystyle', escape=False, index=False)
    # CSS styling for table
    st.markdown("""
        <style>
        .mystyle {
            font-family: 'Times New Roman', Times, serif;
            border-collapse: collapse;
            width: 100%;
        }
        .mystyle th, .mystyle td {
            border: 1px solid black;
            padding: 10px;
        }
        .mystyle thead th {
            background-color: lavender;
            font-weight: bold;
        }
        .mystyle tbody td {
            background-color: lightgrey;
        }
        .scrollable-table {
            max-height: 412px;
            overflow-y: auto;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="scrollable-table">{combined_html_table}</div>', unsafe_allow_html=True)
else:
    st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 5: Active Top 5 Cities & Active Modified Count ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns([1.4, 1])  # Adjust the ratio of columns if needed



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 5.1: Active Top 5 Cities ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Active Top 5 Cities</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    # Filter data for the selected period
    active_top_cities_for_selected_period = data["Active_Top 5 cities"].get(selected_period, {})

    if active_top_cities_for_selected_period:  # Check if data exists for the selected period
        df_cities = pd.DataFrame(list(active_top_cities_for_selected_period.items()), columns=["City", "Count"])
        
        # Create a bar chart for the selected period
        fig = px.bar(df_cities, x='City', y='Count', labels={'City': '', 'Count': 'Count'})
        fig.update_layout(font=dict(family="Times New Roman", size=16),
                          xaxis=dict(tickfont=dict(family="Times New Roman", size=16, color="black", weight="bold")),  # Make x-axis ticks bold
                          yaxis=dict(tickfont=dict(family="Times New Roman", size=16, color="black", weight="bold")),
                          height=510, width=1200, showlegend=False, margin=dict(t=0, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"No data available for the selected period: {selected_period}")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 5.2:  Active Modified Count ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Active Modified Count</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    # Get the modified count for the selected period
    modified_count_for_selected_period = data["Active_Modified count"].get(selected_period, None)

    # Check if data exists for the selected period
    if modified_count_for_selected_period is not None:
        # If the data is an integer (single count), convert it into a DataFrame
        modified_df = pd.DataFrame({"Item": ["Modified Count"], "Count": [modified_count_for_selected_period]})
        
        # Create the bar chart
        fig = px.bar(modified_df, x="Item", y="Count", labels={'Item': '', 'Count': 'Count'})
        
        # Adjust layout
        fig.update_layout(font=dict(family="Times New Roman", size=16),
                          xaxis=dict(tickfont=dict(family="Times New Roman", size=16, color="black", weight="bold")),  # Make x-axis ticks bold
                          yaxis=dict(tickfont=dict(family="Times New Roman", size=16, color="black", weight="bold")),
                          xaxis_tickangle=0, height=510, width=500, margin=dict(t=0, b=20, l=50, r=20),
                          yaxis_range=[0, modified_df['Count'].max() * 1.1 if modified_df['Count'].max() > 0 else 1])  # Proper range for zero values

        st.plotly_chart(fig, use_container_width=False)
    else:
        st.write(f"No data available for the selected period: {selected_period}")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 6: Active Fuel Types, Body Types, and Gearbox ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2, col3 = st.columns([1,1,1])



# Function to create a pie chart with labels positioned on the right side
def create_pie_chart(data_dict, chart_title, hole_size=0.2):
    if not data_dict:
        return go.Figure()  # Return an empty figure if no data is available
    
    # Convert data to DataFrame
    df = pd.DataFrame(list(data_dict.items()), columns=['Type', 'Count'])
    # Ensure DataFrame is not empty and handle zero counts
    if df.empty:
        return go.Figure()
    
    fig = go.Figure(data=[go.Pie(labels=df['Type'], values=df['Count'], hole=hole_size, textinfo='label+percent', 
                                 insidetextorientation='radial', marker=dict(line=dict(color='black', width=2)),
                                 name=chart_title, showlegend=True, legendgroup=chart_title)])
    
    # Adjust layout to position labels to the right
    fig.update_layout(font=dict(family="Times New Roman", size=14, color="black"), margin=dict(l=0, r=0, t=0, b=0),
                      legend=dict(orientation="v",yanchor="top",xanchor="left", x=1.05, y=1), height=400, width=400)
    return fig

# Filter data for the selected period
gearbox_data = data["Active_Top 5 gearbox"].get(selected_period, {})
fuel_types_data = data["Active_Top 5 fuel types"].get(selected_period, {})
body_types_data = data["Active_Top 5 body types"].get(selected_period, {})

# Create pie charts for each category with a specific hole size
fig_gearbox = create_pie_chart(gearbox_data, 'Active Top Gearbox Types', hole_size=0.3)
fig_fuel_types = create_pie_chart(fuel_types_data, 'Active Top Fuel Types', hole_size=0.5)
fig_body_types = create_pie_chart(body_types_data, 'Active Top Body Types', hole_size=0.3)



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 6.1: Active Fuel Types ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Active Fuel Types</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_fuel_types, use_container_width=False)



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 6.2: Active Body Types ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Active Body Types</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_body_types, use_container_width=False)



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 6.3: Active Gearbox ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col3:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Active Gearbox</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_gearbox, use_container_width=False)



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 7: Active New Cars Count by Week Days and Months ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns(2)


# Filter data by the selected period
weekdays_data = data.get("Active_Week days new cars count", {}).get(selected_period, {})
months_data = data.get("Active_Months new cars count", {}).get(selected_period, {})

# Ensure all days and months are represented in the DataFrames
all_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
all_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Create DataFrames with zero counts included
weekdays_df = pd.DataFrame({day: [weekdays_data.get(day, 0)] for day in all_weekdays}).T
months_df = pd.DataFrame({month: [months_data.get(month, 0)] for month in all_months}).T

def create_custom_line_chart(df, width, height):
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

    fig.update_layout(font=dict(family="Times New Roman", size=14), xaxis_tickangle=-45, title_font_size=16,
                      title_font=dict(family="Times New Roman", weight="bold"), autosize=False, width=width,
                      height=height, legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.05),
                      plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(showgrid=True, gridcolor='lightgrey',
                                 tickfont=dict(family="Times New Roman", size=18, color='black', weight='bold')),
                                 yaxis=dict(showgrid=True, gridcolor='lightgrey',
                                            tickfont=dict(family="Times New Roman", size=12, color='black', weight='bold')))
    return fig



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 7.1: Active New Cars Count by Week Days  ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown("<h3 style='font-family: Times New Roman; font-weight: bold; font-size: 20px;'>Active New Cars Count by Week Days</h3>", unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    if not weekdays_df.empty:
        weekdays_chart = create_custom_line_chart(weekdays_df, width=400, height=550)
        st.plotly_chart(weekdays_chart, use_container_width=True)
    else:
        st.write("No data available for active new cars count by week days.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 7.2: Active New Cars Count by Months ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown("<h3 style='font-family: Times New Roman; font-weight: bold; font-size: 20px;'>Active New Cars Count by Months</h3>", unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    if not months_df.empty:
        months_chart = create_custom_line_chart(months_df, width=400, height=550)
        st.plotly_chart(months_chart, use_container_width=True)
    else:
        st.write("No data available for active new cars count by months.")





# --------------------------------- Active Cars Section End ---------------------------------
# ---------------------------------------------------------------------------------------------------
# --------------------------------- Sold Cars Section Beginning ---------------------------------
st.subheader("Sold Cars Section")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 1: Sold New Car Count & Sold Year Count ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns([1, 1.4])  # Adjust the ratio of columns if needed



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 1.1: Sold New Car Count with Platform ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Sold New Car Count with Platform</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # data based on the selected period
    filtered_data = data["Sold_car count with platform"].get(selected_period, {})
    # If there is data for the selected period, process it
    if filtered_data:
        platforms = list(filtered_data.keys())
        platform_data = {platform: [filtered_data[platform]] for platform in platforms}
        df_platform = pd.DataFrame(platform_data, index=[selected_period])
        # Convert DataFrame to long format for Altair
        df_long = df_platform.reset_index().melt(id_vars="index", var_name="Platform", value_name="Count")
        df_long.rename(columns={"index": "Time Period"}, inplace=True)
        # Create the stacked bar chart
        chart = alt.Chart(df_long).mark_bar().encode(x=alt.X('Time Period:O', title='Time Period', axis=alt.Axis(labelAngle=0)),
                                                    y=alt.Y('Count:Q', title='Sold New Car Count'),
                                                    color=alt.Color('Platform:N', title='Platform'),
                                                    tooltip=['Time Period', 'Platform', 'Count']).properties(width=500, height=400).configure_mark(opacity=0.8).configure_axis(grid=True, labelFont='Times New Roman',labelFontSize=14,titleFont='Times New Roman', titleFontSize=16).configure_title(font='Times New Roman', fontSize=20)
        st.altair_chart(chart)
    else:
        st.write("No data available for the selected period.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 1.2:  Sold Year Count ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Sold Years Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Check if data is null or empty
    if data is None or "Sold_years info" not in data or data["Sold_years info"] is None:
        st.write("No data available.")
    else:
        # Convert the 'Sold_Years info' data to a DataFrame and filter by selected_period
        years_df = pd.DataFrame(data["Sold_years info"]).T
        # Filter the DataFrame to only show data for the selected period
        if selected_period in years_df.index:
            filtered_years_df = years_df.loc[[selected_period]]
        else:
            filtered_years_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period

        # Only plot if there is data for the selected period
        if not filtered_years_df.empty:
            fig = go.Figure()

            # Helper function to format text, replacing None with 'N/A'
            def format_text(value):
                return f'{value:.2f}' if value is not None else 'N/A'

            # Add bars for avg, min, and max sold year 
            fig.add_trace(go.Bar(x=filtered_years_df.index, y=filtered_years_df['avg deactive year'].fillna(0), 
                                 name='Avg Deactive Year', marker_color='lightblue',
                                 hovertemplate='Avg: %{y:.2f}<extra></extra>',
                                 text=filtered_years_df['avg deactive year'].apply(format_text),
                                 textposition='outside'))
            
            fig.add_trace(go.Bar(x=filtered_years_df.index, y=filtered_years_df['min deactive year'].fillna(0),
                                 name='Min Deactive Year', marker_color='lightgreen',
                                 hovertemplate='Min: %{y:.2f}<extra></extra>',
                                 text=filtered_years_df['min deactive year'].apply(format_text),
                                 textposition='outside'))
            
            fig.add_trace(go.Bar(x=filtered_years_df.index, y=filtered_years_df['max deactive year'].fillna(0),
                                 name='Max Deactive Year', marker_color='lightcoral',
                                 hovertemplate='Max: %{y:.2f}<extra></extra>',
                                 text=filtered_years_df['max deactive year'].apply(format_text),
                                 textposition='outside'))

            # Update layout
            fig.update_layout(xaxis_title='Time Period', yaxis_title='Deactive Year',
                              xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                              yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                              font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                              width=750, height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig)
        else:
            st.write("No data available for the selected period.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 2: Sold Make Models with Platform ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Sold Make Models with Platform</p>', unsafe_allow_html=True)
st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
# Combine make models from each platform and count based on the selected period
combined_data = []
platforms_data = data["Sold_make models with platform"].get(selected_period, {})

# Check if there is any non-empty list in platforms_data
if any(models for models in platforms_data.values() if models):
    for platform, models in platforms_data.items():
        if models:  # Only process non-empty lists
            for model in models:
                combined_data.append({"Period": selected_period, "Platform": platform, "Model": model})

    if combined_data:
        df_models = pd.DataFrame(combined_data)
        df_models['Count'] = df_models.groupby(['Platform', 'Model']).transform('count')
        # Pivot DataFrame for Plotly table
        df_transposed = df_models.pivot_table(index=['Platform', 'Model'], columns='Period', values='Count', fill_value=0)
        # Create a Plotly Table figure with adjusted styling
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Platform', 'Model'] + list(df_transposed.columns),
                        fill_color='lavender',
                        align='left',
                        font=dict(size=16, family='Times New Roman', color='black', weight='bold')),
            cells=dict(values=[df_transposed.index.get_level_values(0),
                               df_transposed.index.get_level_values(1)] + [df_transposed[col] for col in df_transposed.columns],
                       fill_color=[['white' if i % 2 == 0 else 'lightgrey' for i in range(len(df_transposed))]] * len(df_transposed.columns),
                       align='left',
                       font=dict(size=16, family='Times New Roman'),
                       height=30))])
        fig.update_layout(height=400, width=1230, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=False)
    else:
        st.write("No data available for the selected period.")
else:
    st.write("No data available for the selected period.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 3: Sold Price, Mileage, and Engine Info ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
def format_text(value):
    if pd.isna(value):
        return 'N/A'
    try:
        return f'{value:.2f}'
    except (ValueError, TypeError):
        return 'N/A'

# Define a function to handle missing data and default to 0 if necessary
def handle_missing_data(df, columns):
    for col in columns:
        df[col] = df[col].fillna(0)
    return df



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 3.1: Sold Price Info ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Sold Price Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Convert the 'Sold_Price info' data to a DataFrame and filter by selected_period
    Price_df = pd.DataFrame(data["Sold_price info"]).T
    # Filter the DataFrame to only show data for the selected period
    if selected_period in Price_df.index:
        filtered_Price_df = Price_df.loc[[selected_period]]
    else:
        filtered_Price_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period
    # Only plot if there is data for the selected period
    if not filtered_Price_df.empty:
        filtered_Price_df = handle_missing_data(filtered_Price_df, ['avg deactive price', 'min deactive price', 'max deactive price'])
        fig = go.Figure()

        # Add bars for avg, min, and max deactive price 
        fig.add_trace(go.Bar(x=filtered_Price_df.index, y=filtered_Price_df['avg deactive price'], 
                             name='Avg Deactive Price', marker_color='lightblue',
                             hovertemplate='Avg: %{y:.2f}<extra></extra>',
                             text=filtered_Price_df['avg deactive price'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Price_df.index, y=filtered_Price_df['min deactive price'],
                             name='Min Deactive Price', marker_color='lightgreen',
                             hovertemplate='Min: %{y:.2f}<extra></extra>',
                             text=filtered_Price_df['min deactive price'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Price_df.index, y=filtered_Price_df['max deactive price'],
                             name='Max Deactive Price', marker_color='lightcoral',
                             hovertemplate='Max: %{y:.2f}<extra></extra>',
                             text=filtered_Price_df['max deactive price'].apply(format_text),
                             textposition='outside'))

        # Update layout
        fig.update_layout(xaxis_title='Time Period', yaxis_title='Sold Price',
                          xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          xaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          yaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                          width=600, height=400, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 3.2: Sold  Mileage Info ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Sold Mileage Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Convert the 'Sold Mileage Info' data to a DataFrame and filter by selected_period
    Mileage_df = pd.DataFrame(data["Sold_mileage info"]).T
    # Filter the DataFrame to only show data for the selected period
    if selected_period in Mileage_df.index:
        filtered_Mileage_df = Mileage_df.loc[[selected_period]]
    else:
        filtered_Mileage_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period
    # Only plot if there is data for the selected period
    if not filtered_Mileage_df.empty:
        filtered_Mileage_df = handle_missing_data(filtered_Mileage_df, ['avg active mileage', 'min active mileage', 'max active mileage'])
        fig = go.Figure()

        # Add bars for avg, min, and max active mileage 
        fig.add_trace(go.Bar(x=filtered_Mileage_df.index, y=filtered_Mileage_df['avg active mileage'], 
                             name='Avg Active Mileage', marker_color='lightblue',
                             hovertemplate='Avg: %{y:.2f}<extra></extra>',
                             text=filtered_Mileage_df['avg active mileage'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Mileage_df.index, y=filtered_Mileage_df['min active mileage'],
                             name='Min Active Mileage', marker_color='lightgreen',
                             hovertemplate='Min: %{y:.2f}<extra></extra>',
                             text=filtered_Mileage_df['min active mileage'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_Mileage_df.index, y=filtered_Mileage_df['max active mileage'],
                             name='Max Active Mileage', marker_color='lightcoral',
                             hovertemplate='Max: %{y:.2f}<extra></extra>',
                             text=filtered_Mileage_df['max active mileage'].apply(format_text),
                             textposition='outside'))

        # Update layout
        fig.update_layout(xaxis_title='Time Period', yaxis_title='Sold Mileage',
                          xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          xaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          yaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                          width=500, height=400, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 3.3: Sold Engine Info ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col3:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Sold EngineSize Info</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    # Convert the 'Sold_engineSize info' data to a DataFrame and filter by selected_period
    engineSize_df = pd.DataFrame(data["Sold_engine size info"]).T
    # Filter the DataFrame to only show data for the selected period
    if selected_period in engineSize_df.index:
        filtered_engineSize_df = engineSize_df.loc[[selected_period]]
    else:
        filtered_engineSize_df = pd.DataFrame()  # Create an empty DataFrame if no data for selected_period
    # Only plot if there is data for the selected period
    if not filtered_engineSize_df.empty:
        filtered_engineSize_df = handle_missing_data(filtered_engineSize_df, ['avg deactive engineSize', 'min deactive engineSize', 'max deactive engineSize'])
        fig = go.Figure()

        # Add bars for avg, min, and max deactive engineSize 
        fig.add_trace(go.Bar(x=filtered_engineSize_df.index, y=filtered_engineSize_df['avg deactive engineSize'], 
                             name='Avg Deactive EngineSize', marker_color='lightblue',
                             hovertemplate='Avg: %{y:.2f}<extra></extra>',
                             text=filtered_engineSize_df['avg deactive engineSize'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_engineSize_df.index, y=filtered_engineSize_df['min deactive engineSize'],
                             name='Min Deactive EngineSize', marker_color='lightgreen',
                             hovertemplate='Min: %{y:.2f}<extra></extra>',
                             text=filtered_engineSize_df['min deactive engineSize'].apply(format_text),
                             textposition='outside'))
        
        fig.add_trace(go.Bar(x=filtered_engineSize_df.index, y=filtered_engineSize_df['max deactive engineSize'],
                             name='Max Deactive EngineSize', marker_color='lightcoral',
                             hovertemplate='Max: %{y:.2f}<extra></extra>',
                             text=filtered_engineSize_df['max deactive engineSize'].apply(format_text),
                             textposition='outside'))

        # Update layout
        fig.update_layout(xaxis_title='Time Period', yaxis_title='Sold EngineSize',
                          xaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          yaxis_title_font=dict(family='Times New Roman', size=16, color='black', weight='bold'),
                          xaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          yaxis_tickfont=dict(family='Times New Roman', size=14, color='black', weight='bold'),
                          font=dict(family='Times New Roman', size=14), barmode='group', xaxis_tickangle=0,
                          width=750, height=400, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 4: Sold Top 5 Expensive & Cheap Makes and Models ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-10px;">Top 5 Sold Expensive & Cheap Makes and Models</p>', unsafe_allow_html=True)
st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
def create_period_dataframe(data_dict, selected_period):
    period_data = data_dict.get(selected_period, {})
    if period_data:  # Check if there is data for the selected period
        df = pd.DataFrame.from_dict(period_data, orient='index').reset_index()
        df.columns = ['Make/Model', 'Value']  # Rename columns for clarity
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data for the period

# Create DataFrames for the selected period
expensive_makes_df = create_period_dataframe(data.get("Sold_Top 5 expensive makes", {}), selected_period)
cheap_makes_df = create_period_dataframe(data.get("Sold_Top 5 cheap makes", {}), selected_period)
expensive_models_df = create_period_dataframe(data.get("Sold_Top 5 expensive make models", {}), selected_period)
cheap_models_df = create_period_dataframe(data.get("Sold_Top 5 cheap make models", {}), selected_period)

# Combine all DataFrames into one
combined_df = pd.DataFrame({
    'Expensive Make': expensive_makes_df['Make/Model'] if not expensive_makes_df.empty else [None] * 5,
    'Expensive Make Value': expensive_makes_df['Value'] if not expensive_makes_df.empty else [None] * 5,
    'Cheap Make': cheap_makes_df['Make/Model'] if not cheap_makes_df.empty else [None] * 5,
    'Cheap Make Value': cheap_makes_df['Value'] if not cheap_makes_df.empty else [None] * 5,
    'Expensive Model': expensive_models_df['Make/Model'] if not expensive_models_df.empty else [None] * 5,
    'Expensive Model Value': expensive_models_df['Value'] if not expensive_models_df.empty else [None] * 5,
    'Cheap Model': cheap_models_df['Make/Model'] if not cheap_models_df.empty else [None] * 5,
    'Cheap Model Value': cheap_models_df['Value'] if not cheap_models_df.empty else [None] * 5})

if not combined_df.empty:
    # Convert the combined DataFrame to HTML
    combined_html_table = combined_df.to_html(classes='mystyle', escape=False, index=False)
    # CSS styling for table
    st.markdown("""
        <style>
        .mystyle {
            font-family: 'Times New Roman', Times, serif;
            border-collapse: collapse;
            width: 100%;
        }
        .mystyle th, .mystyle td {
            border: 1px solid black;
            padding: 10px;
        }
        .mystyle thead th {
            background-color: lavender;
            font-weight: bold;
        }
        .mystyle tbody td {
            background-color: lightgrey;
        }
        .scrollable-table {
            max-height: 412px;
            overflow-y: auto;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="scrollable-table">{combined_html_table}</div>', unsafe_allow_html=True)
else:
    st.write("No data available for the selected period.")


# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 5: Sold Top 5 Cities ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Sold Top 5 Cities</p>', unsafe_allow_html=True)
st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
# Filter data for the selected period
sold_top_cities_for_selected_period = data["Sold_Top 5 cities"].get(selected_period, {})

if sold_top_cities_for_selected_period:  # Check if data exists for the selected period
    df_cities = pd.DataFrame(list(sold_top_cities_for_selected_period.items()), columns=["City", "Count"])
    
    # Create a bar chart for the selected period
    fig = px.bar(df_cities, x='City', y='Count', labels={'City': '', 'Count': 'Count'})
    fig.update_layout(font=dict(family="Times New Roman", size=16),
                        xaxis=dict(tickfont=dict(family="Times New Roman", size=16, color="black", weight="bold")),  # Make x-axis ticks bold
                        yaxis=dict(tickfont=dict(family="Times New Roman", size=16, color="black", weight="bold")),
                        height=510, width=1200, showlegend=False, margin=dict(t=0, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write(f"No data available for the selected period")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 6: Sold Fuel Types, Body Types, and Gearbox ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2, col3 = st.columns([1,1,1])



# Function to create a pie chart with labels positioned on the right side
def create_pie_chart(data_dict, chart_title, hole_size=0.2):
    if not data_dict:
        return go.Figure()  # Return an empty figure if no data is available
    
    # Convert data to DataFrame
    df = pd.DataFrame(list(data_dict.items()), columns=['Type', 'Count'])
    # Ensure DataFrame is not empty and handle zero counts
    if df.empty:
        return go.Figure()
    
    fig = go.Figure(data=[go.Pie(labels=df['Type'], values=df['Count'], hole=hole_size, textinfo='label+percent', 
                                 insidetextorientation='radial', marker=dict(line=dict(color='black', width=2)),
                                 name=chart_title, showlegend=True, legendgroup=chart_title)])
    
    # Adjust layout to position labels to the right
    fig.update_layout(font=dict(family="Times New Roman", size=14, color="black"), margin=dict(l=0, r=0, t=0, b=0),
                      legend=dict(orientation="v", yanchor="top", xanchor="left", x=1.05, y=1), height=400, width=400)
    return fig

# Filter data for the selected period
gearbox_data = data["Sold_Top 5 gearbox"].get(selected_period, {})
fuel_types_data = data["Sold_Top 5 fuel types"].get(selected_period, {})
body_types_data = data["Sold_Top 5 body types"].get(selected_period, {})

# Create pie charts for each category with a specific hole size
fig_gearbox = create_pie_chart(gearbox_data, 'Sold Top Gearbox Types', hole_size=0.3)
fig_fuel_types = create_pie_chart(fuel_types_data, 'Sold Top Fuel Types', hole_size=0.5)
fig_body_types = create_pie_chart(body_types_data, 'Sold Top Body Types', hole_size=0.3)



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 6.1: Sold Fuel Types ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Sold Fuel Types</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    if fuel_types_data:
        st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
        st.plotly_chart(fig_fuel_types, use_container_width=False)
    else:
        st.write("No data available for Sold Fuel Types")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 6.2: Sold Body Types ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Sold Body Types</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    if body_types_data:
        st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
        st.plotly_chart(fig_body_types, use_container_width=False)
    else:
        st.write("No data available for Sold Body Types")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 6.3: Sold Gearbox ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col3:
    st.markdown('<p style="font-family:Times New Roman; font-size:20px; font-weight:bold; margin-bottom:-30px;">Sold Gearbox</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
    if gearbox_data:
        st.markdown('<div style="height:5px;"></div>', unsafe_allow_html=True)
        st.plotly_chart(fig_gearbox, use_container_width=False)
    else:
        st.write("No data available for Sold Body Gearbox")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section 7: Sold New Cars Count by Week Days and Months ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns(2)


# Filter data by the selected period
weekdays_data = data.get("Sold_Week days new cars count", {}).get(selected_period, {})
months_data = data.get("Sold_Week new cars count", {}).get(selected_period, {})

# Ensure all days and months are represented in the DataFrames
all_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
all_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Create DataFrames with zero counts included
weekdays_df = pd.DataFrame({day: [weekdays_data.get(day, 0)] for day in all_weekdays}).T
months_df = pd.DataFrame({month: [months_data.get(month, 0)] for month in all_months}).T

def create_custom_line_chart(df, width, height):
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

    fig.update_layout(font=dict(family="Times New Roman", size=14), xaxis_tickangle=-45, title_font_size=16,
                      title_font=dict(family="Times New Roman", weight="bold"), autosize=False, width=width,
                      height=height, legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.05),
                      plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(showgrid=True, gridcolor='lightgrey',
                                 tickfont=dict(family="Times New Roman", size=18, color='black', weight='bold')),
                                 yaxis=dict(showgrid=True, gridcolor='lightgrey',
                                            tickfont=dict(family="Times New Roman", size=12, color='black', weight='bold')))
    return fig



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 7.1: Sold New Cars Count by Week Days  ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown("<h3 style='font-family: Times New Roman; font-weight: bold; font-size: 20px;'>Sold New Cars Count by Week Days</h3>", unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    if not weekdays_df.empty:
        weekdays_chart = create_custom_line_chart(weekdays_df, width=400, height=550)
        st.plotly_chart(weekdays_chart, use_container_width=True)
    else:
        st.write("No data available for Sold new cars count by week days.")



# ------------------------------------------------------------------------------------------------------------------
# --------------------------------- Section/Column 7.2: Sold New Cars Count by Months ---------------------------
# ------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown("<h3 style='font-family: Times New Roman; font-weight: bold; font-size: 20px;'>Sold New Cars Count by Months</h3>", unsafe_allow_html=True)
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    if not months_df.empty:
        months_chart = create_custom_line_chart(months_df, width=400, height=550)
        st.plotly_chart(months_chart, use_container_width=True)
    else:
        st.write("No data available for Sold new cars count by months.")








# --------------------------------- Sold Cars Section End ---------------------------------
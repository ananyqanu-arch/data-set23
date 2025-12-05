import streamlit as st
import pandas as pd
import altair as alt

# Assuming df is already loaded and prepared with 'Price_Category' and 'Rating_Category'
# If running this cell independently, ensure df is available or load it again.

# Set the title of the Streamlit application
st.title('Swiggy Data Analysis Dashboard')
df=pd.read_csv('swiggy (1).csv')
# Add a sidebar for interactive filters
st.sidebar.title('Filter Options')

# City Filter
selected_cities = st.sidebar.multiselect(
    'Select City',
    options=df['City'].unique(),
    default=list(df['City'].unique())
)

# Area Filter (dependent on selected cities)
# Filter areas based on selected cities first to ensure valid options
available_areas = df[df['City'].isin(selected_cities)]['Area'].unique()
selected_areas = st.sidebar.multiselect(
    'Select Area',
    options=available_areas,
    default=list(available_areas)
)

# Average Rating Filter
min_rating, max_rating = st.sidebar.slider(
    'Select Average Rating Range',
    min_value=float(df['Avg ratings'].min()),
    max_value=float(df['Avg ratings'].max()),
    value=(float(df['Avg ratings'].min()), float(df['Avg ratings'].max()))
)

# Delivery Time Filter
min_delivery_time, max_delivery_time = st.sidebar.slider(
    'Select Delivery Time Range (minutes)',
    min_value=int(df['Delivery time'].min()),
    max_value=int(df['Delivery time'].max()),
    value=(int(df['Delivery time'].min()), int(df['Delivery time'].max()))
)

# Apply filters to the DataFrame
filtered_df = df[
    (df['City'].isin(selected_cities)) &
    (df['Area'].isin(selected_areas)) &
    (df['Avg ratings'] >= min_rating) &
    (df['Avg ratings'] <= max_rating) &
    (df['Delivery time'] >= min_delivery_time) &
    (df['Delivery time'] <= max_delivery_time)
]

# Create main sections for visualizations
st.header('Data Visualizations')

if not filtered_df.empty:
    st.write(f"Displaying data for {len(filtered_df)} restaurants after filtering.")

    # Visualization 1: Restaurant Count by City
    st.subheader('Restaurant Count by City')
    city_counts = filtered_df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Count']
    chart_city = alt.Chart(city_counts).mark_bar().encode(
        x=alt.X('City', sort='-y'),
        y='Count',
        tooltip=['City', 'Count']
    ).properties(title='Number of Restaurants per City')
    st.altair_chart(chart_city, use_container_width=True)

    # Visualization 2: Average Ratings Distribution
    st.subheader('Average Ratings Distribution')
    rating_counts = filtered_df['Rating_Category'].value_counts().reset_index()
    rating_counts.columns = ['Rating Category', 'Count']
    chart_ratings = alt.Chart(rating_counts).mark_bar().encode(
        x=alt.X('Rating Category', sort=['Excellent', 'Very Good', 'Good', 'Fair', 'Poor']),
        y='Count',
        tooltip=['Rating Category', 'Count']
    ).properties(title='Distribution of Average Ratings')
    st.altair_chart(chart_ratings, use_container_width=True)

    # Visualization 3: Delivery Time Distribution
    st.subheader('Delivery Time Distribution')
    chart_delivery = alt.Chart(filtered_df).mark_bar().encode(
        alt.X('Delivery time', bin=True),
        alt.Y('count()', title='Number of Restaurants'),
        tooltip=['Delivery time', 'count()']
    ).properties(title='Distribution of Delivery Times')
    st.altair_chart(chart_delivery, use_container_width=True)

    # Visualization 4: Average Price by City
    st.subheader('Average Price by City')
    avg_price_city = filtered_df.groupby('City')['Price'].mean().reset_index()
    chart_avg_price = alt.Chart(avg_price_city).mark_bar().encode(
        x=alt.X('City', sort='-y'),
        y='Price',
        tooltip=['City', 'Price']
    ).properties(title='Average Price per City')
    st.altair_chart(chart_avg_price, use_container_width=True)

else:
    st.write("No data available for the selected filters to display visualizations.")

# Create a section for the summary report
st.header('Summary Report')
if not filtered_df.empty:
    st.write("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Restaurants", value=len(filtered_df))
    with col2:
        st.metric(label="Average Rating", value=f"{filtered_df['Avg ratings'].mean():.2f}")
    with col3:
        st.metric(label="Average Price", value=f"₹{filtered_df['Price'].mean():.2f}")

    st.write("### Top 5 Restaurants by Average Rating (for selected filters)")
    top_rated = filtered_df.sort_values(by='Avg ratings', ascending=False).head(5)
    st.dataframe(top_rated[['Restaurant', 'City', 'Area', 'Avg ratings', 'Total ratings']])

    st.write("### Insights")
    st.markdown(f"- The dashboard currently displays data for **{len(selected_cities)}** cities and **{len(selected_areas)}** areas.")
    st.markdown(f"- Restaurants with ratings between **{min_rating:.1f}** and **{max_rating:.1f}** are considered.")
    st.markdown(f"- Delivery times considered are between **{min_delivery_time}** and **{max_delivery_time}** minutes.")
    st.markdown(f"- The city with the most restaurants among the filtered data is **{city_counts.iloc[0]['City']}** with **{city_counts.iloc[0]['Count']}** restaurants.")
    st.markdown(f"- The highest average price among filtered cities is in **{avg_price_city.iloc[avg_price_city['Price'].idxmax()]['City']}** with an average of **₹{avg_price_city['Price'].max():.2f}**.")


else:
    st.write('No data available for the selected filters to generate a summary report.')

# Display a sample of the filtered data
st.subheader('Filtered Data Sample')
st.write(filtered_df.head())

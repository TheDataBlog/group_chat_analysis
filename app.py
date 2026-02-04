import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import json

st.set_page_config(page_title='chat analysis', layout='wide')

st.info(
    "ℹ️ Note: This app analyzes group chat communication patterns. "
    "All user identifiers and personal information have been anonymized "
    "to ensure privacy and responsible data handling."
)

per_person_sum = pd.read_csv('files/per_person_sum.csv')

# Make sure columns are named correctly
# CSV should have 'person' and 'messages' columns
chart_df = per_person_sum.copy()

# Create Altair bar chart
chart = (
    alt.Chart(chart_df)
    .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
    .encode(
        x=alt.X('person:N', sort='-y', title='Person'),
        y=alt.Y('count:Q', title='Number of messages'),
        tooltip=['person', 'count'],
        color=alt.Color('count:Q', scale=alt.Scale(scheme='blues'))
    )
    .properties(
        title='Who talks the most',
        height=600
    )
)

st.altair_chart(chart, use_container_width=True)

group1 = pd.read_csv('files/group1.csv')
group2 = pd.read_csv("files/group2.csv")

# Ensure 'date' is a datetime type
group1['date'] = pd.to_datetime(group1['date'])
group2['date'] = pd.to_datetime(group2['date'])

# Chart for top 7 people (group1)
chart1 = (
    alt.Chart(group1)
    .mark_line()
    .encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('cumulative_person:Q', title='Total Messages'),
        color=alt.Color('person:N', title='Person'),
        tooltip=['person:N', 'date:T', 'cumulative_person:Q']
    )
    .properties(
        title='Chat Growth Over Time for Top 7 People',
        height=500
    )
    .interactive()
)

st.altair_chart(chart1, use_container_width=True)

# Chart for the rest of the people (group2)
chart2 = (
    alt.Chart(group2)
    .mark_line()
    .encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('cumulative_person:Q', title='Total Messages'),
        color=alt.Color('person:N', title='Person'),
        tooltip=['person:N', 'date:T', 'cumulative_person:Q']
    )
    .properties(
        title='Chat Growth Over Time for Other Members',
        height=500
    )
    .interactive()
)

st.altair_chart(chart2, use_container_width=True)

replied_per_person = pd.read_csv('files/replied_per_person.csv')

sort_order = alt.SortField(field="ignored", order="descending")

# Bars


# Show a warning if missing messages affect results
st.warning(
    "⚠️ Some users have missing chat history due to deleted messages. "
    "This may cause the 'gets ignored' metric to appear higher than actual."
)

bars = (
    alt.Chart(replied_per_person)
    .mark_bar()
    .encode(
        x=alt.X('person:N', sort=sort_order, title='Person'),
        y=alt.Y('ignored:Q', title='Percentage'),
        tooltip=[
            alt.Tooltip('person:N', title='Person'),
            alt.Tooltip('ignored:Q', title='Ignored (%)', format='.1f')
        ],
        color=alt.Color('ignored:Q', scale=alt.Scale(scheme='reds'))
    )
    .properties(
        title='Who gets ignored the most',
        height=700
    )
)

# Labels (IMPORTANT: same sort)
labels = (
    alt.Chart(replied_per_person)
    .mark_text(dy=-5)
    .encode(
        x=alt.X('person:N', sort=sort_order),
        y='ignored:Q',
        text=alt.Text('ignored:Q', format='.1f')
    )
)

chart = bars + labels


st.altair_chart(chart + labels, use_container_width=True)
most_reply_count = pd.read_csv('files/most_reply_count.csv')

# Display as a DataFrame in Streamlit
st.subheader("Top Reply Pairs")
st.dataframe(
    most_reply_count[['person', 'replied_to', 'count']].rename(
        columns={
            'person': 'Person',
            'replied_to': 'Replied To',
            'count': 'Number of Replies'
        }
    )
)

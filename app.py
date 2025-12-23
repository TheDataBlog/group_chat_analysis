import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title='chat analysis', layout='wide')

json_file = st.file_uploader(
    label='Enter the JSON file here',
    type='json'
)

if json_file is not None:
    df = pd.read_json(json_file)

    df_messages = pd.json_normalize(df['messages'])
    messages = df_messages[df_messages['type'] == 'message'].copy()

    messages = messages.rename(columns={'from': 'person'})
    messages['date'] = pd.to_datetime(messages['date'])

    per_person_sum = messages['person'].value_counts()

    chart_df = per_person_sum.reset_index()
    chart_df.columns = ['person', 'messages']

    chart = (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X('person:N', sort='-y', title='Person'),
            y=alt.Y('messages:Q', title='Number of messages'),
            tooltip=['person', 'messages'],
            color=alt.Color('messages:Q', scale=alt.Scale(scheme='blues'))
        )
        .properties(
            title='Who talks the most',
            height=600
        )
    )

    st.altair_chart(chart, use_container_width=True)


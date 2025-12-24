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

    date_groups = messages.groupby(by = [messages['date'].dt.date, 
                                         messages['person']]).agg(count=('person','count'))
    date_groups = date_groups.reset_index()
    date_groups = date_groups.sort_values(['person','date'])
    date_groups['cumulative_person'] = date_groups.groupby('person')['count'].cumsum()

    group1 = date_groups[date_groups['person'].isin(per_person_sum.head(7).index)]
    group2 = date_groups[~date_groups['person'].isin(per_person_sum.head(7).index)]

    chart = (
        alt.Chart(group1)
        .mark_line()
        .encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('cumulative_person:Q', title='Total Messages'),
            color=alt.Color('person:N', title='Person'),
            tooltip=['person:N', 'date:T', 'cumulative_person:Q']
        )
        .properties(
            title='Chat Growth Over Time for Each Person',
            height=500
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    chart = (
    alt.Chart(group2)
    .mark_line()
    .encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('cumulative_person:Q', title='Total Messages'),
        color=alt.Color('person:N', title='Person'),
        tooltip=['person:N', 'date:T', 'cumulative_person:Q']
    )
    .properties(
        title='Chat Growth Over Time for Each Person',
        height=500
    )
    .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    messages = messages.merge(messages[['id','person']], 
                              how='left', left_on='reply_to_message_id', 
                              right_on='id', suffixes=('', '_replied'))
    
    replied_per_person = messages['person_replied'].value_counts()
    replied_per_person = pd.DataFrame(replied_per_person)
    per_person_sum = pd.DataFrame(per_person_sum)
    replied_per_person = replied_per_person.merge(right=per_person_sum, 
                                                  how='inner',left_index=True,
                                                  right_on='person', suffixes=('','_add'))


    replied_per_person['percentage'] = round((replied_per_person['count'] / replied_per_person['count_add']) * 100, 1)
    replied_per_person['ignored'] = 100 - replied_per_person['percentage']

    replied_per_person = replied_per_person.sort_values('ignored', ascending=False)
    replied_per_person = replied_per_person.reset_index()

    replied_per_person = replied_per_person.reset_index()

    chart = (
        alt.Chart(replied_per_person)
        .mark_bar()
        .encode(
            x=alt.X('person:N',sort='y', title='Person'),
            y=alt.Y('ignored:Q', title='Percentage'),
            tooltip=[
                alt.Tooltip('person:N', title='Person'),
                alt.Tooltip('ignored:Q', title='Ignored (%)', format='.1f')
            ]
        )
        .properties(
            title='Percentage of Messages Ignored for Each Person',
            height=700
        )
    )

    labels = (
        alt.Chart(replied_per_person)
        .mark_text(dy=-5)
        .encode(
            x='person:N',
            y='ignored:Q',
            text=alt.Text('ignored:Q', format='.1f')
        )
    )

    st.altair_chart(chart + labels, use_container_width=True)

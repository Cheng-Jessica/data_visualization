#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import holoviews as hv
import hvplot.pandas
import panel as pn
pn.extension()

import warnings
warnings.filterwarnings('ignore')

data_df = pd.read_csv('kickstarter.csv')
data_df.head()

# Change the format to datetime
data_df["launched"] = pd.to_datetime(data_df["launched"])
data_df["deadline"] = pd.to_datetime(data_df["deadline"])

# Generate new columns
data_df["launch_year"] = data_df["launched"].dt.year
data_df["launch_month"] = data_df["launched"].dt.month

## Remove the noisy data from the DataFrame
data_df = data_df[data_df["launch_year"] > 1970]

# Create widgets for filtering
country_radio_button = pn.widgets.RadioButtonGroup(name='Country', options=['US', 'FR', 'GB'], value='US')
year_slider = pn.widgets.IntSlider(name='Year', start=int(data_df['launch_year'].min()), end=int(data_df['launch_year'].max()), value=int(data_df['launch_year'].min()))
visualization_radio_button = pn.widgets.RadioButtonGroup(name='Visualization', options=['Projects', 'Success Projects'], value='Projects')

# Define a function to update the chart based on widget values
def update_chart(selected_country, selected_year, selected_visualization):
    filtered_data = data_df[(data_df['country'] == selected_country) & (data_df['launch_year'] == selected_year)]

    if selected_visualization == 'Success Projects':
        filtered_data = filtered_data[filtered_data['state'] == 'successful']

    counts = filtered_data.groupby('launch_month').size()
    chart = hv.Curve((counts.index, counts.values), label='Count', kdims=['Month'], vdims=['Count'])
    return chart.opts(title='Project Counts by Month', xlabel='Month', ylabel='Count', width=800)

# Create a Panel app using pn.interact
dashboard = pn.interact(update_chart, selected_country=country_radio_button, selected_year=year_slider, selected_visualization=visualization_radio_button)

# Show the dashboard in the Jupyter Notebook
dashboard.servable()

import panel as pn
pn.serve(dashboard, port=5007)

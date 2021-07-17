#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from bokeh.models.layouts import Column
from bokeh.palettes import Category20_16
from bokeh.models import (Select, MultiSelect, Panel,
                        CheckboxGroup, HoverTool,
                        ColumnDataSource, FuncTickFormatter)
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.transform import dodge
import pandas as pd
import numpy as np
import math

Category20_16 = list(Category20_16)
Category20_16.sort()

def creating_tab_1(df_transfers, substances, countries,
                   waste_managements, years):
    '''
    Fuction to make the fist tab for the dashboard
    '''

    # Countries and their colors
    postions = [-0.25, 0.0, 0.25]
    country_colors = {country: Category20_16[i] for i, country in enumerate(countries)}

    def make_dataset(initial_wm,
                    opt_substance='50000 : Formaldehyde',
                    opt_countries=['USA']):

        columns = ['reporting_year','country', 'total_transfer_amount_kg']

        # Selecting substance
        df_to_plot = df_transfers[df_transfers['generic_substance'] == opt_substance]
        
        # Selecting waste management
        df_to_plot = df_to_plot[df_to_plot['transfer_class_wm_hierarchy_name'].isin(initial_wm)]

        # Selecting countries
        df_to_plot = df_to_plot[df_to_plot['country'].isin(opt_countries)]

        # Keeping desired columns
        df_to_plot = df_to_plot[columns]
        df_to_plot.reset_index(inplace=True, drop=True)

        # Pivot table
        table = pd.pivot_table(df_to_plot,
            values='total_transfer_amount_kg', index=['reporting_year'],
                    columns=['country'], aggfunc=np.sum, fill_value=0)

        # Compliting columns
        for country in countries:
            if not country in table.columns:
                table[country] = 0.00

        # Compliting rows
        for year in years:
            if not year in table.index:
                table.loc[country] = [0.0]*len(table.columns)

        # Reset indexes
        table.reset_index(inplace=True)

        
        src = ColumnDataSource(data=table)


        return src


    def make_plot(src):

        # Blank plot with correct labels
        plot = figure(
                    x_range=src.data['reporting_year'],
                    title='Total transfer amount reported by country',
                    y_axis_label='Total transfer amount [kg/yr]',
                    x_axis_label='Reporting year',
                    tools='wheel_zoom,pan,box_zoom,reset,save',
                    sizing_mode="stretch_both"
                    )

        stacked_countries = [col for col in src.data.keys() if col in country_colors.keys()]

        for i, stacked_country in enumerate(stacked_countries):
            plot.vbar(x=dodge('reporting_year', postions[i], range=plot.x_range),
                    top=stacked_country, width=0.2, source=src,
                    color=country_colors[stacked_country],
                    hover_fill_color=country_colors[stacked_country],
                    legend_label=stacked_country,
                    hover_fill_alpha=1.0,
                    fill_alpha=0.7,
                    muted_color=country_colors[stacked_country],
                    muted_alpha=0.2)

        # Hover tool with vline mode
        TOOLTIPS = [('Reporting year', '@reporting_year'),
                    ('Total transfer amount [kg]', '$y{0,0.000}')]
        hover = HoverTool(tooltips=TOOLTIPS,
						  mode='vline')

        plot.add_tools(hover)

        # Styling
        plot = style(plot)

        return plot


    def update(attr, old, new):
        wm_to_plot = [wm_checkbox.labels[i] for i in wm_checkbox.active]

        new_src = make_dataset(wm_to_plot,
                    opt_substance=substance_selector.value,
                    opt_countries=country_selector.value)

        src.data.update(new_src.data)

        plot = make_plot(src)


    def style(plot):
        # Title 
        plot.title.align = 'center'
        plot.title.text_font_size = '20pt'
        plot.title.text_font = 'serif'

        # Axis titles
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_style = 'bold'
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        plot.xaxis.major_label_text_font_size = '12pt'
        plot.xaxis.major_label_orientation = math.pi/2
        plot.yaxis.major_label_text_font_size = '12pt'
        plot.yaxis.formatter = FuncTickFormatter(code='''
                                            if (tick < 1e3){
                                                var unit = ''
                                                var num =  (tick).toFixed(2)
                                              }
                                              else if (tick < 1e6){
                                                var unit = 'k'
                                                var num =  (tick/1e3).toFixed(2)
                                              }
                                              else{
                                                var unit = 'm'
                                                var num =  (tick/1e6).toFixed(2)
                                                }
                                            return `${num} ${unit}`
                                           ''')

        plot.x_range.range_padding = 0.1
        plot.xgrid.grid_line_color = None
        plot.legend.location = "top_left"
        plot.legend.orientation = "horizontal"
        plot.legend.click_policy="mute"
        plot.background_fill_color = "white"
        
        return plot


    # Establishing country multi-selector
    country_selector = MultiSelect(title="Country:",
                            value=countries,
                            options=countries,
                            sizing_mode="stretch_width")
    country_selector.on_change('value', update)

    # Establishing substance selector
    substance_selector = Select(title="Generic substance:",
                            value=substances[0],
                            options=substances,
                            sizing_mode="stretch_width")
    substance_selector.on_change('value', update)

    # Establishing wm selector
    wm_checkbox = CheckboxGroup(labels=waste_managements,
                            active=list(range(len(waste_managements))),
                            sizing_mode="stretch_both",
                            name='Waste management activity')
    wm_checkbox.on_change('active', update)

    # Initial transfers and data source
    initial_wm = [wm_checkbox.labels[i] for i in wm_checkbox.active]
    src = make_dataset(initial_wm,
                    opt_substance=substance_selector.value,
                    opt_countries=country_selector.value)
    plot = make_plot(src)


    # Put controls in a single element
    controls = row(country_selector,
                        substance_selector,
                        wm_checkbox)

    # Create a row layout
    layout = Column(controls, plot, sizing_mode="stretch_both")


    # Make a tab with the layout 
    tab = Panel(child=layout, title='Tab 1')

    return tab
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from bokeh.models.layouts import Column
from bokeh.palettes import Blues
from bokeh.models import (Panel, Select, CheckboxGroup, RangeSlider,
                        ColumnDataSource, HoverTool,
                        LinearColorMapper, BasicTicker, ColorBar)
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.transform import transform, dodge
import numpy as np
import math

palette = list(Blues[256])
palette.reverse()

def creating_tab_3(df_transfers, substances, countries, years):
    '''
    Fuction to make the third tab for the dashboard
    '''

    def make_dataset(opt_year,
                    opt_substance='50000 : Formaldehyde',
                    opt_countries=['USA']):

        columns = ['reporting_year','country', 'total_transfer_amount_kg',
                    'number_of_facilities', 'generic_transfer_class']
        
        # Selecting substance
        df_to_plot = df_transfers[df_transfers['generic_substance'] == opt_substance]

        # Selecting countries
        df_to_plot = df_to_plot[df_to_plot['country'].isin(opt_countries)]

        # Selecting years
        opt_year = [str(year) for year in list(range(opt_year[0], opt_year[1] + 1))]
        df_to_plot = df_to_plot[df_to_plot['reporting_year'].isin(opt_year)]

        # Keeping desired columns
        columns = ['total_transfer_amount_kg','number_of_facilities', 'generic_transfer_class', 'generic_sector']
        df_to_plot = df_to_plot[columns]


        # Suming
        df_to_plot =  df_to_plot.groupby(['generic_transfer_class', 'generic_sector'], as_index=False).sum()
        df_to_plot['generic_transfer_class_number'] = df_to_plot['generic_transfer_class'].str.extract(r'(M[0-9]{1,2})')
        df_to_plot['generic_sector_number'] = df_to_plot['generic_sector'].str.extract(r'([0-9]{1,2})')
        df_to_plot.sort_values(by='generic_sector_number', inplace=True)
        df_to_plot = df_to_plot[df_to_plot['total_transfer_amount_kg'] != 0]
        df_to_plot['total_transfer_amount_kg_log'] = df_to_plot['total_transfer_amount_kg'].apply(lambda x: np.log(x))

        # Reset indexes
        df_to_plot.reset_index(inplace=True, drop=True)

        src = ColumnDataSource(data=df_to_plot)

        return src

    def make_plot(src):

        x_range = [int(x) for x in set(src.data['generic_sector_number'])]
        x_range.sort()
        x_range = [str(x) for x in x_range]

        plot = figure(title='Relationship between industry sector and transfer class',
                    tools='wheel_zoom,pan,box_zoom,reset,save',
                    sizing_mode="stretch_both",
                    x_range=x_range,
                    y_range=list(set(src.data['generic_transfer_class_number'])),
                    y_axis_label='Generic transfer class',
                    x_axis_label='Generic industry sector',
                    y_axis_location="right",
                    )

        # Add legend
        mapper = LinearColorMapper(palette=palette,
                                    low=min(src.data['total_transfer_amount_kg_log']),
                                    high=max(src.data['total_transfer_amount_kg_log'])
                                    )

        rectwidth = 1
        plot.rect(y='generic_transfer_class_number',
                x=dodge('generic_sector_number', 0, range=plot.x_range),
                width=rectwidth, height=rectwidth, source=src,line_color=None,
                fill_color=transform('total_transfer_amount_kg_log', mapper))

        # Hover tool with vline mode
        TOOLTIPS = [
                    ('Generic transfer class', '@generic_transfer_class'),
                    ('Generic industry sector', '@generic_sector'),
                    ('N° records', '@number_of_facilities{0,0}'),
                    ('Total transfer amount [kg/yr]', '@total_transfer_amount_kg{0,0}')
                    ]
        hover = HoverTool(tooltips=TOOLTIPS,
						  mode='mouse')
        plot.add_tools(hover)

        # Styling
        plot = style(plot)

         # Add color bar
        color_bar = ColorBar(
                color_mapper=mapper,
                location=(0, 0),
                ticker=BasicTicker(desired_num_ticks=10),
                title='ln[total kgs transferred]',
                title_text_align='left',
                title_text_font_size='14pt',
                title_text_font_style='bold',
                title_standoff=12,
                label_standoff=12,
                major_tick_line_color='black',
                major_label_text_font_size='10pt',
                bar_line_color='black',
                )
        plot.add_layout(color_bar, 'left')

        return plot

    def update_data(attr, old, new):
        
        new_src = make_dataset(year_rangeslider.value,
                    opt_substance=substance_selector.value,
                    opt_countries=[country_checkbox.labels[i] for i in country_checkbox.active])

        src.data.update(new_src.data)

        plot = make_plot(src)

    def style(plot):
        # Title 
        plot.title.align = 'center'
        plot.title.text_font_size = '20pt'
        plot.title.text_font = 'serif'

        # Axis titles
        plot.axis.axis_line_color = 'black'
        plot.axis.major_label_standoff = 0
        plot.axis.major_tick_line_color = 'black'
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.major_label_text_font_size = '10pt'
        plot.xaxis.axis_label_standoff = 12
        plot.xaxis.major_label_standoff = 12
        plot.xaxis.axis_label_text_font_style = 'bold'
        plot.xaxis.major_label_orientation = math.pi / 2
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.major_label_text_font_size = '10pt'
        plot.yaxis.axis_label_standoff = 12
        plot.yaxis.major_label_standoff = 12
        plot.yaxis.axis_label_text_font_style = 'bold'
        plot.grid.grid_line_color = None

        plot.background_fill_color = "beige"
        plot.background_fill_alpha = 0.6

        return plot


    # Establishing substance selector
    substance_selector = Select(title="Generic substance:",
                            value=substances[0],
                            options=substances,
                            sizing_mode="stretch_width")
    substance_selector.on_change('value', update_data)

    # Establishing year selector
    year_rangeslider = RangeSlider(
                            start=int(min(years)),
                            end=int(max(years)),
                            step=1,
                            value=tuple([int(min(years)), int(max(years))]),
                            sizing_mode="stretch_width",
                            title='Reporting year')
    year_rangeslider.on_change('value', update_data)

    # Establishing country selector
    country_checkbox = CheckboxGroup(labels=countries,
                            active=list(range(len(countries))),
                            sizing_mode="stretch_both",
                            name='Country')
    country_checkbox.on_change('active', update_data)

    # Initial transfers and data source
    src = make_dataset(year_rangeslider.value,
                    opt_substance=substance_selector.value,
                    opt_countries=[country_checkbox.labels[i] for i in country_checkbox.active])
                    
    plot = make_plot(src)

     # Put controls in a single element
    controls = row(substance_selector,
                year_rangeslider,
                country_checkbox)

    # Create a row layout
    layout = Column(controls, plot, sizing_mode="stretch_both")

    # Make a tab with the layout
    tab = Panel(child=layout, title='Heatmap')

    return tab
    

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from bokeh.models.layouts import Column
from bokeh.palettes import mpl
from bokeh.models import (Panel, Select, CheckboxGroup, RangeSlider,
                        ColumnDataSource, HoverTool, Label,
                        LinearColorMapper, BasicTicker, ColorBar)
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.transform import transform
import numpy as np
import math


palette = mpl["Plasma"][256]

def creating_tab_3(df_transfers, substances, countries,
                transfer_classes, years, industry_sectors):
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
        df_to_plot['generic_sector_number'] = df_to_plot['generic_sector'].str.extract(r'([0-9]{1,2})').astype(int)
        df_to_plot.sort_values(by='generic_sector_number', inplace=True)
        df_to_plot = df_to_plot[df_to_plot['total_transfer_amount_kg'] != 0]
        df_to_plot['total_transfer_amount_kg_log'] = df_to_plot['total_transfer_amount_kg'].apply(lambda x: np.log(x))
    
        # Reset indexes
        df_to_plot.reset_index(inplace=True, drop=True)

        src = ColumnDataSource(data=df_to_plot)

        return src

    def make_plot(src):

        x_range = list(set(src.data['generic_sector_number']))
        x_range.sort()
        x_range = list(str(x) for x in x_range)

        plot = figure(title='Relationship between industry sector and transfer class',
                    tools='wheel_zoom,pan,box_zoom,reset,save',
                    sizing_mode="stretch_both",
                    x_range=x_range,
                    y_range=list(x for x in set(src.data['generic_transfer_class_number'])),
                    y_axis_label='Generic transfer class',
                    x_axis_label='Generic industry sector',
                    )

        # Add legend
        mapper = LinearColorMapper(palette=palette,
                                    low=min(src.data['total_transfer_amount_kg_log']),
                                    high=max(src.data['total_transfer_amount_kg_log'])
                                    )
        color_bar = ColorBar(
                color_mapper=mapper,
                location=(0, 0),
                ticker=BasicTicker(desired_num_ticks=len(palette)),
                title='ln(total kgs transferred)',
                title_text_align='center',
                title_text_font_size='14pt',
                title_text_font_style='bold',
                label_standoff=12,
                border_line_color=None
                )
        plot.add_layout(color_bar, 'right')

        rectwidth = 0.9
        plot.rect(y='generic_transfer_class_number', x='generic_sector_number',
                width=rectwidth, height=rectwidth, source=src,
                line_width=1,
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
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_style = 'bold'
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.axis_label_text_font_style = 'bold'

        plot.grid.grid_line_color = None

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
    

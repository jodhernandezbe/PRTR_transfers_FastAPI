#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from bokeh.models.layouts import Column
from bokeh.palettes import Category20_16
from bokeh.models import (Panel, Select, CheckboxGroup, RangeSlider,
                        ColumnDataSource, HoverTool, Label)
from bokeh.layouts import row
from bokeh.plotting import figure
from math import pi

Category20_16 = list(Category20_16)

def creating_tab_2(df_transfers, substances, countries,
                        transfer_classes, years):
    '''
    Fuction to make the second tab for the dashboard
    '''

    transfer_classes.sort()
    transfer_class_colors = {transfer_class: Category20_16[i] for i, transfer_class in enumerate(transfer_classes)}

    def make_dataset(opt_year,
                    opt_substance='50000 : Formaldehyde',
                    opt_countries=['USA']):
        
        # Selecting substance
        df_to_plot = df_transfers[df_transfers['generic_substance'] == opt_substance]

        # Selecting countries
        df_to_plot = df_to_plot[df_to_plot['country'].isin(opt_countries)]

        # Selecting years
        opt_year = [str(year) for year in list(range(opt_year[0], opt_year[1] + 1))]
        df_to_plot = df_to_plot[df_to_plot['reporting_year'].isin(opt_year)]

        # Percentage
        column_sum = df_to_plot['number_of_facilities'].sum()
        df_to_plot['percentage'] = (df_to_plot['number_of_facilities']/column_sum)

        # Keeping desired columns
        columns = ['total_transfer_amount_kg','number_of_facilities', 'generic_transfer_class', 'percentage']
        df_to_plot = df_to_plot[columns]

        # Suming
        df_to_plot = df_to_plot.groupby(['generic_transfer_class'], as_index=False).sum()

        # Compliting null values
        for t_class in transfer_classes:
            if df_to_plot[df_to_plot['generic_transfer_class'] == t_class].empty:
                new_row = {'total_transfer_amount_kg': 0.0,
                            'number_of_facilities': 0,
                            'percentage': 0.0,
                            'generic_transfer_class': t_class}
                df_to_plot.append(new_row, ignore_index=True)
        
        # Other aspects
        df_to_plot.sort_values(by='generic_transfer_class', inplace=True)
        df_to_plot.reset_index(inplace=True, drop=True)
        df_to_plot['color'] = df_to_plot['generic_transfer_class'].apply(lambda x: transfer_class_colors[x])
        percentages = [0]  + df_to_plot['percentage'].cumsum().tolist()
        df_to_plot['start'] = [p * 2 * pi for p in percentages[:-1]]
        df_to_plot['end'] = [p * 2 * pi for p in percentages[1:]]
        idx_smallest = df_to_plot.nsmallest(3, 'percentage').index.tolist()
        df_to_plot['inner_radius'] = 0.25
        df_to_plot['outer_radius'] = 0.5
        df_to_plot.loc[idx_smallest, 'inner_radius'] = 0.52
        df_to_plot.loc[idx_smallest, 'outer_radius'] = 0.8
        df_to_plot['percentage'] = df_to_plot['percentage'].astype(float).map(lambda n: '{:.2%}'.format(n))
        df_to_plot["percentage"] = df_to_plot['percentage'].astype(str)

        src = ColumnDataSource(data=df_to_plot)

        return src


    def make_plot(src):

        plot = figure(title='Number of records by generic transfer class',
                    tools='wheel_zoom,pan,box_zoom,reset,save',
                    sizing_mode="stretch_both",
                    x_range=(-1.1, 1.1),
                    y_range=(-1.1, 1.1))

        plot.annular_wedge(x=0.1, y=0, inner_radius='inner_radius',
            outer_radius='outer_radius', source=src,
            start_angle='start',
            end_angle='end',  line_color="white",
            fill_color='color',
            hover_fill_color='color',
            muted_color='color',
            legend_field='generic_transfer_class',
            hover_fill_alpha=1.5,
            fill_alpha=0.6,
            muted_alpha=0.2,
            name='generic_transfer_class')

        # Hover tool with vline mode
        TOOLTIPS = [
                    ('Generic transfer class', '@generic_transfer_class'),
                    ('N° records', '@number_of_facilities{0,0} (@percentage)'),
                    ('Total transfer amount [kg/yr]', '@total_transfer_amount_kg{0,0}')
                    ]
        hover = HoverTool(tooltips=TOOLTIPS,
						  mode='mouse')
        plot.add_tools(hover)

        # Annontation
        citation = Label(x=0.7, y=0.15,
                 text='Low occurrence',
                 background_fill_color='white',
                 text_font_size = '14pt',
                 text_font = 'serif',
                 text_color = '#274472',
                 text_font_style = 'bold',
                 background_fill_alpha=1.0)
        plot.add_layout(citation)

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


        plot.axis.axis_label = None
        plot.axis.visible = False
        plot.grid.grid_line_color = None
        plot.legend.title_text_font_size = '12pt'
        plot.legend.title_text_font = 'serif'
        plot.legend.location = "top_left"
        plot.legend.title = 'Transfer class:'
        plot.legend.padding = 20
        plot.legend.border_line_color = 'black'
        plot.legend.border_line_width = 2
        plot.background_fill_color = "white"

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
    tab = Panel(child=layout, title='Pie diagram')

    return tab
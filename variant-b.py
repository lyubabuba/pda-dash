import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv('master.csv')
# Создаем датафрейм с статистикой по полу
sex_stats = pd.DataFrame(
    data.groupby(['sex'], sort=True).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()

# Создаем датафрейм с средним количеством суицидов по возрасту
age_num = pd.DataFrame(
    data.groupby(['age'], sort=True).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()
age_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']
age_num['age'] = pd.Categorical(age_num['age'], categories=age_order, ordered=True)

# Создаем датафрейм с средним количеством суицидов по поколению
gen_num = pd.DataFrame(
    data.groupby(['generation'], sort=True).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()
gen_order = ['G.I. Generation', 'Silent', 'Boomers', 'Generation X', 'Millenials', 'Generation Z']
gen_num['generation'] = pd.Categorical(gen_num['generation'], categories=gen_order, ordered=True)

# Создаем датафрейм с средним количеством суицидов по странам
country_stats = pd.DataFrame(
    data.groupby(['country'], sort=True).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()

external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN',
        'crossorigin': 'anonymous'
    }
]

external_scripts = [
    {
        'src': 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js',
        'integrity': 'sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js',
        'integrity': 'sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+',
        'crossorigin': 'anonymous'
    }
]

# Инициализация Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

# Создаем дашборд
app.layout = html.Div(
    className='main',
    children=[
        html.Div(
            tabIndex='0',
            children=[
                html.H1(children='Статистика самоубийств'),
                html.P(className='lead',
                    children="Всем привет! Ниже представлен дашборд, охватывающий статистику самоубийств в разных странах за 1984-2016 годы. Графики основаны на 2 основных параметрах - suicides_no (среднее общее число суицидов по стране) и suicide_rate (средняя частота самоубийств на 100 тысяч человек по стране)"),
                html.Div(
                    className='row row-cols-2',
                    children=[
                        html.Div(
                            className='col',
                            children=[
                                html.H2(children='Статистика по полу', id='sex-stat'),
                                dcc.RadioItems(
                                    id='sex-stat-selector',
                                    className="form-check",
                                    options=[
                                        {'label': 'Общее количество', 'value': 'suicides_no'},
                                        {'label': 'Частота', 'value': 'suicide_rate'}
                                    ],
                                    inputClassName='form-check-input',
                                    labelClassName='form-check-label',
                                    value='suicides_no',
                                    labelStyle={'display': 'block'}
                                ),
                                dcc.Graph(id='sex-stat-plot')
                            ]),
                        html.Div(
                            className='col',
                            children=[
                                html.H2(children='Статистика по возрасту', id='age-stat'),
                                dcc.RadioItems(
                                    id='age-stat-selector',
                                    className="form-check",
                                    options=[
                                        {'label': 'Общее количество', 'value': 'suicides_no'},
                                        {'label': 'Частота', 'value': 'suicide_rate'}
                                    ],
                                    inputClassName='form-check-input',
                                    labelClassName='form-check-label',
                                    value='suicides_no',
                                    labelStyle={'display': 'block'}
                                ),
                                dcc.Graph(id='age-stat-plot')
                            ]
                        ),
                        html.Div(
                            className='col',
                            children=[
                                html.H2(children='Статистика по поколениям', id='gen-stat'),
                                dcc.RadioItems(
                                    id='gen-stat-selector',
                                    className="form-check",
                                    options=[
                                        {'label': 'Общее количество', 'value': 'suicides_no'},
                                        {'label': 'Частота', 'value': 'suicide_rate'}
                                    ],
                                    inputClassName='form-check-input',
                                    labelClassName='form-check-label',
                                    value='suicides_no',
                                    labelStyle={'display': 'block'}
                                ),
                                dcc.Graph(id='gen-stat-plot')
                            ]),
                        html.Div(
                            className='col',
                            children=[
                                html.H2(children='Статистика по странам', id='country-stat'),
                                dcc.RadioItems(
                                    id='country-stat-selector',
                                    className="form-check",
                                    options=[
                                        {'label': 'Общее количество', 'value': 'suicides_no'},
                                        {'label': 'Частота', 'value': 'suicide_rate'}
                                    ],
                                    inputClassName='form-check-input',
                                    labelClassName='form-check-label',
                                    value='suicides_no',
                                    labelStyle={'display': 'block'}
                                ),
                                dcc.Graph(id='country-stat-plot')
                            ])
                    ]
                )
            ],
        )
    ])


# Callback для графика по полу
@app.callback(
    Output('sex-stat-plot', 'figure'),
    [Input('sex-stat-selector', 'value')]
)
def update_gender_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = sex_stats.sort_values(by=['suicides_no'], ascending=False)
        title = 'Общее количество'
    else:
        plot_data = sex_stats.sort_values(by=['suicide_rate'], ascending=False)
        title = 'Частота'

    color_column = {'male': 'male', 'female': 'female'}

    fig = go.Figure(data=[go.Pie(labels=plot_data['sex'], values=plot_data[selected_stat],
                                 marker=dict(colors=[color_column[gender] for gender in plot_data['sex']]))])

    fig.update_layout(title=title)

    return fig


# Callback для графика по возрасту
@app.callback(
    Output('age-stat-plot', 'figure'),
    [Input('age-stat-selector', 'value')]
)
def update_age_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = age_num.sort_values(by=['suicides_no'], ascending=False)
        title = 'Общее количество'
    else:
        rate_num = pd.DataFrame(data.groupby(['age'], sort=True)['suicide_rate'].mean()).reset_index()
        rate_num['age'] = pd.Categorical(rate_num['age'], categories=age_order, ordered=True)
        plot_data = rate_num.sort_values(by=['suicide_rate'], ascending=False)
        title = 'Частота'

    return px.pie(plot_data, names='age', values=selected_stat, title=title, category_orders={'age': age_order})


# Callback для графика по поколению
@app.callback(
    Output('gen-stat-plot', 'figure'),
    [Input('gen-stat-selector', 'value')]
)
def update_gen_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = gen_num.sort_values(by=['suicides_no'], ascending=False)
        title = 'Общее количество'
    else:
        rate_num = pd.DataFrame(data.groupby(['generation'], sort=True)['suicide_rate'].mean()).reset_index()
        rate_num['generation'] = pd.Categorical(rate_num['generation'], categories=gen_order, ordered=True)
        plot_data = rate_num.sort_values(by=['suicide_rate'], ascending=False)
        title = 'Частота'

    return px.pie(plot_data, names='generation', values=selected_stat, title=title,
                  category_orders={'generation': gen_order})


# Callback для графика по странам
@app.callback(
    Output('country-stat-plot', 'figure'),
    [Input('country-stat-selector', 'value')]
)
def update_country_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = country_stats.sort_values(by=['suicides_no'], ascending=False)
        title = 'Общее количество'
    else:
        plot_data = country_stats.sort_values(by=['suicide_rate'], ascending=False)
        title = 'Частота'

    return px.choropleth(
        plot_data,
        locations='country',
        locationmode='country names',
        color=selected_stat,
        title=title,
        color_continuous_scale='reds'
    )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8051, help="Port number")
    args = parser.parse_args()

    app.run_server(debug=True, port=args.port)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#ngrok start --config=/Users/lyubovr/Desktop/у-ч-ё-б-а/pda/ngrok.yml --all
data = pd.read_csv('/Users/lyubovr/Desktop/у-ч-ё-б-а/pda/master.csv')
# Установливаем размеры фигуры графика
plt.figure(figsize=(12, 6))

# Создаем датафрейм с средним количеством суицидов по возрасту
age_num = pd.DataFrame(data.groupby(['age'], sort=True).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()

# Указываем желаемый естественный порядок
age_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']

# Преобразуем столбец 'age' в категориальный тип с указанным порядком
age_num['age'] = pd.Categorical(age_num['age'], categories=age_order, ordered=True)

# Создаем датафрейм с статистикой по полу
sex_stats = pd.DataFrame(data.groupby(['sex'], sort=True).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()

# Создаем датафрейм с средним количеством суицидов по поколению
gen_num = pd.DataFrame(data.groupby(['generation'], sort=True).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()

# Указываем желаемый естественный порядок для поколения
gen_order = ['G.I. Generation', 'Silent', 'Boomers', 'Generation X', 'Millenials', 'Generation Z']

# Преобразуем столбец 'generation' в категориальный тип с указанным порядком
gen_num['generation'] = pd.Categorical(gen_num['generation'], categories=gen_order, ordered=True)

# Создаем датафрейм с статистикой по странам
country_stats = pd.DataFrame(data.groupby(['country']).agg({'suicides_no': 'mean', 'suicide_rate': 'mean'})).reset_index()

# Инициализация Dash
app = dash.Dash(__name__)

# Создаем дашборд
app.layout = html.Div(children=[
    html.H1(children='Suicides Statistics Dashboard'),

    html.H3(children="Hi there! here's a dashboard covering suicide statistics for different states throughout 1984-2016. Plots below are based on 2 major parameters - suicides_total (the average total value by country) & suicide_rate (the average frequency per 100 thousand people by country)"),

    html.Div(children=[
        html.H2(children='Statistics by Gender'),
        dcc.RadioItems(
            id='sex-stat-selector',
            options=[
                {'label': 'Suicides Total by Gender', 'value': 'suicides_no'},
                {'label': 'Suicide Rate by Gender', 'value': 'suicide_rate'}
            ],
            value='suicides_no',
            labelStyle={'display': 'block'}
        ),
        dcc.Graph(id='sex-stat-plot')
    ]),

    html.Div(children=[
        html.H2(children='Statistics by Age'),
        dcc.RadioItems(
            id='age-stat-selector',
            options=[
                {'label': 'Suicides Total', 'value': 'suicides_no'},
                {'label': 'Suicide Rate', 'value': 'suicide_rate'}
            ],
            value='suicides_no',
            labelStyle={'display': 'block'}
        ),
        dcc.Graph(id='age-stat-plot')
    ]),   

    html.Div(children=[
        html.H2(children='Statistics by Generation'),
        dcc.RadioItems(
            id='gen-stat-selector',
            options=[
                {'label': 'Suicides Total by Generation', 'value': 'suicides_no'},
                {'label': 'Suicide Rate by Generation', 'value': 'suicide_rate'}
            ],
            value='suicides_no',
            labelStyle={'display': 'block'}
        ),
        dcc.Graph(id='gen-stat-plot')
    ]),

    html.Div(children=[
        html.H2(children='Statistics by Country'),
        dcc.RadioItems(
            id='country-stat-selector',
            options=[
                {'label': 'Suicides Total by Country', 'value': 'suicides_no'},
                {'label': 'Suicide Rate by Country', 'value': 'suicide_rate'}
            ],
            value='suicides_no',
            labelStyle={'display': 'block'}
        ),
        dcc.Graph(id='country-stat-plot')
    ])
])


# Callback для графиков по полу
@app.callback(
    Output('sex-stat-plot', 'figure'),
    [Input('sex-stat-selector', 'value')]
)
def update_sex_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = sex_stats.sort_values(by=['suicides_no'], ascending=False)
        title = 'Suicides TOTAL by Gender'
    else:
        plot_data = sex_stats.sort_values(by=['suicide_rate'], ascending=False)
        title = 'Suicide RATE by Gender'

    color_column = {'male': 'male', 'female': 'female'}

    return px.bar(plot_data, x=selected_stat, y='sex', orientation='h', title=title, color=color_column)


# Callback для графиков по возрасту
@app.callback(
    Output('age-stat-plot', 'figure'),
    [Input('age-stat-selector', 'value')]
)
def update_age_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = age_num.sort_values(by=['suicides_no'], ascending=False)
        title = 'Suicides TOTAL by Age'
    else:
        rate_num = pd.DataFrame(data.groupby(['age'], sort=True)['suicide_rate'].mean()).reset_index()
        rate_num['age'] = pd.Categorical(rate_num['age'], categories=age_order, ordered=True)
        plot_data = rate_num.sort_values(by=['suicide_rate'], ascending=False)
        title = 'Suicide RATE by Age'

    return px.bar(plot_data, x=selected_stat, y='age', orientation='h', title=title, category_orders={'age': age_order})


# Callback для графиков по поколению
@app.callback(
    Output('gen-stat-plot', 'figure'),
    [Input('gen-stat-selector', 'value')]
)
def update_gen_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = gen_num.sort_values(by=['suicides_no'], ascending=False)
        title = 'Suicides TOTAL by Generation'
    else:
        rate_num = pd.DataFrame(data.groupby(['generation'], sort=True)['suicide_rate'].mean()).reset_index()
        rate_num['generation'] = pd.Categorical(rate_num['generation'], categories=gen_order, ordered=True)
        plot_data = rate_num.sort_values(by=['suicide_rate'], ascending=False)
        title = 'Suicide RATE by Generation'

    return px.bar(plot_data, x=selected_stat, y='generation', orientation='h', title=title, category_orders={'generation': gen_order})

# Callback для графиков по странам
@app.callback(
    Output('country-stat-plot', 'figure'),
    [Input('country-stat-selector', 'value')]
)
def update_country_plot(selected_stat):
    if selected_stat == 'suicides_no':
        plot_data = country_stats.sort_values(by=['suicides_no'], ascending=False).head(20)
        title = 'Suicides TOTAL by Country'
    else:
        plot_data = country_stats.sort_values(by=['suicide_rate'], ascending=False).head(20)
        title = 'Suicide RATE by Country'

    return px.bar(
        plot_data,
        x='country',
        y=selected_stat,
        title=title,
        labels={'country': 'Country', selected_stat: selected_stat},
        color=selected_stat,
        color_continuous_scale='reds'
    ).update_layout(
        xaxis_tickangle=-90,  # Поворот подписей оси X на 90 градусов
    )

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8052, help="Port number")
    args = parser.parse_args()

    app.run_server(debug=True, port=args.port)

from django.shortcuts import render
import plotly.offline as opy
import plotly.graph_objs as go
import pandas as pd
from .models import Iris

def iris_view(request):
    # Fetch data
    data = pd.DataFrame(list(Iris.objects.values()))

    # Heatmap: Correlation between measurements
    numeric_data = data.drop(columns=['species'])
    correlation = numeric_data.corr()
    heatmap = go.Heatmap(z=correlation.values, x=correlation.columns, y=correlation.columns)
    layout1 = go.Layout(title='Correlation between Iris measurements')
    figure1 = go.Figure(data=[heatmap], layout=layout1)
    div1 = opy.plot(figure1, auto_open=False, output_type='div')

    # Radar Chart
    means = data.groupby('species').mean().reset_index()
    categories = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    traces = []
    for index, row in means.iterrows():
        traces.append(
            go.Scatterpolar(
                r=[row[col] for col in categories],
                theta=categories,
                fill='toself',
                name=row['species']
            )
        )
    layout2 = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(data[col].max() for col in categories)]
            )
        ),
        showlegend=True,
        title="Average Measurements by Species in Radar Chart"
    )
    figure2 = go.Figure(data=traces, layout=layout2)
    div2 = opy.plot(figure2, auto_open=False, output_type='div')

    return render(request, 'iris_app/plot.html', context={'heatmap_div': div1, 'radar_div': div2})


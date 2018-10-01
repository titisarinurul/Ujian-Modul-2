import plotly.graph_objs as go
import seaborn as sns
import pandas as pd

dfTitanic = pd.read_csv('Titanic.csv')
dfTitanicOutCalc = pd.read_csv('TitanicOutCalc.csv')

listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
}
def getPlot(jenis, xCategory) :
    return [listGOFunc[jenis](
                x=dfTitanic[xCategory],
                y=dfTitanic['fare'],
                text=dfTitanic['who'],
                opacity=0.7,
                name='fare',
                marker=dict(color='blue'),
                legendgroup='fare'
            ),
            listGOFunc[jenis](
                x=dfTitanic[xCategory],
                y=dfTitanic['age'],
                text=dfTitanic['who'],
                opacity=0.7,
                name='age',
                marker=dict(color='orange'),
                legendgroup='age'
            )]

import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.YETI]
)
app.title = 'Client Segmentation Dashboard'

CLUSTER_MAPPINGS = {
    'Elite': 1,
    'Low Recent': 2,
    'Low Old': 0,
    'High Potential': 3
}





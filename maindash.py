
import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.YETI]
)
app.title = 'Client Segmentation Dashboard'
server = app.server

CLUSTER_MAPPINGS = {
    'Elite': 1,
    'Low Recent': 2,
    'Low Old': 0,
    'High Potential': 3
}
CLUSTER_ORDER = ['Low Old', 'Low Recent', 'High Potential', 'Elite']
CLUSTER_COLORS = ['#ACE2AA', '#44B977', '#00898E', '#001D68']
CLUSTER_COLORS_MAP = {CLUSTER_ORDER[i]: CLUSTER_COLORS[i] for i in range(4)}





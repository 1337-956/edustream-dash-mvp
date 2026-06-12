pandas>=2.0.0
dash>=2.11.0
dash-bootstrap-components>=1.4.0
plotly>=5.15.0
SQLAlchemy>=2.0.0
psycopg2-binary>=2.9.0

# =====================================================================
# 1. HYBRID DATABASE REGISTRATION LAYER (PostgreSQL + CSV Fallback)
# =====================================================================
DB_USER = "postgres"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "edustream_db"

# Target relational PostgreSQL cluster connection string
postgres_uri = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(postgres_uri)

def fetch_live_dashboard_data():
    """Queries production PostgreSQL relational engine with auto-fallback safety to CSV."""
    query = "SELECT * FROM fact_universities"
    try:
        # Step A: Attempt primary PostgreSQL relational ingestion query
        print("Connecting to local PostgreSQL cluster server configuration...")
        df = pd.read_sql(query, con=engine)
        print("Data successfully streamed from live PostgreSQL engine layer.")
        return df, "Production Database Engine (Live PostgreSQL)"
    except Exception as e:
        # Step B: Fall back cleanly to your flat file warehouse to ensure the application compiles
        print(f"\n[SYSTEM NOTICE] PostgreSQL offline or refused connection: {e}")
        print("Bypassing port block and routing traffic to local storage layer ('cleaned_universities.csv')...")
        
        csv_path = "cleaned_universities.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            return df, "Local CSV Storage Warehouse (API Scrape Cache)"
        else:
            # Step C: Final contingency data frame layer to prevent app layout crashes
            fallback_sample = [
                {"university_name": "Harvard University", "state_province": "MA", "country_name": "United States"},
                {"university_name": "Stanford University", "state_province": "CA", "country_name": "United States"},
                {"university_name": "Texas A&M University", "state_province": "TX", "country_name": "United States"},
                {"university_name": "Rice University", "state_province": "TX", "country_name": "United States"}
            ]
            return pd.DataFrame(fallback_sample), "Emergency Local Mock Framework Data"

# Execute hybrid ingestion check
df_universities, active_data_source_label = fetch_live_dashboard_data()

# Calculate metadata targets for business insight cards
total_scale = df_universities['university_name'].nunique()
state_options = [{'label': s, 'value': s} for s in sorted(df_universities['state_province'].dropna().unique()) if s != '']

# =====================================================================
# 2. EXECUTIVE DASHBOARD USER INTERFACE LAYOUT
# =====================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.title = "EduStream | Academic Infrastructure MVP"

app.layout = dbc.Container([
    # Executive Navbar Menu
    dbc.NavbarSimple(
        brand="EduStream Global Intelligence Portal",
        brand_href="#",
        color="dark",
        dark=True,
        className="mb-4 shadow-sm"
    ),
    
    # Header Information Notice Banner
    dbc.Row([
        dbc.Col([
            html.Div(f"Active Infrastructure Ingestion Layer: {active_data_source_label}", 
                     className="alert alert-info text-center p-2 mb-4 font-weight-bold small shadow-sm")
        ], width=12)
    ]),
    
    # Core Control Metric Row
    dbc.Row([
        # KPI Ingestion Metric Summary Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("NATIONAL INGESTION SCALE", className="card-title text-muted text-uppercase small mb-1"),
                    html.H2(f"{total_scale:,}", className="text-success font-weight-bold mb-0"),
                    html.P("Total Verified Academic Institutions", className="text-light small mb-0")
                ])
            ], color="dark", inverse=True, className="shadow-sm mb-4")
        ], md=4),
        
        # Interactive Selection Dropdown Core Component
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Interactive Analytical Scope Filter (State / Subdivision):", className="text-light font-weight-bold mb-2 small"),
                    dcc.Dropdown(
                        id='state-dropdown-selector',
                        options=state_options,
                        value='TX' if 'TX' in [s['value'] for s in state_options] else state_options['value'],
                        clearable=False,
                        style={'color': '#000000'}
                    ),
                    html.P("Updates secondary components instantly via parallel callback pipelines.", className="text-muted x-small mt-2 mb-0")
                ])
            ], color="dark", className="shadow-sm mb-4")
        ], md=8)
    ]),
    
    # Dual Visualization Analytical Panel
    dbc.Row([
        # Visualization Chart 1 Component
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Regional Density: Localized Institutional Volume", className="font-weight-bold text-light"),
                dbc.CardBody([
                    dcc.Graph(id='density-bar-chart')
                ])
            ], color="dark", className="shadow-sm mb-4")
        ], lg=7),
        
        # Visualization Chart 2 Component
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("National Market Proportion Contribution", className="font-weight-bold text-light"),
                dbc.CardBody([
                    dcc.Graph(id='proportion-donut-chart')
                ])
            ], color="dark", className="shadow-sm mb-4")
        ], lg=5)
    ])
], fluid=True)

# =====================================================================
# 3. INTERACTIVE REACTION LOGIC (Parallel Callbacks)
# =====================================================================
@app.callback(
    [Output('density-bar-chart', 'figure'),
     Output('proportion-donut-chart', 'figure')],
    [Input('state-dropdown-selector', 'value')]
)
def refresh_dashboard_insights(selected_state):
    # Dynamically query the data frame matrix layer
    state_df = df_universities[df_universities['state_province'] == selected_state]
    
    # Chart 1 Process: Regional Volume Distribution
    bar_data = state_df['university_name'].value_counts().reset_index().head(12)
    bar_data.columns = ['University Name', 'Total Records']
    
    fig_bar = px.bar(
        bar_data,
        x='Total Records',
        y='University Name',
        orientation='h',
        template='plotly_dark',
        color_discrete_sequence=['#00bc8c']
    )
    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending', 'title': None},
        xaxis={'title': 'Instance Record Count'},
        margin=dict(l=10, r=10, t=15, b=15)
    )
    
    # Chart 2 Process: Macro Share Allocation Breakdown
    national_state_counts = df_universities['state_province'].value_counts().reset_index()
    national_state_counts.columns = ['State', 'Count']
    
    top_states = national_state_counts.head(5)
    other_count = national_state_counts.iloc[5:]['Count'].sum()
    
    share_df = pd.concat([top_states, pd.DataFrame([{'State': 'Other Regions', 'Count': other_count}])], ignore_index=True)
    
    fig_donut = px.pie(
        share_df,
        values='Count',
        names='State',
        hole=0.4,
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_layout(
        margin=dict(l=10, r=10, t=15, b=15),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig_bar, fig_donut

if __name__ == '__main__':
    app.run(debug=True)

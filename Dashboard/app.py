"""
===============================================================================
Projet : Dashboard Dash Omique (POO)
Auteur : Kpaka Mouhamadou Adesanya
Module : app.py
Description : Point d'entrée principal. Orchestre les modules de données et d'UI.
===============================================================================
"""

import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State

# Importation des modules personnalisés
from data.loaders import OmicsLoader
from data.filters import GeneFilter, CompositeFilter
from ui.plots import BarPlot, HeatmapPlot, VolcanoPlot
from ui.notifications import ValidationNotification, FilterNotification


class DashApp:
    """
    Orchestrateur principal de l'application Dash (Pattern Controller).
    """
    def __init__(self, title="Omics Analysis Dashboard"):
        self.app = dash.Dash(__name__)
        self.title = title
        self.loader = None
        self.data = None
        
        self.build_layout()
        self.register_callbacks()

    def build_layout(self):
        """Construit l'interface utilisateur globale."""
        self.app.layout = html.Div([
            html.H2(self.title, style={'fontFamily': 'sans-serif', 'color': '#2c3e50'}),
            
            dcc.Upload(
                id="upload", 
                children=html.Div(['Glissez-déposez ou ', html.A('sélectionnez un fichier CSV')]),
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '2px', 'borderStyle': 'dashed',
                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px 0'
                }
            ),
            
            html.Div(id="notifications-validation"),
            
            html.Div([
                html.Label("Sélection des gènes :", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id="gene-filter", multi=True),
            ], style={'marginTop': '20px', 'marginBottom': '10px'}),
            
            html.Div([
                html.Label("Type de graphique :", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id="plot-type",
                    options=[
                        {"label": "Barplot (Expression)", "value": "barplot"},
                        {"label": "Heatmap (Comparaison)", "value": "heatmap"},
                        {"label": "Volcano Plot (Significativité)", "value": "volcano"}
                    ],
                    value="barplot",
                    clearable=False
                ),
            ], style={'marginBottom': '20px'}),
            
            dcc.Graph(id="main-graph"),
            html.Div(id="notifications-filter")
            
        ], style={'maxWidth': '850px', 'margin': 'auto', 'padding': '20px', 'fontFamily': 'sans-serif'})

    def register_callbacks(self):
        """Enregistre les réacteurs d'événements (Callbacks Dash)."""
        
        @self.app.callback(
            Output("gene-filter", "options"),
            Output("gene-filter", "value"),
            Output("notifications-validation", "children"),
            Input("upload", "contents"),
            State("upload", "filename")
        )
        def process_upload(contents, filename):
            if not contents:
                return [], [], dash.no_update
                
            # Couche 1 : Instanciation du chargeur omique
            self.loader = OmicsLoader(contents)
            self.data = self.loader.load(is_base64=True)
            
            # Validation métier
            is_valid = self.loader.validate()
            notif_ui = ValidationNotification(is_valid).render()
            
            if not is_valid:
                return [], [], notif_ui
                
            # Normalisation log2
            self.loader.normalize(method="log2")
            self.data = self.loader.raw_data
            
            genes = sorted(self.data["gene"].unique())
            options = [{"label": g, "value": g} for g in genes]
            
            return options, genes, notif_ui

        @self.app.callback(
            Output("main-graph", "figure"),
            Output("notifications-filter", "children"),
            Input("gene-filter", "value"),
            Input("plot-type", "value"),
            prevent_initial_call=True
        )
        def update_visualization(selected_genes, plot_type):
            if self.data is None:
                return dash.no_update, dash.no_update
                
            n_before = len(self.data)
            
            # Couche 2 : Application du filtrage composite
            gene_filter = GeneFilter(None) 
            composite = CompositeFilter(self.data, filters=[gene_filter])
            
            filtered_data = composite.apply(
                GeneFilter={"genes": selected_genes}
            )
            n_after = len(filtered_data)
            
            # Couche 3 : Instanciation dynamique de la classe de graphique
            plot_classes = {
                "barplot": BarPlot,
                "heatmap": HeatmapPlot,
                "volcano": VolcanoPlot
            }
            
            PlotClass = plot_classes.get(plot_type, BarPlot)
            plot_instance = PlotClass(filtered_data, title=f"Représentation : {plot_type.capitalize()}")
            
            # Couche 4 : Notification de filtrage
            filter_notif = FilterNotification(n_before, n_after).render()
            
            return plot_instance.get_figure(), filter_notif

    def run(self, debug=True):
        """Exécute le serveur Web Dash."""
        self.app.run(debug=debug)


if __name__ == "__main__":
    # Génération automatique du fichier de test local dans le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "test_omics.csv")
    
    df_test = pd.DataFrame({
        "gene": ["BRCA1", "BRCA1", "TP53", "TP53", "EGFR", "EGFR"],
        "condition": ["Control", "Treated", "Control", "Treated", "Control", "Treated"],
        "expression": [10.5, 2.1, 15.0, 18.2, 5.4, 22.1]
    })
    df_test.to_csv(csv_path, index=False)
    
    # Lancement de l'application
    dashboard = DashApp()
    dashboard.run(debug=True)
    
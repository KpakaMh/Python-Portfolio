"""
===============================================================================
Projet : Dashboard Dash Omique (POO)
Auteur : Kpaka Mouhamadou Adesanya
Module : ui/notifications.py
Description : Composants d'affichage des messages de retour utilisateur (UI feedback).
===============================================================================
"""

from dash import html


class Notification:
    """
    Classe de base pour la génération de cartes d'information/notification HTML.
    """
    def __init__(self, message: str, level="info"):
        self.message = message
        self.level = level  # 'info' | 'error'

    def render(self):
        """
        Rend le composant HTML Dash stylisé selon le niveau de sévérité.
        """
        colors = {
            "info": {"bg": "#e7f5ff", "border": "#339af0", "text": "#1864ab"},
            "error": {"bg": "#fff5f5", "border": "#fa5252", "text": "#c92a2a"}
        }
        style = colors.get(self.level, colors["info"])
        return html.Div(
            self.message,
            style={
                'backgroundColor': style["bg"], 
                'color': style["text"],
                'borderLeft': f'4px solid {style["border"]}',
                'padding': '10px', 
                'borderRadius': '4px',
                'marginTop': '10px', 
                'fontFamily': 'sans-serif'
            }
        )


class ValidationNotification(Notification):
    """
    Notification spécifique pour le résultat du contrôle qualité des données chargées.
    """
    def __init__(self, is_valid: bool):
        msg = "Fichier conforme : Structure valide et données normalisées ($log_2$)." if is_valid else "Erreur de validation : Colonnes requises manquantes ou valeurs négatives détectées."
        level = "info" if is_valid else "error"
        super().__init__(msg, level)


class FilterNotification(Notification):
    """
    Notification informant du nombre d'éléments conservés après filtrage.
    """
    def __init__(self, n_before: int, n_after: int):
        super().__init__(f"Filtre appliqué : {n_after} données affichées (sur {n_before} au total).", "info")
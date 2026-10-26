"""
===============================================================================
Projet : Dashboard Dash Omique (POO)
Auteur : Kpaka Mouhamadou Adesanya
Module : data/loaders.py
Description : Gestion du chargement, du décodage et de la validation des données.
===============================================================================
"""

import base64
import io
import pandas as pd
import numpy as np


class DataLoader:
    """
    Classe abstraite de base définissant l'interface générique de chargement de données.
    """
    def __init__(self, source: str):
        """
        Initialise le chargeur avec une source de données (chemin de fichier ou chaîne encodée).
        """
        self.source = source
        self.raw_data = None

    def load(self):
        """Méthode abstraite pour charger les données."""
        raise NotImplementedError("La méthode load() doit être implémentée dans la sous-classe.")

    def validate(self):
        """Méthode abstraite pour valider la structure des données."""
        raise NotImplementedError("La méthode validate() doit être implémentée dans la sous-classe.")


class CSVLoader(DataLoader):
    """
    Spécialisation de DataLoader pour la lecture de fichiers au format CSV (fichiers locaux ou Base64).
    """
    def load(self, is_base64=False):
        """
        Charge les données CSV dans un DataFrame Pandas.
        
        Parameters:
            is_base64 (bool): Indique si la source est une chaîne encodée transmise par Dash.
        """
        if is_base64 and self.source:
            content_type, content_string = self.source.split(',')
            decoded = base64.b64decode(content_string)
            self.raw_data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            self.raw_data = pd.read_csv(self.source)
        return self.raw_data

    def validate(self):
        """
        Vérifie la présence des colonnes minimales requises dans le fichier CSV.
        """
        if self.raw_data is None:
            return False
        required_columns = ["gene", "condition", "expression"]
        return all(col in self.raw_data.columns for col in required_columns)


class OmicsLoader(CSVLoader):
    """
    Hérite de CSVLoader — Spécialisé pour les données d'expression génique.
    Intègre des règles de validation biologique et des méthodes de normalisation.
    """
    def validate(self):
        """
        Redéfinit la méthode validate() en appelant la validation parente (super)
        et en ajoutant un contrôle sur l'absence de valeurs d'expression négatives.
        """
        base_valid = super().validate()
        if not base_valid:
            return False
        no_negatives = (self.raw_data["expression"] >= 0).all()
        return base_valid and no_negatives

    def normalize(self, method="log2"):
        """
        Applique une transformation mathématique aux niveaux d'expression.
        
        Parameters:
            method (str): Méthode de normalisation ('log2' par défaut).
        """
        if method == "log2" and self.raw_data is not None:
            self.raw_data["expression_norm"] = np.log2(self.raw_data["expression"] + 1)
        return self.raw_data
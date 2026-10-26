"""
===============================================================================
Projet : Dashboard Dash Omique (POO)
Auteur : Kpaka Mouhamadou Adesanya
Module : data/filters.py
Description : Logique de filtrage des jeux de données via le design pattern Composite.
===============================================================================
"""

import pandas as pd


class DataFilter:
    """
    Classe abstraite de base pour l'application de filtres sur un DataFrame.
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def apply(self, **kwargs):
        """Méthode abstraite d'application du filtre."""
        raise NotImplementedError("La méthode apply() doit être implémentée dans la sous-classe.")


class GeneFilter(DataFilter):
    """
    Filtre le DataFrame sur une liste de gènes d'intérêt.
    """
    def apply(self, genes: list):
        if not genes or self.data is None:
            return self.data
        return self.data[self.data["gene"].isin(genes)]


class ConditionFilter(DataFilter):
    """
    Filtre le DataFrame sur des conditions expérimentales spécifiques.
    """
    def apply(self, conditions: list):
        if not conditions or self.data is None:
            return self.data
        return self.data[self.data["condition"].isin(conditions)]


class CompositeFilter(DataFilter):
    """
    Implémentation du pattern Composite : permet d'enchaîner plusieurs filtres séquentiellement.
    """
    def __init__(self, data: pd.DataFrame, filters: list):
        super().__init__(data)
        self.filters = filters  # Liste d'instances de DataFilter

    def apply(self, **kwargs):
        """
        Applique chaque filtre de la chaîne sur le résultat du précédent.
        """
        result = self.data
        for f in self.filters:
            f.data = result
            filter_args = kwargs.get(f.__class__.__name__, {})
            result = f.apply(**filter_args)
        return result
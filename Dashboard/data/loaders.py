"""
data/loaders.py
Compatible Python 3.8+
"""

import base64
import io
import pandas as pd
import numpy as np
from pathlib import Path


class DataLoader:

    def __init__(self, source):
        self.source = source
        self.raw_data = None
        self._is_loaded = False

    def load(self, is_base64=False):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

    def summary(self):
        if not self._is_loaded:
            return {"status": "non chargé"}
        return {
            "lignes": len(self.raw_data),
            "colonnes": list(self.raw_data.columns),
            "valeurs_manquantes": int(self.raw_data.isnull().sum().sum())
        }

    def __repr__(self):
        status = "chargé" if self._is_loaded else "non chargé"
        return f"{self.__class__.__name__}(status={status})"


class CSVLoader(DataLoader):

    REQUIRED_COLUMNS = ["gene", "condition", "expression"]

    def __init__(self, source):
        super().__init__(source)

    def load(self, is_base64=False):
        if is_base64:
            content_type, content_string = self.source.split(",", 1)
            decoded = base64.b64decode(content_string)
            self.raw_data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        else:
            path = Path(self.source)
            if not path.exists():
                raise FileNotFoundError(f"Fichier introuvable : {path}")
            self.raw_data = pd.read_csv(path)

        self.raw_data.columns = self.raw_data.columns.str.strip().str.lower()
        self.raw_data.dropna(how="all", inplace=True)
        self._is_loaded = True
        return self.raw_data

    def validate(self):
        if self.raw_data is None:
            raise RuntimeError("Appeler load() avant validate()")
        missing = [c for c in self.REQUIRED_COLUMNS if c not in self.raw_data.columns]
        return len(missing) == 0


class OmicsLoader(CSVLoader):

    def __init__(self, source):
        super().__init__(source)

    def load(self, is_base64=False):
        super().load(is_base64=is_base64)

        if "log2fc" not in self.raw_data.columns:
            self.raw_data["log2fc"] = np.random.uniform(-3, 3, len(self.raw_data))
        if "pvalue" not in self.raw_data.columns:
            self.raw_data["pvalue"] = np.random.uniform(0.001, 0.99, len(self.raw_data))

        return self.raw_data

    def validate(self):
        if not super().validate():
            return False
        no_neg   = (self.raw_data["expression"] >= 0).all()
        not_empty = self.raw_data["gene"].notna().all()
        return bool(no_neg and not_empty)

    @property
    def available_features(self):
        if self.raw_data is None:
            return []
        base = {"gene", "condition", "expression", "log2fc", "pvalue"}
        return [
            c for c in self.raw_data.select_dtypes(include="number").columns
            if c not in base
        ]

    def normalize(self, method="log2"):
        col = self.raw_data["expression"]
        if method == "log2":
            self.raw_data["expression_norm"] = np.log2(col + 1)
        elif method == "zscore":
            self.raw_data["expression_norm"] = (col - col.mean()) / col.std()
        return self.raw_data

    def summary(self):
        base = super().summary()
        base.update({
            "gènes_uniques": int(self.raw_data["gene"].nunique()),
            "conditions":    list(self.raw_data["condition"].unique()),
            "features":      self.available_features,
        })
        return base
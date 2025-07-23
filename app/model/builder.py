import logging
import pandas as pd

class Model:
    def __init__(self, df: pd.DataFrame, classified: str):
        logging.info("Initializing Model...")
        self._validate_input(df, classified)
        self.df = df
        self.classified = classified
        self.features = self._get_features()
        self.labels = self._get_labels()
        self.model = {}
        self.all_val = {}
        self.class_prob = self.get_class_prob()
        logging.info("Model initialized successfully.")

    def _validate_input(self, df: pd.DataFrame, classified: str):
        logging.debug("Validating input DataFrame and classified column.")
        if df is None or df.empty:
            logging.error("Received empty DataFrame.")
            raise ValueError("Received empty DataFrame.")
        if classified not in df.columns:
            logging.error(f"Column '{classified}' not found in DataFrame.")
            raise ValueError(f"Column '{classified}' not found in DataFrame.")
        logging.debug("Input validation passed.")

    def _get_features(self):
        features = [col for col in self.df.columns if col != self.classified]
        logging.info(f"Extracted features: {features}")
        return features

    def _get_labels(self):
        labels = self.df[self.classified].unique()
        logging.info(f"Identified labels: {labels}")
        return labels.tolist()
    def get_class_prob(self):
        class_count = self.df[self.classified].value_counts()
        total = len(self.df)
        return (class_count/total).to_dict()

    def create_model(self):
        logging.info("Creating model based on dataset...")

        for column in self.features:
            self.model[column] = {}
            unique_values = self.df[column].unique()
            self.all_val[column] = unique_values.tolist()
            size = len(unique_values)
            logging.debug(f"Processing column '{column}' with {size} unique values.")

            for val in unique_values:
                self.model[column][val] = {}

                for label in self.labels:
                    clas = self.df[self.df[self.classified] == label]
                    numerator = len(clas[clas[column] == val]) + 1
                    denominator = len(clas) + size
                    probability = numerator / denominator
                    self.model[column][val][label] = probability

                    logging.debug(
                        f"P({column}={val} | {self.classified}={label}) = {probability:.4f} "
                        f"(numerator={numerator}, denominator={denominator})"
                    )
        logging.info("Model creation complete.")
    def info(self):
        return [self.model,self.all_val,self.class_prob]

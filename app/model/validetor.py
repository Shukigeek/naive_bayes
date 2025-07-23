import math
import pandas as pd
from sklearn.metrics import confusion_matrix

class Evaluation:
    def __init__(self, trained: dict, test_df: pd.DataFrame, label_col: str,class_prob:dict):
        self.trained = trained
        self.test = test_df
        self.label_col = label_col
        self.labels = self.test[label_col].unique()
        self.class_prob = class_prob

    def _predict_row(self, row: pd.Series) -> str:
        scores = {}
        for label in self.labels:
            log_prob = 0
            for feature, value in row.drop(labels=[self.label_col]).items():
                prob = self.trained.get(feature, {}).get(value, {}).get(label, 1e-9)
                log_prob += math.log(prob)
            log_prob += math.log(self.class_prob[label])
            scores[label] = math.exp(log_prob)
        return max(scores, key=scores.get)

    def true_vs_pred(self):
        y_true = self.test[self.label_col].tolist()
        y_pred = self.test.apply(self._predict_row, axis=1).tolist()
        return y_true, y_pred
    def accuracy_stats(self):
        y_true, y_pred = self.true_vs_pred()
        correct = sum(t == p for t, p in zip(y_true, y_pred))
        total = len(y_true)
        incorrect = total - correct
        accuracy = correct / total * 100
        return {
            "correct": correct,
            "incorrect": incorrect,
            "accuracy_percent": accuracy
        }
    def get_confusion_matrix(self):
        y_true, y_pred = self.true_vs_pred()
        cm = confusion_matrix(y_true, y_pred, labels=self.labels)
        cm_df = pd.DataFrame(cm, index=self.labels, columns=self.labels)
        # print("\nConfusion Matrix:")
        # print(cm_df)
        return cm_df.to_dict(orient="index")
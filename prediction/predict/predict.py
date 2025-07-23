import math


class Predict:
    def __init__(self, model: dict,class_prob:dict,labels:list):
        self.model = model
        self.labels = labels
        self.class_prob = class_prob
    def predict_row(self, row: dict) -> str:
        scores = {}
        for label in self.labels:
            log_prob = 0
            for feature, value in row.items():
                prob = self.model.get(feature, {}).get(value, {}).get(label, 1e-9)
                log_prob += math.log(prob)
            print(self.class_prob[label])
            print(type(self.class_prob[label]))

            log_prob += math.log(self.class_prob[label])
            scores[label] = math.exp(log_prob)
        return max(scores, key=scores.get)


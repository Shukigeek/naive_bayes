import math


class Predict:
    def __init__(self, model: dict,class_prob:dict,labels:list):
        self.model = model
        self.labels = labels
        self.class_prob = class_prob

    def predict_row(self, row: dict) -> str:
        print(">> התחזית מתחילה")
        print(">> קלט:", row)
        scores = {}
        for label in self.labels:
            log_prob = 0
            for feature, value in row.items():
                prob = self.model.get(feature, {}).get(value, {}).get(label, 1e-9)
                log_prob += math.log(prob)
            print(f"label={label}, class_prob={self.class_prob.get(label)}, type={type(self.class_prob.get(label))}")
            log_prob += math.log(self.class_prob[label])
            scores[label] = math.exp(log_prob)
        print(">> scores:", scores)
        if not scores:
            return "Error: Empty scores"
        return max(scores, key=scores.get)



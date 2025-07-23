from model.data_loader import DataLoader
from model.cleaner import Clean
from model.builder import Model
from model.split_data import split_dataframe
from model.validetor import Evaluation

class ModelManager:
    def __init__(self, file: str, label: str):
        self.file = file
        self.label = label
        self._load_and_prepare()
        self._train_model()
        self._evaluate()

    def _load_and_prepare(self):
        loader = DataLoader()
        loader.load_data(self.file)
        df = Clean.clean_dataframe(loader.df)
        self.train_df, self.test_df = split_dataframe(df)

    def _train_model(self):
        model = Model(self.train_df, self.label)
        model.create_model()
        self.model = model.model
        self.class_prob = model.class_prob
        self.features = model.features
        self.labels = model.labels
        self.options = model.all_val

    def _evaluate(self):
        self.evaluator = Evaluation(self.model, self.test_df, self.label, self.class_prob)

    def get_accuracy(self):
        return self.evaluator.accuracy_stats()

    def get_confusion_matrix(self):
        return self.evaluator.get_confusion_matrix()

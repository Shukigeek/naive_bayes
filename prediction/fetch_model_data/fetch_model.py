import requests

class GetModel:
    def __init__(self, url="http://model:8000/trained_model"):
        self.trained_model = None
        self.class_prob = None
        self.labels = None
        self.fetch_model(url)

    def fetch_model(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.trained_model = data.get('model')
                self.class_prob = data.get('class_prob')
                self.labels = data.get('labels')
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Exception occurred while fetching model: {e}")

# דוגמה לשימוש:
if __name__ == "__main__":
    model = GetModel()
    if model.trained_model:
        print("Model fetched successfully!")
        print("model:",model.trained_model)
        print("class_prob:",model.class_prob)
        print("Labels:", model.labels)
    else:
        print("Failed to fetch the model.")

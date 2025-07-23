import requests

class GetOptions:
    def __init__(self, url="http://127.0.0.1:8000/get_options"):
        self.fetch_model(url)

    def fetch_model(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.options = data.get('options')
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Exception occurred while fetching model: {e}")


if __name__ == "__main__":
    model = GetOptions()
    if model.options:
        print("options fetched successfully!")
        print("options:",model.options)
    else:
        print("Failed to fetch the model.")

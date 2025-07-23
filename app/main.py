from fastapi import FastAPI

from prediction.fetch_model_data.fetch_model import GetModel
from prediction.predict.predict import Predict
from model_manager import ModelManager
import os
import uvicorn


app = FastAPI()
def get_model_path(file_base):
    if os.path.exists("/.dockerenv"):

        return f"/app/data/{file_base}"
    else:

        return f"/app/data/{file_base}"
# file = 'app/data/buy_computer.csv'
file = get_model_path('buy_computer.csv')
label = 'buys_computer'

model_manager = ModelManager(file, label)

@app.get('/trained_model')
def trained_model():
    return {'model': model_manager.model,
            'class_prob' : model_manager.class_prob,
            'labels' : model_manager.labels.tolist() if hasattr(model_manager.labels, 'tolist') else list(model_manager.labels)
    }
@app.get('/get_options')
def get_options():
    return {'options':model_manager.options}

@app.get('/evaluation')
def evaluation():
    return model_manager.get_accuracy()

@app.get('/confusion_matrix')
def confusion():
    return model_manager.get_confusion_matrix()

fetch = GetModel()

@app.post('/prediction')
def prediction(row:dict):
    print(">>> קיבלנו נתונים לתחזית:")
    print(row)

    if fetch.trained_model is None:
        print("❌ המודל לא נטען כמו שצריך!")
        return {"error": "Model not loaded"}

    try:
        predict = Predict(fetch.trained_model,fetch.class_prob,fetch.labels)
        res = predict.predict_row(row)
        print(">>> תחזית התקבלה בהצלחה:", res)
        return {'prediction':res}
    except Exception as e:
        print("❌ שגיאה בזמן תחזית:", e)
        return {"error": str(e)}



if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

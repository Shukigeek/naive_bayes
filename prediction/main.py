from fetch_model import GetModel
from fastapi import FastAPI
from predict import Predict
import uvicorn


app = FastAPI()

fetch = GetModel()

@app.get('/prediction')
def prediction():
    predict = Predict(fetch.trained_model,fetch.class_prob,fetch.labels)
    row = {'age': '<=30', 'income': 'medium', 'student': 'yes', 'credit_rating': 'fair'}
    res = predict.predict_row(row)
    print(res)
    return res

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
from fetch_model_data.fetch_model import GetModel
from fastapi import FastAPI
from predict.predict import Predict
import uvicorn


app = FastAPI()

fetch = GetModel()

@app.post('/prediction')
def prediction(row:dict):
    predict = Predict(fetch.trained_model,fetch.class_prob,fetch.labels)
    res = predict.predict_row(row)
    print(res)
    return {'prediction':res}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
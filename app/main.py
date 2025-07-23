from fastapi import FastAPI
from model_manager import ModelManager
import os
import uvicorn


app = FastAPI()
def get_model_path(file_base):
    if os.path.exists("/.dockerenv"):

        return f"/app/data/{file_base}"
    else:

        return f"data/{file_base}"
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

if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

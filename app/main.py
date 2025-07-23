from fastapi import FastAPI
from model_manager import ModelManager

app = FastAPI()

file = 'model/buy_computer.csv'
label = 'buys_computer'

model_manager = ModelManager(file, label)

@app.get('/evaluation')
def evaluation():
    return model_manager.get_accuracy()

@app.get('/confusion_matrix')
def confusion():
    return model_manager.get_confusion_matrix()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

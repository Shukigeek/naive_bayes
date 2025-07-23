from fastapi import FastAPI, HTTPException
import uvicorn
from data_loader import DataLoader
from cleaner import Clean
from builder import Model
from split_data import split_dataframe
from validetor import Evaluation

app = FastAPI()

# file = 'model/all_star.csv'
# label = 'Label'
# file = 'model/Staff.csv'
# label = 'Position'

file = r'C:\Users\shuki\AppData\Local\Microsoft\Windows\INetCache\IE\ZCIWUMX7\buy_computer_data[1].csv'
label = 'buys_computer'

# טוען דאטא והופך את זה לטבלה
data_loader = DataLoader()
data_loader.load_data(file)
df = data_loader.df
# מנקה את הדאטא
df = Clean.clean_dataframe(df)
# מקבל 70 אחוזים מהדאטא
train_df,test_df = split_dataframe(df)
# מאמן את המודל
train_model = Model(train_df, label)
train_model.create_model()
#שומר את המודל
model_trained = train_model.model
# שומר את הערכים של הלייבל לפי כמות
class_prob = train_model.class_prob
# שומר את כל שמות של העמודות והערכים בפנים
features = train_model.features
labels = train_model.labels
options = train_model.all_val

eva = Evaluation(model_trained,test_df,label,class_prob)

@app.get('/evaluation')
def evaluation():
    if eva:
        return eva.accuracy_stats()
    return 'message: model not found'
@app.get('/confusion_matrix')
def evaluation():
    if eva:
        return eva.get_confusion_matrix()
    return 'message: model not found'

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


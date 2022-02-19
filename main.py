from matplotlib.font_manager import json_load
import pandas as pd
import json
from fastapi import  FastAPI
from pydantic import BaseModel
import os
# from test import Student

app=FastAPI()

DB_PATH = './data/students.csv'

def database():
    students:pd.DataFrame=None
    if not os.path.exists(DB_PATH):
        students = pd.DataFrame(columns=['id','fname','lname','age'])
    else:
        students = pd.read_csv('./data/students.csv')
    return students

@app.get("/")
def root():
   return{"massege":"hello data_scientist."}

@app.get("/data/{limit}")
def data(limit:int):
    df=pd.read_csv("./data/airports.csv",nrows=limit)
    return json.loads(df.to_json(orient='records')) 
    
class Student(BaseModel):
    id: int
    fname: str
    age: int
    lname: str

@app.post("/create/")
def create(student:Student):
    db = database()
    student_dict = student.dict()
    db=db.append(student_dict,ignore_index=True)
    db.to_csv(DB_PATH,index=False)
    return student_dict

@app.put("/update/")
def create(student:Student):
    db = database()
    db.loc[db.id==student.id,'fname']=student.fname
    db.loc[db.id==student.id,'lname']=student.lname
    db.loc[db.id==student.id,'age']=student.age
    db.to_csv(DB_PATH,index=False)
    return student.dict()


@app.delete("/delete/{id}")
def create(id:int):
    db = database()
    db=db[db.id!=id]
    db.to_csv(DB_PATH,index=False)
    return {'status':'deleted'}



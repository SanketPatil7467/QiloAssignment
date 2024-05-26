from fastapi import FastAPI,Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from pymongo import MongoClient
from bson import json_util

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")

db = client["QiloDB"]
collection = db["Students"]
# dictionary = {"id": 12,
#               "name": "Rohan Das"}
# collection.insert_one(dictionary)



@app.get("/getdetails")
async def get_details():
    details = []
    for detail in collection.find():
        details.append(detail)
    return json_util.dumps(details)


@app.post("/add")
async def add_data(request: Request, name: str = Query(None)):
    data = await request.json()
    if name:
        data["name"] = name
    result = collection.insert_one(data)
    inserted_id = json_util.dumps(result.inserted_id)
    return {"message": "Data added successfully", "id": inserted_id}


@app.delete("/students/{name}")
async def delete_student(name: str):
    result = collection.delete_one({"name": name})
    if result.deleted_count == 1:
        return JSONResponse(content={"message": "Student deleted successfully"})
    else:
        return JSONResponse(content={"message": "Student not found"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5050)

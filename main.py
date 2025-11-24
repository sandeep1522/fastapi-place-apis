
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uuid
import json
import os

app = FastAPI(title="Place APIs (RahulShettyAcademy compatible)")

DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")
EXPECTED_KEY = "qaclick123"

def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

class Location(BaseModel):
    lat: float
    lng: float

class AddPlaceBody(BaseModel):
    location: Location
    accuracy: int
    name: str
    phone_number: str
    address: str
    types: list
    website: str
    language: str

class DeletePlaceBody(BaseModel):
    place_id: str

class UpdatePlaceBody(BaseModel):
    place_id: str
    address: str
    key: str = None

# ADD PLACE (POST) - query param key=qaclick123
@app.post("/maps/api/place/add/json")
def add_place(body: AddPlaceBody, key: str = Query(...)):
    if key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    db = read_db()
    place_id = uuid.uuid4().hex
    # store the place as dict, include place_id
    place = body.dict()
    place['place_id'] = place_id
    db[place_id] = place
    write_db(db)
    # sample-like response
    return {
        "status": "OK",
        "place_id": place_id,
        "scope": "APP",
        "reference": uuid.uuid4().hex,
        "id": uuid.uuid4().hex
    }

# GET PLACE (GET) - requires place_id and key
@app.get("/maps/api/place/get/json")
def get_place(place_id: str = Query(...), key: str = Query(...)):
    if key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    db = read_db()
    if place_id not in db:
        raise HTTPException(status_code=404, detail="Place not found")
    # return stored place object (excluding our internal place_id duplication if present)
    place = db[place_id].copy()
    return place

# UPDATE PLACE (PUT) - expects JSON body with place_id, address, key
@app.put("/maps/api/place/update/json")
def update_place(body: UpdatePlaceBody):
    if body.key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    db = read_db()
    pid = body.place_id
    if pid not in db:
        raise HTTPException(status_code=404, detail="Place not found")
    # update address
    db[pid]['address'] = body.address
    write_db(db)
    # Return a response similar to the sample (returning full place object)
    return db[pid]

# DELETE PLACE (POST) - as per provided doc, using POST at delete/json
@app.post("/maps/api/place/delete/json")
def delete_place(body: DeletePlaceBody, key: str = Query(...)):
    if key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    db = read_db()
    pid = body.place_id
    if pid in db:
        del db[pid]
        write_db(db)
        return {"status": "OK"}
    raise HTTPException(status_code=404, detail="Place not found")

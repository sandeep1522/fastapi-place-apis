
# FastAPI Place APIs (Rahul Shetty Academy compatible)

This project implements the 4 Place APIs using **FastAPI**, with the exact same request/response structure
(and the same API key `qaclick123`) as the document you provided.

## Endpoints
- `POST /maps/api/place/add/json?key=qaclick123`  → Add a place  
- `GET  /maps/api/place/get/json?place_id=<id>&key=qaclick123` → Get a place  
- `PUT  /maps/api/place/update/json`  → Update a place (body contains place_id, address, key)  
- `POST /maps/api/place/delete/json?key=qaclick123` → Delete a place (body contains place_id)

## Files
- `main.py` - FastAPI app  
- `asgi.py` - ASGI exposure for hosting  
- `database.json` - simple JSON file storage (created/updated at runtime)  
- `requirements.txt` - Python dependencies

## Running locally (for testing)
1. Create virtualenv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Swagger UI will be available at `http://localhost:8000/docs`

## Deploying on PythonAnywhere
- Free tier supports hosting; to use your custom domain `sandeepyadavacademy.com` you'll need a paid plan.
- Upload the project files via the **Files** tab.
- Install dependencies from a Bash console:
  ```bash
  pip install -r requirements.txt --user
  ```
- Create a Web app (manual config) and point it to use `uvicorn` to run `main:app`.
- Alternatively, use the `asgi.py` exposure and configure the web app to run an ASGI server.

If you want, I can provide step-by-step screenshots for PythonAnywhere setup.

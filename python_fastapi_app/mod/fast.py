import sys
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

fruits = []
app = FastAPI()


@app.get("/")
async def docs_redirect():
    try:
        return RedirectResponse(url='/docs')
    except Exception:
        sys.exc_info()
        exception_json = {
            "Error Message": sys.exc_info()
        }
        raise HTTPException(status_code=404, detail=exception_json)


@app.post('/add_fruits')
def add_fruits(fruit):
    fruits.append(fruit)
    return {"fruit added": fruits[-1]}

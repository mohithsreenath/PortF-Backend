from fastapi import FastAPI
from app.endpoints.skills import router as skills_router
from app.endpoints.catagories import router as categories_router


app = FastAPI(
    title="Portfolio Backend API"
)

@app.get("/")
def health_check():
    return {"status": "running"}

app.include_router(skills_router)
app.include_router(categories_router)

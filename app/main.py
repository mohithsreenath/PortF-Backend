from fastapi import FastAPI
from app.endpoints.skills import router as skills_router
from app.endpoints.catagories import router as categories_router
from app.endpoints.projects import router as projects_router
from app.endpoints.admin import router as admin_router
from app.endpoints.blogs import router as blogs_router
from app.endpoints.experience import router as experience_router
from app.endpoints.contact import router as contact_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Portfolio Backend API"
)

#CORS
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5173",        # local dev
        "http://localhost:4173",        # local preview
        "https://your-vercel-app.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def health_check():
    return {"status": "running"}

app.include_router(skills_router)
app.include_router(categories_router)
app.include_router(projects_router)
app.include_router(admin_router)
app.include_router(blogs_router)
app.include_router(experience_router)
app.include_router(contact_router)
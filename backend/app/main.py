
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.settings import settings
from .routers import health, chat, profile

app = FastAPI(title=settings.APP_NAME)

# CORS pour permettre l'appel depuis l'IHM Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # + ton domaine prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router)
app.include_router(chat.router)
app.include_router(health.router)


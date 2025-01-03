from fastapi import FastAPI,HTTPException
from router import servers,kernel_user_base_fetcher,foreman_api
from  database import engine,SessionLocal
import models
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
models.Base.metadata.create_all(bind=engine)
app.include_router(servers.router)
app.include_router(kernel_user_base_fetcher.router)
app.include_router(foreman_api.router)


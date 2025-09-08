from fastapi import FastAPI
from main.routers import user, todo, auth, service
from main.database.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Main App",
    description="Main application API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(todo.router)
app.include_router(auth.router)
app.include_router(service.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app", 
        host="0.0.0.0",
        port=8000,
        reload=True
    )
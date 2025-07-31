from fastapi import FastAPI
from app.database import init_db
from app.routes import auth, project, user

app = FastAPI()

init_db()

app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
app.include_router(project.router, prefix="/v1/projects", tags=["projects"])
app.include_router(user.router, prefix="/v1/user", tags=["user"])

# /ping route for health check
@app.get("/ping", tags=["system"])
def ping():
    return {"message": "pong"}

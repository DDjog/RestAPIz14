from fastapi import FastAPI
import uvicorn
from src.routes import contacts, auth, users


app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.get("/")
async def root():
    return {"message": "--> mega super duper FastAPI sample contacts  <--"}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


import os

from dotenv import load_dotenv

# Load environment variables from .env file if not running in AWS Lambda
if not os.environ.get("AWS_EXECUTION_ENV"):
    print("Loading .env file")
    load_dotenv(os.path.join(os.getcwd(), ".env"))

from beanie import init_beanie
from core.models.shoes import Sneaker
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.middleware.sessions import SessionMiddleware

from api.data.instance import DATABASE_NAME, client
from api.routes import auth, sneakers

# Create FastAPI app
app = FastAPI(
    redoc_url=None,  # Disable redoc, keep only swagger
    responses={404: {"resource": "Not found"}},  # Custom 404 page
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Enable session handling for StocxkX OAuth flow
app.add_middleware(SessionMiddleware, secret_key="vT!y!r5s#bwcDxDG")


@app.on_event("startup")
async def startup_event():
    # Initialize Beanie ODM
    await init_beanie(
        database=client.get_database(DATABASE_NAME),
        document_models=[Sneaker],
    )
    # Include all routers
    app.include_router(sneakers.router)
    app.include_router(auth.router)


# This is the entry point for AWS Lambda
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn

    # Run the app locally using Uvicorn
    uvicorn.run(app, host="localhost", port=8000)

from fastapi import FastAPI

app = FastAPI(
    title="FuelIQ API",
    description="Fuel tracking and analytics platform",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {"message": "Welcome to FuelIQ"}

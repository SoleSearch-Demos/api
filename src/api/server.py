import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="localhost",
        port=8000,
        reload=True,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
    )

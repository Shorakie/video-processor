import uvicorn

if __name__ == "__main__":
    """Run the application."""
    uvicorn.run("app:create_app", factory=True, host="0.0.0.0", port=8000)

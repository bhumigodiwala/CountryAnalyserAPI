import uvicorn
from app.views.views import app
from app.models.models import Base, engine

if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="127.0.0.1", port=8000)

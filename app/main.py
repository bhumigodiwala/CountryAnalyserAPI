#main.py -> run the app
import uvicorn
from views.views import app
from models.models import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # Run the app using uvicorn on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)

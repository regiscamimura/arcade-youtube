import os
import sys

import uvicorn

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    uvicorn.run("app.web_interface:app", host="127.0.0.1", port=8000, reload=True)

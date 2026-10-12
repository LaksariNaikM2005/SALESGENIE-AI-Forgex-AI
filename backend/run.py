import os
import sys
from pathlib import Path
import uvicorn

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.main import app

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "true").lower() == "true"

    print(f"🚀 Starting SalesGenie AI FastAPI Server at http://{host}:{port}")
    print(f"📚 OpenAPI Interactive Documentation at http://{host}:{port}/docs")

    uvicorn.run(
        "backend.app.main:app",
        host=host,
        port=port,
        reload=debug,
    )
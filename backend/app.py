import os
import sys

# Ensure backend directory is in the Python search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from main import app

if __name__ == "__main__":
    app.run(debug=True, port=5000)
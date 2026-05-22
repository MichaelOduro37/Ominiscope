import os
import sys

# Ensure backend folder is first on sys.path so local `app` package is found
HERE = os.path.dirname(__file__)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# local import after sys.path patching
from app import create_app  # noqa: E402


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5000)

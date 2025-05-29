import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

try:
    from app import create_app
    app = create_app()
except Exception as e:
    import traceback
    print(f"Error: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

import os
import importlib


# Get the package directory
package_dir = os.path.dirname(__file__)

# Iterate over all python files in the package directory (excluding __init__.py)
for file in os.listdir(package_dir):
    if file.endswith(".py") and file != "__init__.py":
        # Import the module
        module = importlib.import_module(f".{file[:-3]}", __name__)
        
        # Import all classes from the module
        for name in module.__dict__:
            if not name.startswith("__"):
                globals()[name] = getattr(module, name)

# Import SQLModel
from sqlmodel import SQLModel
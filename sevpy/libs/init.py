from pathlib import Path

def create_dirs(debug=False):
    """
    Creates the necessary directories for the project.
    """
    HOME_DIR = Path.home()
    CACHE_DIR = HOME_DIR / ".cache"
    dirs = [
        CACHE_DIR / "sevpy",
    ]
    
    for dir in dirs:
        if debug: print(f"[DEBUG] Creating directory: {dir}")
        dir.mkdir(parents=True, exist_ok=True)
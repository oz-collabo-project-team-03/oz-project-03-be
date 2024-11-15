import logging
import platform
import subprocess
import sys
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG)

# 프로젝트 루트 디렉토리를 sys.path에 추가
# 상단에 위치 필수 !
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 여기부터 router 추가


app = FastAPI(debug=True)

origins = ["https://daesik.store", "http://localhost:5173", "https://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_origin_regex="http://111\.111\.111\.111(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")


def run_check_script():
    system = platform.system().lower()

    if system == "darwin":  # Mac OS
        script_path = "./scripts/check.sh"
    elif system == "windows":
        script_path = "./scripts/check.bat"

    try:
        print(f"Running {script_path}...")
        result = subprocess.run([script_path], capture_output=True, text=True, shell=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr, file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: {script_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_check_script()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

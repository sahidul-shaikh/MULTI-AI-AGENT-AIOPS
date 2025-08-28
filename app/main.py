import subprocess
import threading
import time
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)

    except Exception as e:
        logger.error(f"Backend server failed to start: {e}")
        raise CustomException("Backend server failed to start", error_detail=e)
    
def run_frontend():
    try:
        logger.info("Starting frontend UI...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)

    except Exception as e:
        logger.error(f"Frontend UI failed to start: {e}")
        raise CustomException("Frontend UI failed to start", error_detail=e)
    
if __name__ == "__main__":

    try:
        backend_thread = threading.Thread(target=run_backend)
        frontend_thread = threading.Thread(target=run_frontend)

        backend_thread.start()
        time.sleep(5) 
        frontend_thread.start()

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise CustomException("Failed to start application", error_detail=e)

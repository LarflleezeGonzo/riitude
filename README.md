
# Riitide FastAPI Project


## Getting Started

### Prerequisites
- Python environment is set up
- [Git](https://git-scm.com/) is installed

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/LarflleezeGonzo/riitude.git
   ```

2. Change into the project directory:
   ```bash
   cd riptide
   ```

3. Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### FastAPI Web Application
- Serve the FastAPI application with the following command:
   ```bash
   uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The application will be available at `http://localhost:8000`.

- Access Swagger documentation at:
   `http://localhost:8000/docs`

### Testing
- Run tests using the following command:
   ```bash
   pytest fastapi_app/tests/test_api.py
   ```

### CLI Application
- Run the CLI application with the following command:
   ```bash
   python cli_app/app/main.py
   ```


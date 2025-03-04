# FastAPI Scaffold

## Project Description
This project is a web application built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/ahmadkhidir/fastapi-scaffold.git
    ```
2. Change to the project directory:
    ```bash
    cd fastapi-scaffold
    ```
3. Create a virtual environment:
    ```bash
    python -m venv env
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source env/bin/activate
        ```
5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Using Docker Compose
1. Clone the repository:
    ```bash
    git clone https://github.com/ahmadkhidir/fastapi-scaffold.git
    ```
2. Change to the project directory:
    ```bash
    cd fastapi-scaffold
    ```
3. Build and start the containers:
    ```bash
    docker compose up --build
    ```

## Usage
1. Run the application:
    ```bash
    uvicorn main:app --reload
    ```
2. Open your browser and navigate to `http://127.0.0.1:8000` to see the application running.

### Using Docker Compose
1. Run the application:
    ```bash
    docker compose up
    ```
2. Open your browser and navigate to `http://127.0.0.1:8000` to see the application running.

### Using Makefile
1. Create and apply migrations:
    ```bash
    make createmigrations "Your migration message"
    make migrate
    ```
2. Create an admin user:
    ```bash
    make createadminuser
    ```

## Features
- FastAPI for building APIs
- Pydantic for data validation
- Asynchronous request handling

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License.

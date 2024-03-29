# CountryAnalyserAPI

A FastAPI project that includes a Restful API to fetch countries from an external API (https://restcountries.com). It incorporates user authentication (JWT-based login) and signup with a required country field. Additionally, the project involves the creation of a user table, data generation, and the utilization of machine learning algorithms for analyzing user activities to provide suggestions for new company branches based on market analysis in each country. The project follows industry-standard practices, including version control using Git and asynchronous programming for improved efficiency.

## Table of Contents
- [Directory Structure](#directory-structure)
- [Setup and Usage](#setup-and-usage)
  - [Setting Up Environments](#setting-up-environments)
  - [Running Locally](#running-locally)
- [Results](#results)
  
## Directory Structure

```bash

CountryAnalyserAPI
├── app
│   ├── controllers
│   │   └── controllers.py
│   ├── models
│   │   └── models.py
│   └── views
│      └── views.py
|   ├── main.py
│   ├── create_data.py
│   ├── test.db
├─  venv/
├── README.md
└── requirements.txt
```

| Directory/File              | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| **app/**                    | Core application directory.                                                 |
|                             |                                                                             |
| **controllers/**            | Business logic modules.                                                     |
| **controllers.py**          | Main module for handling business logic.                                    |
|                             |                                                                             |
| **models/**                 | Data model definitions.                                                     |
| **models.py**               | Central module defining data models.                                        |
|                             |                                                                             |
| **views/**                  | Manages HTTP requests and rendering views.                                  |
| **views.py**                | Main module responsible for handling views and request processing.          |
|                             |                                                                             |
| **create_data.py**          | Script to generate and insert mock data into the database.                  |
|                             |                                                                             |
| **main.py**                 | Entry point for the application, handling initialization and setup.         |
|                             |                                                                             |
| **test.db**                 | SQLite database file for storing test data during development and testing.  |
|                             |                                                                             |
| **venv/**                   | Virtual environment directory.                                              |
|                             |                                                                             |
| .gitignore                  | Specifies files and directories to ignore in version control.               |
|                             |                                                                             |
| requirements.txt            | Lists project dependencies.                                                 |
|                             |                                                                             |
| README.md                   | Project documentation.                                                      |

## Setup and Usage

### Setting Up Environments

1. **Python Environment:**

   > It's recommended to use a virtual environment for Python to manage dependencies.

    _Using `venv`_
    - Create a virtual environment in the root directory:
      ```bash
      python -m venv {$venv_name} # In this case the {$venv_name} -> venv
      ```
    - Activate the virtual environment:
      - On Windows:
        ```bash
        {$venv_name}\Scripts\activate
        ```
      - On macOS and Linux:
        ```bash
        source {$venv_name}/bin/activate
        ```
    - Install the required Python packages:
      ```bash
      pip install -r requirements.txt
      ```

### Running Locally

**Start FastAPI Server:**
  Start FastAPI Server (Backend):
  1. In one terminal run this command to start the server:
     ```bash
     cd app
     uvicorn main:app --reload
     ```
     
  This command starts the FastAPI server on `http://127.0.0.1:8000` and also creates the database(test.db) in the app directory.

  2. In another terminal run the below command to generate mock data entries in the database:
     ```bash
     cd app
     python3 create_data.py
     ```
  Explore FastAPI with Swagger Documentation on `http://127.0.0.1:8000/docs`.

**Note:** This README provides a basic setup guide. Additional setup and configuration might be needed depending on your environment and requirements.

## Results

### Database
The database(test.db) in the SQLite DB viewer:

<img align="center" width="600" alt="image" src="https://github.com/bhumigodiwala/CountryAnalyserAPI/assets/62346064/39970ee9-3ec6-4c81-a8e4-43c3de4d9e53">

### API Endpoints

1. GET response (Default response)

  <img align="center" width="600" alt="image" src="https://github.com/bhumigodiwala/CountryAnalyserAPI/assets/62346064/c0ee9a3f-ca20-4454-a384-49512bba3b31">

2. Signup Endpoint

  <img align="center" width="600" alt="image" src="https://github.com/bhumigodiwala/CountryAnalyserAPI/assets/62346064/9ada80b3-64f9-4874-96e1-bf4e11980727">

3. Token Verification

  <img align="center" width="600" alt="image" src="https://github.com/bhumigodiwala/CountryAnalyserAPI/assets/62346064/000a9330-41d1-4dbb-a2f9-0d894a28ec04">

4. ML Algorithm Analysis

a. User Authorization

  <img align="center" width="600" alt="image" src="https://github.com/bhumigodiwala/CountryAnalyserAPI/assets/62346064/207efc16-c9df-4c49-8a4f-24b343741ef2">

b. ML Analysis Result Suggestion      

  <img align="center" width="600" alt="image" src="https://github.com/bhumigodiwala/CountryAnalyserAPI/assets/62346064/68e39ad9-ec36-42f2-8962-4416a36aeddb">


  

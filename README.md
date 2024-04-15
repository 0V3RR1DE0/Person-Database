# Releasing Soon!


# Person Data Database

A Flask-based web application for managing database entries.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Manual Installation](#manual-installation)
  - [Docker Installation](#docker-installation)
      - [Dockerfile](#dockerfile)
- [Usage](#usage)
  - [Manual Run](#manual-run)
  - [Docker Run](#docker-run)
- [Default Root User](#default-root-user)
- [Upcoming Features](#default-root-user)
- [Credits](#credits)
- [License](#license)

## Features

- **User Authentication:**
  - Register, log in, and log out.
  - Change passwords.
  - Root users can manage other users.
  
- **Entry Management:**
  - Add, view, and edit database entries.
  - Only root users can delete entries.

- **Database:**
  - SQLite is used as the database backend.

## Requirements

- Python 3.x
- Flask
- Flask SQLAlchemy
- Flask Login
- Flask WTF
- Flask Bootstrap
- Docker (optional)

## Installation

### Manual Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/0V3RR1DE0/Person-Database.git
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

### Docker Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/0V3RR1DE0/Person-Database.git
    ```
2. **Make Dockerfile:**

    ##### Linux
    ```Linux
    mkdir Person-Database
    cd Person-Database
    nano Dockerfile
    ```

    ##### Windows
    ```Windows
    mkdir Person-Database
    cd Person-Database
    notepad Dockerfile
    ```
    
    #### Dockerfile

    ```Dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.9-slim-buster

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container
    COPY . /app
    
    # Upgrade pip
    RUN pip install --no-cache-dir --upgrade pip

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Make port 5000 available to the world outside this container
    EXPOSE 5000

    # Define environment variable
    ENV FLASK_APP app.py

    # Run app.py when the container launches
    CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
    ```

3. **Build the Docker image:**

    ```bash
    docker build -t person-database .
    ```

## Usage

### Manual Run

```bash
python app.py
```

### Docker Run

- **Default Port (5000):**

    ```bash
    docker run -d -p 5000:5000 --name person-database person-database:latest
    ```

- **Different Port (e.g., 5001):**

    ```bash
    docker run -d -p 5001:5001 --name person-database person-database:latest
    ```

- Open your web browser and navigate to `http://localhost:5000` or `http://localhost:5001` to access the application.

## Default Root User

- **Username:** root
- **Password:** default

## Upcoming Features:

- [ ] **Markdown Support for Entries**

## Credits

This project was created by [0V3RR1DE0](https://github.com/0V3RR1DE0).

## License

This project is licensed under the [MIT] License - see the [LICENSE.md](LICENSE.md) file for details.

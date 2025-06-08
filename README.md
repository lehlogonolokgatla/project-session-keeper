# Project Estimator Web Application (Flask)

 Overview

The **Project Estimator** is a simple yet effective Flask web application designed to help users track hours spent on various projects and calculate estimated costs based on an hourly rate. It provides a straightforward interface for logging work sessions and viewing a summary of all projects, making it a useful tool for freelancers, consultants, or anyone needing to manage project time and budget.

## Features

-   **Project Creation:** Easily define new projects with a name, type, and an assigned hourly rate.
-   **Session Tracking:** Log individual work sessions by specifying start and end times for each project.
-   **Automatic Calculations:** The application automatically calculates the duration of each session, accumulates total hours for a project, and estimates the cost based on the configured hourly rate.
-   **Work Details:** Add brief descriptions or notes to each session for better record-keeping and context.
-   **Database Persistence:** All project and session data is securely stored in an SQLite database using SQLAlchemy ORM, ensuring data integrity and persistence across sessions.
-   **Timezone Awareness:** Implements timezone handling (specifically SAST) to accurately log and display timestamps, avoiding common time-related issues.
-   **User-Friendly Interface:** A clean and intuitive web interface allows for easy navigation and data entry.

## Technologies Used

-   **Backend:** Python (Flask)
-   **Database:** SQLite (managed with Flask-SQLAlchemy)
-   **Frontend:** HTML, CSS (with W3.CSS for responsiveness and basic styling)
-   **Timezone Handling:** `pytz` library

## Setup and Installation

To run this application locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/lehlogonolokgatla/Project-Estimator.git](https://github.com/lehlogonolokgatla/Project-Estimator.git)
    cd Project-Estimator
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure your `requirements.txt` file contains `Flask`, `Flask-SQLAlchemy`, and `pytz`).

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

6.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/` (or the address displayed in your terminal).

    *Note: The `site.db` database file will be created automatically in your project directory upon the first run if it doesn't already exist.*

## Usage

-   **Create Projects:** Use the interface to add new projects with their details.
-   **Log Sessions:** For each project, you can add new work sessions, specifying start and end times.
-   **View Summaries:** The main dashboard or project-specific pages will display accumulated hours and estimated costs.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

[Specify your license here, e.g., MIT License, Apache License 2.0, etc.]

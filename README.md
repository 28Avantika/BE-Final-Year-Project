# Early Detection of Alzheimer Disease Using Deep Learning and Smart Medicine Box

## Introduction

This project is a web application designed to detect early signs of Alzheimer's disease using deep learning algorithms and to assist patients with medication management through a smart medicine box integration. The application aims to provide an accessible tool for early diagnosis, enhancing treatment outcomes and improving patient quality of life. The smart medicine box ensures timely medication intake, fostering better health management.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Demo/Preview](#demopreview)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Installation Instructions](#installation-instructions)
6. [Usage Instructions](#usage-instructions)
7. [Contact Information](#contact-information)

---

## Demo/Preview

You can view the live demo of the application hosted on GitHub Pages:

[Live Demo](https://github.com/28Avantika/BE-Final-Year-Project)

Alternatively, here is a preview of the application:

![Application Screenshot](./assets/screenshot.png)

---

## Features

- Early detection of Alzheimer's disease using advanced deep learning models.
- Integration with a smart medicine box for timely medication reminders.
- User-friendly web interface for patients and caregivers.
- Secure storage of patient data and test results.
- Real-time notifications and alerts for missed medications.
- Detailed analytics and insights for healthcare providers.

---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **Machine Learning**: TensorFlow, Keras
- **Database**: PostgreSQL
- **Hosting**: GitHub Pages
- **Version Control**: Git, GitHub

---

## Installation Instructions

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/28Avantika/BE-Final-Year-Project.git
   ```

2. Navigate to the project directory:
   ```bash
   cd BE-Final-Year-Project
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database (ensure PostgreSQL is installed and configured):
   ```bash
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

6. Run the application locally:
   ```bash
   flask run
   ```

7. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage Instructions

1. **Perform an Alzheimer's Detection Test:**
   - Upload MRI or medical imaging data through the user-friendly interface.
   - View the detailed prediction and analysis report.

2. **Healthcare Provider Access:**
   - View analytics and patient history.
   - Provide personalized treatment plans based on detailed reports.

---

## Contact Information

- **Maintainer**: Avantika Shende
- **Email**: avantikashende2@gmail.com
- **GitHub**: [Avantika Shende's GitHub Profile](https://github.com/28Avantika)

Feel free to reach out if you have any questions or feedback!

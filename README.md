[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/Teacher-Android-App/blob/main/README.md)
[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/Teacher-Android-App/blob/main/README.fa.md)
# SEPAD (The Persian acronym for Student Online Monitoring System) - Teacher-Android-App
This repository is a part of the SEPAD project and was developed by [Abolfazl Rashidian](https://github.com/abolfazlrashidian) for students to enter the class and send their attention level to the server.

Click [here](https://github.com/SEPAD-Project) to visit the SEPAD organization.

## Overview
The Teacher Panel in SEPAD is a management interface that allows teachers to monitor students' attention levels in real-time during online classes. This panel collects data on their focus (through facial recognition and gaze analysis via webcam) and displays it on Android app.

## Requirements
Before installation, ensure you meet these requirements:
- Python 3.8 or higher for running on Windows & Linux
- Flet application for running on Android
## Installation

1. Clone the repository:
```bash
git clone https://github.com/SEPAD-Project/Teacher-Android-App.git
```
2. Navigate to the student-app directory:
```bash
cd Teacher-android-app
```
3. Create a virtual environment:
```bash
python -m venv .venv
```
4. Activate the virtual environment:
```bash
.venv\Scripts\activate.bat
```
5. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application
1. Run RUN.py file
```bash
python RUN.py
```

## Directory Structure
```bash
teacher-android-app/
├── source/
├── └──
├──── gui/                          # GUI components
│     └── login.py                  # Main application entry point
├──── backend/                      # Attention analysis models
├── RUN.py                          # Run login page
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
└── .gitignore                      # Git ignore file
```

# 📝 Contribution  
1. Fork the repository  
2. Create feature branch (`git checkout -b feature/NewFeature`)  
3. Commit changes (`git commit -m 'Add NewFeature'`)  
4. Push to branch (`git push origin feature/NewFeature`)  
5. Open a Pull Request  

# 📬 Contact  
**Email**: SepadOrganizations@gmail.com  
**Issues**: [GitHub Issues](https://github.com/SEPAD-Project/Teacher-Android-App/issues)  

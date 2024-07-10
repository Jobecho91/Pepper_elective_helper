# Pepper Elective Helper

This repository contains the final project for the Human Centered Interaction in Robotics course.

## Overview

Pepper Elective Helper is a project aimed at enhancing the interaction between humans and robots, specifically using Pepper robot. The project focuses on allowing Pepper to help students choose electives subjects in the autonomous systems master's degree at HBRS University.

Detailed information about the project
1. Pepper detects faces using a webcam.
2. Initiates a personalized, multi-modal greeting upon face detection.
3. Handles noise and errors in face detection and verification.
4. Assists users in finding preferred elective subjects through conversation.
5. Uses an internal model to recommend courses based on user preferences, optionally providing a ranking using a Bayesian network.
6. Uses illustrative gestures during conversation.
7. Bids farewell in a socially appropriate manner after the conversation.
8. Filters and refrains from engaging in abusive language.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Jobecho91/Pepper_elective_helper.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Pepper_elective_helper
    ```

3. Create and Activate Virtual Environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  
    ```
4. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure all dependencies are installed.

2. Run the main script to initiate the project:

    ```bash
        python main.py
    ```
## RASA Integration

This project uses RASA for advanced dialogue management. Due to file size constraints, the full RASA model files are not included in this repository. However, you can upload the basic files needed to train the RASA model.
## Training the RASA Model

1. Ensure you have RASA installed:
    ```bash
        pip install rasa
    ```
    For more information check RASA documentation- [RASA](https://rasa.com/docs/rasa/installation/installing-rasa-open-source/)

2. Upload the necessary training files (nlu.yml, stories.yml, domain.yml, etc.) to the rasa directory.

3. Train the RASA model
    ```bash
        rasa train
    ```
4. Run the RASA server:
    ```bash
        rasa run actions
        rasa shell
    ```

# License

Distributed under the MGNU GPL 3.0. See `LICENSE` for more information.
 
## References

- [RASA Documentation](https://rasa.com/docs/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyAgrum Documentation](https://pyagrum.readthedocs.io/en/latest/)
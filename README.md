# Uni Admission Chatbot 🤖

Welcome to the Uni Admission Chatbot repository! This repository contains code and resources for ai tutor, a field that supports humans in learning math.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

---

## Introduction

Uni Admission Chatbot is a project inspired by Autonomous Agents to help users learn math through interactive AI. It provides personalized assistance and real-time feedback, enhancing the learning experience.

The system's core components are function calling and memory management, which ensure efficient task execution and personalized interactions. Uni Admission Chatbot revolutionizes math education by creating a seamless and engaging learning environment.

## Features

- **Function Calling by JSON Parsing**: Executes specific tasks based on user inputs by parsing JSON data, enabling precise and efficient interactions.
- **Tool Calling by Prompting**: Utilizes prompts to access and operate various tools, enhancing the AI's capability to assist with diverse tasks.
- **Memory Management**: Retains and recalls past interactions to provide a personalized learning experience, ensuring continuity and context in user interactions.
- **Evaluation Metrics**: Evaluation metrics and benchmarks to assess the performance of reasoning algorithms and compare different approaches.

## Installation

Follow these steps to set up Uni Admission Chatbot on your local machine or server:

### 1. Clone repository

```
https://gitlab.ftech.ai/nlp/research/uni_admission_chatbot.git
cd uni-admission-chatbot
```

### 2. Install Libraries and Dependencies

```
pip install -r requirements.txt
```

### 3. Get the API Key

Obtain the necessary API key from the relevant third-party service provider.

- Groq API: Access the [Groq Cloud](https://console.groq.com) to get API Key
- Literal API: Access the [Literal AI](https://cloud.getliteral.ai), then signin or signup to create project and get API key
- Chainlit auth secret: After install libraries and dependencies, run cli ``chainlit create-secret``

### 4. Run the Demo App

- To run the demo app locally

```
chainlit run app.py
```

- To run the demo app on a server

```
chainlit run app.py -h --host <host> --port <port>
```

## Usage

## Contributing

Contributions to this repository are welcome! If you have any ideas, bug reports, or want to add new features, feel free to submit a pull request. Please make sure to follow the existing coding style, write clear commit messages, and provide sufficient documentation for your changes.

## License

This repository is licensed under the MIT License. You are free to use, modify, and distribute the code and resources for both commercial and non-commercial purposes. Refer to the LICENSE file for more information.

## Authors

- Phạm Văn Quân
- Ngô Văn Úc

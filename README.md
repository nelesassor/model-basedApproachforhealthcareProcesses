# Model-Based Approach for Healthcare Processes

## Description

This Python script is developed as part of a master's thesis project, focusing on a model-based approach for comparing and evaluating healthcare processes. The project utilizes BPMN (Business Process Model and Notation), OWL (Web Ontology Language), and RDF (Resource Description Framework) to analyze and compare healthcare processes.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The purpose of this project is to provide a model-based approach for comparing and evaluating healthcare processes. This involves the use of BPMN for modeling healthcare processes and the integration of OWL and RDF to enable semantic analysis.

## Installation

Before using this project, make sure you have Python installed. You can download Python from [python.org](https://www.python.org/downloads/).

To set up the required Python libraries, you can use `pip`:

bash
pip install nltk 


## Usage
The core functionality of this script involves the classification and categorization of healthcare process descriptions into various domains within the healthcare system. These domains encompass Actors, Tasks, Data, Steps, Communication (digital and analog), Information, and Systems.

To utilize the script for classification purposes, you can employ the classify_task_description function. This function accepts a task description as input and provides the associated category.

The output will display the classified task along with its respective category.

To apply the classification to BPMN diagrams, you can utilize the modify_bpmn_labels function. This function analyzes BPMN diagrams and updates the labels of elements based on the classification of tasks.

modify_bpmn_labels('input_file_path.bpmn', 'output_file_path.bpmn')

## License
This project is licensed under the MIT License. 
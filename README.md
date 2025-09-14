# SVG Animator AI
================

## Introduction
This repository contains a Streamlit application that utilizes a Large Language Model (LLM) to animate SVG icons. The application allows users to upload a static SVG file, describe the desired animation, and then generates an animated SVG file based on the user's prompt.

## Requirements
To run the application, you will need to install the following libraries:

* `langchain_google_genai`
* `langchain_community`
* `unstructured`
* `streamlit`

You can install these libraries by running the following command:
```bash
pip install -r requirements.txt
```
## Usage
To use the application, follow these steps:

1. Upload a static SVG file using the file uploader.
2. Describe the desired animation in the text input field.
3. Click the "Generate" button to generate the animated SVG file.
4. View the animated SVG file and download it if desired.

## Code Explanation
The application consists of several components:

* `front_end.py`: This file contains the Streamlit application code, including the file uploader, text input field, and generate button.
* `src.py`: This file contains the LLM setup and configuration, including the API key and model selection.
* `notebook.ipynb`: This file contains a Jupyter Notebook that demonstrates the usage of the LLM to animate an SVG file.
* `images/`: This directory contains example SVG files that can be used to test the application.
* `output/`: This directory contains the generated animated SVG files.

## LLM Configuration
The LLM is configured using the `langchain_google_genai` library. The API key is set using the `GOOGLE_API_KEY` environment variable. The model used is the `gemini-2.5-flash` model, which is a text-to-text model that can generate text based on a given prompt.

## Animation Generation
The animation generation process involves the following steps:

1. The user uploads a static SVG file and describes the desired animation.
2. The LLM is used to generate a new SVG file based on the user's prompt.
3. The generated SVG file is then displayed in the application and can be downloaded by the user.

## Example Use Cases
Here are some example use cases for the application:

* Animating a logo or icon to create a dynamic visual effect.
* Creating animated illustrations or graphics for a website or social media platform.
* Generating animated SVG files for use in presentations or videos.

## Limitations
The application has the following limitations:

* The LLM may not always generate the desired animation, and the user may need to refine the prompt to achieve the desired result.
* The application only supports SVG files, and does not support other file formats such as PNG or JPEG.
* The application requires a stable internet connection to function, as it relies on the LLM API to generate the animated SVG files.
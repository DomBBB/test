[![python](https://img.shields.io/badge/python-3.8.5-blue?logo=python&logoColor=FED643)](https://www.python.org)
[![License: BSD 2-Clause](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)  

<p align="center"> <img src="assets/logo.png" height="256"> </p>

# <p> <img src="assets/logo.png" height="30"> ARTify Studio </p>

ARTify Studio is a desktop application where users can upload images and apply various artistic styles to it. It supports customization options such as filters, image editing, and frames, aswell as exporting the final images. This guide will walk you through the setup and use of the app.

- 🎴 Images reimagined in styles of Monet, Van Gogh, Cezanne, and Ukiyo-e.
- 🤖 Deep Learning powered Generative AI to apply styles to your images.
- 🎨 Own customizations through filters, editing and further adjustments.
- 🖥️ Intuitive UI with easy-to-navigate sliders, dropdowns, and checkboxes.
- 💾 Save edited images to your gallery and export them in various formats.


---

## 💻 Installation - Windows

### 0. Prerequisite

Ensure you have **Python 3.8.5** or later installed on your system (*program tested for 3.8.5*). You can download Python from python.org.

### 1. Download the Program

Download or clone this repository.

### 2. Set up a Virtual Environment and install required libraries

Open command prompt and navigate to the project folder
    
Create a venv in the project folder <img align="right" src="assets/install_1.jpg" height="20">

    python -m venv venv

Activate the venv <img align="right" src="assets/install_2.jpg" height="20">

    venv\Scripts\activate

Within the venv, install required libraries <img align="right" src="assets/install_3.jpg" height="20">

    pip install -r requirements.txt

### 3. Launch ARTify Studio

If necessary, open command prompt and navigate to the project folder

If necessary, reactivate the venv <img align="right" src="assets/install_2.jpg" height="20">

    venv\Scripts\activate

Within the venv, execute <img align="right" src="assets/run.png" height="20">

    python main.py


---

## 💻 TO DO

Installation - macOS

### 0. Prerequisite

Ensure you have **Python 3.8.5** or later installed on your system (*program tested for 3.8.5*). You can download Python from python.org.

### 1. Download the Program

Download or clone this repository.

### 2. Set up a Virtual Environment and install required libraries

Open Terminal and navigate to the project folder
    
Create a virtual environment:

    python3 -m venv venv

Activate the virtual environment:

    source venv/bin/activate

Navigate to the requirements.txt file and execute:

    pip install -r requirements.txt

### 3. Launch ARTify Studio

Navigate to the project folder and execute:

    python main.py


---

## 📑 TO DO

Using the App

After starting the app, you’ll see the main navigation page with buttons to upload images, edit images, and view a gallery.

### 1. Upload Image

Select up to 12 images from your computer or choose sample images from the app's library. The selected images are then processed
before the **Workspace** is displayed.

### 2. Workspace

Displays each image together with its style previews. Click an image to start customizing the image in real-time. In the editor,
you can chose a style from the dropdown, adjust properties like brightness or sharpness using sliders and apply filters like sepia,
grayscale, or ccolorize. Finally, you can add frames or textures to enhance the image further and export the images into your **Gallery**.

### 3. Gallery

Display all images and their stored edits. There are various options to view and export the edited images in a preferred format.


---

## 💖 Acknowledgments

Thanks to all contributors and the open-source community.

### Contributors

This project has been created for the master's course **7,789: Skills: Programming with Advanced Computer Languages** taught by **Dr. Mario Silic** at the **University of St.Gallen (HSG)** in the **Autumn Semester 2024**.

- Katja Alison Zimmermann
- Dominik Manuel Buchegger

### Powered by CycleGAN

CycleGAN is a generative model architecture used for image style transfer without needing paired examples of the original and target styles during training. In our application, we leveraged a CycleGAN with four pretrained models to apply artistic styles to images. We also used some images from the CycleGAN dataset for the app's example images.

- [Model architecture](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
- [Pretrained models](https://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/)
- [Example images](https://efrosgans.eecs.berkeley.edu/cyclegan/datasets/)

CycleGAN is licensed under [BSD 2-Clause](https://opensource.org/licenses/BSD-2-Clause), which is why this project has the same license.

### Creation supported by ChatGPT

ChatGPT has been used througout the project, which enabled us to rapidly build an entire application around our image style transfer.

- Logo created by DALL·E
- Graphical user interface built with assistance from GPT-4o
- Image filter and editing functions created by GPT-4o 

<p align="center"> <img src="assets/logo.png" height="256"> </p>

# ARTify Studio

ARTify Studio is a desktop application where users can upload images and apply various artistic styles to it. It supports customization options such as filters, image editing, and frames aswell as the export of the edited images. This guide will walk you through the setup and use of the app.

- 🎴 Images reimagined in styles of Monet, Van Gogh, Cezanne, and Ukiyo-e.
- 🤖 Generative UI to apply selected styles to your images.
- 🎨 Filters and adjustments to add your own customizations.
- 🖥️ Intuitive UI with easy-to-navigate sliders, dropdowns, and checkboxes.
- 💾 Save edited images to a gallery and export them in various formats.


## 💻 Installation

### 0. Prerequisite

Ensure you have **Python 3.8.5** or later installed on your system (*program tested for 3.8.5*). You can download Python from python.org.

### 1. Download the Program

Download or clone this repository.

### 2. Set up a Virtual Environment and install required libraries

**Windows**

Open Command Prompt and navigate to the project folder
    
Create a virtual environment:

    python -m venv venv

Activate the virtual environment:

    venv\Scripts\activate

Navigate to the requirements.txt file and execute:

    pip install -r requirements.txt

**macOS**

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


## 🌐 Resources




Using the App

After starting the app, you’ll see the main navigation page with options to upload images, view a gallery, and edit images.
1. Uploading an Image

    Go to the Upload page.
    Select an image from your computer or choose a sample image from the app's library.

2. Workspace

    The Workspace page shows each image with dropdowns to select different styles.
    Select a style to preview it, and click Edit to start customizing the image.

3. Editor

    In the Editor, you can:
        Choose a style from the dropdown.
        Adjust properties like Brightness, Contrast, and Sharpness using sliders.
        Apply filters like Sepia, Grayscale, or Colorize.
        Add frames or textures to enhance the image further.

<p align="center"> <img src="path/to/editor_screenshot.png" width="600"> </p>
4. Saving and Exporting

    Save the edited image to the gallery using the Save to Gallery button.
    Export the image in a preferred format (JPEG, PNG, BMP) using the Export button.


---

## 💖 Acknowledgments

Thanks to all contributors and the open-source community.

### Contributors
- Katja Alison Zimmermann
- Dominik Manuel Buchegger

### Powered by CycleGAN
- [Model architecture](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
- [Pretrained models](https://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/)
- [Example images](https://efrosgans.eecs.berkeley.edu/cyclegan/datasets/)

### Supported by ChatGPT
- Logo created by DALL·E
- Graphical user interface built with assistance from GPT-4o
- Image filters and editing created by GPT-4o 

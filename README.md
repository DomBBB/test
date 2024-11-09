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

---

## 🌐 Resources

**GitHub Repo:**
  - **RAG API:** [github.com/danny-avila/rag_api](https://github.com/danny-avila/rag_api)
  - **Website:** [github.com/LibreChat-AI/librechat.ai](https://github.com/LibreChat-AI/librechat.ai)

**Other:**
  - **Website:** [librechat.ai](https://librechat.ai)
  - **Documentation:** [docs.librechat.ai](https://docs.librechat.ai)
  - **Blog:** [blog.librechat.ai](https://docs.librechat.ai)

---

## 📝 Changelog

Keep up with the latest updates by visiting the releases page and notes:
- [Releases](https://github.com/danny-avila/LibreChat/releases)
- [Changelog](https://www.librechat.ai/changelog) 

**⚠️ Please consult the [changelog](https://www.librechat.ai/changelog) for breaking changes before updating.**

---

## ⭐ Star History

<p align="center">
  <a href="https://star-history.com/#danny-avila/LibreChat&Date">
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=danny-avila/LibreChat&type=Date&theme=dark" onerror="this.src='https://api.star-history.com/svg?repos=danny-avila/LibreChat&type=Date'" />
  </a>
</p>
<p align="center">
  <a href="https://trendshift.io/repositories/4685" target="_blank" style="padding: 10px;">
    <img src="https://trendshift.io/api/badge/repositories/4685" alt="danny-avila%2FLibreChat | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
  </a>
  <a href="https://runacap.com/ross-index/q1-24/" target="_blank" rel="noopener" style="margin-left: 20px;">
    <img style="width: 260px; height: 56px" src="https://runacap.com/wp-content/uploads/2024/04/ROSS_badge_white_Q1_2024.svg" alt="ROSS Index - Fastest Growing Open-Source Startups in Q1 2024 | Runa Capital" width="260" height="56"/>
  </a>
</p>














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

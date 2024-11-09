<p align="center"> <img src="assets/logo.png" height="256"> </p>

# ARTify Studio

---

X

📃
- 🖥️ UI 
- 🤖 AI 
- 🪄 Generative UI with **[Code Artifacts](https://youtu.be/GfTj7O4gmd0?si=WJbdnemZpJzBrJo3)**
   - Create React, HTML code, and Mermaid diagrams right in chat
- 💾 Create, Save, & Share Custom Presetsעברית
- 🎨 Customizable Dropdown & Interface: Adapts to both power users and newcomers


## 🪶 All-In-One AI Conversations with LibreChat

LibreChat brings together the future of assistant AIs with the revolutionary technology of OpenAI's ChatGPT. Celebrating the original styling, LibreChat gives you the ability to integrate multiple AI models. It also integrates and enhances original client features such as conversation and message search, prompt templates and plugins.

With LibreChat, you no longer need to opt for ChatGPT Plus and can instead use free or pay-per-call APIs. We welcome contributions, cloning, and forking to enhance the capabilities of this advanced chatbot platform.

[![Watch the video](https://raw.githubusercontent.com/LibreChat-AI/librechat.ai/main/public/images/changelog/v0.7.5.png)](https://www.youtube.com/watch?v=IDukQ7a2f3U)
Click on the thumbnail to open the video☝️

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











Overview

The Art Studio App is an interactive platform where users can upload images, apply various artistic styles, adjust filters, and export their edited images. The app supports multiple image transformation styles (e.g., Monet, Van Gogh) and customization options such as tint, texture, and frames. This guide will walk you through the installation, setup, and use of the app.
Features

    Image Styling: Choose from styles like Monet, Van Gogh, Cezanne, and Ukiyo-e.
    Adjustments and Filters: Control exposure, brightness, contrast, sharpness, and more.
    Save and Export: Save edited images to a gallery or export them in various formats.
    Intuitive UI: Easy-to-navigate layout with sliders, dropdowns, and checkboxes.

Installation
1. Prerequisites

Ensure you have Python 3.7 or later installed on your system. You can download Python from python.org.
2. Clone the Repository

git clone https://github.com/yourusername/art-studio-app.git
cd art-studio-app

3. Setting Up a Virtual Environment

To avoid conflicts, set up a virtual environment in your project directory.
macOS

    Open Terminal.
    Navigate to your project folder and create a virtual environment:

python3 -m venv venv

Activate the virtual environment:

    source venv/bin/activate

Windows

    Open Command Prompt.
    Navigate to your project folder and create a virtual environment:

python -m venv venv

Activate the virtual environment:

    venv\Scripts\activate

4. Install Required Libraries

Once the virtual environment is activated, install the dependencies from the requirements.txt file.

pip install -r requirements.txt

Running the App

To launch the Art Studio App, follow these steps:

    Navigate to the project folder if not already there:

cd art-studio-app

Run the main application file:

    python main.py

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

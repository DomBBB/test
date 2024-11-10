"""
This file defines the main components of ARTify Studio, including pages for viewing,
editing, and saving images with various styles and adjustments. The app provides an
intuitive UI with sliders, checkboxes, and dropdowns.

Key pages include:
- WorkspacePage: Users can preview and select images.
- EditorPage: Users can apply edits, add effects, and export images.
"""

# Import PyQT5 for GUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QGridLayout, QScrollArea, QCheckBox, QPushButton, QMessageBox, QStackedLayout, QHBoxLayout, QSizePolicy, QFileDialog, QSlider
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFont

# Import libraries
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
import shutil
import time
import uuid
import numpy as np

# Import toolbar
from ui.toolbar_helper import setup_toolbar


class WorkspacePage(QWidget):
    """
    Workspace page that displays each original image together with its different
    styles for preview. Original images are clickable and open the image editor.
    """

    # Signals for navigation to other pages
    go_to_main = pyqtSignal()
    go_to_upload = pyqtSignal()
    go_to_workspace = pyqtSignal()
    go_to_gallery = pyqtSignal()

    # Signal to go to the editor page
    go_to_editor = pyqtSignal(str)

    def __init__(self):
        """
        Initializes the workspace page layout including the toolbar and all
        original and styled images for the user to select one image to edit.
        """

        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the main user interface for the workspace page, including the toolbar for navigation,
        a description label, and a scrollable grid layout to display images. Each image group displays
        various styles and provides options for editing and deletion.
        """

        #####################################################################
        #                                                                                                                                      #
        # Setup Main Layout                                                                                                      #
        #                                                                                                                                      #
        #####################################################################

        # Main layout for the page with padding and spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Add the toolbar for navigation
        self.toolbar = setup_toolbar(
            self,
            self.go_to_main.emit, # Signal for main page
            self.go_to_upload.emit, # Signal for upload page
            self.go_to_workspace.emit, # Signal for workspace page
            self.go_to_gallery.emit # Signal for gallery page
        )
        # Make the toolbar transparent
        self.toolbar.setStyleSheet("background: none;")
        # Toolbar at the top
        main_layout.addWidget(self.toolbar)

        # Title label centered at the top
        description_label = QLabel(
            "View your Processed Images and Select one to Edit")
        description_label.setFont(QFont("Arial", 15, QFont.Bold))
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("color: #555555; background: none;")
        description_label.setWordWrap(True)
        # Add to the page
        main_layout.addWidget(description_label)

        # Scrollable area for main content with padding and spacing
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        grid_layout = QGridLayout(content_widget)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(30)

        # Set background color for the page
        self.setStyleSheet("background-color: #f7f9fc;")

        # Set thumbnail size
        self.image_size = 400

        #####################################################################
        #                                                                                                                                      #
        # Content Layout                                                                                                            #
        #                                                                                                                                      #
        #####################################################################

        # Load images (newest image folders first)
        image_groups = sorted(Path("database/workspace").glob("*"), key=lambda x: x.name, reverse=True)
        # If there are images in the workspace folder
        if image_groups:
            # Populate the grid layout
            row = 0
            for group_folder in image_groups:
                self.add_image_group_to_grid(group_folder, grid_layout, row)
                row += 1
        # If there are no images in the workspace folder
        else:
            # Display a message
            no_images_label = QLabel("No processed images available")
            no_images_label.setFont(QFont("Arial", 14))
            no_images_label.setAlignment(Qt.AlignCenter)
            no_images_label.setStyleSheet("color: #555555;")
            no_images_label.setWordWrap(True)
            # Add to layout
            grid_layout.addWidget(no_images_label)

        #####################################################################
        #                                                                                                                                      #
        # Set Layout                                                                                                                    #
        #                                                                                                                                      #
        #####################################################################

        # Set the scroll area to contain all content
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Set Layout
        self.setLayout(main_layout)

    def add_image_group_to_grid(self, group_folder, main_layout, row):
        """
        Adds a grid of images for each style variant in the given image group folder.
        Each group includes the original image and its various styled versions.

        Parameters:
            group_folder (Path): Path to the folder containing the image group.
            main_layout (QGridLayout): The layout to which images are added.
            row (int): The row index for positioning the image group in the grid.
        """

        # Define available styles for each image group
        styles = ["original", "cezanne", "monet", "ukiyoe", "vangogh"]
        image_name = group_folder.name

        # Iterate through all styles
        for col, style in enumerate(styles):
            image_path = group_folder / f"{image_name}_{style}.png"

            # Create a container with no margins for each image
            container = QWidget()
            container_layout = QGridLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)

            # Set up the image label to display the styled image
            image_label = QLabel()
            # Original image
            if style == "original":
                image_size = self.image_size
            # Styled images are displayed smaller
            else:
                image_size = int(self.image_size * 3 / 4)
            pixmap = QPixmap(str(image_path)).scaled(image_size, image_size, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            # Add to layout
            container_layout.addWidget(image_label, 0, 0, Qt.AlignCenter)

            # The original image contains a delete button
            if style == "original":
                # Add a delete button on the top right of the original image for removing the entire image group
                delete_button = QPushButton("✖")
                delete_button.setFixedSize(48, 48)
                delete_button.setStyleSheet("color: white; background-color: #1976D2; border-radius: 12px;")
                delete_button.clicked.connect(lambda _, folder=group_folder: self.confirm_delete(folder))
                # Add to layout
                container_layout.addWidget(delete_button, 0, 0, Qt.AlignTop | Qt.AlignRight)

                # Set the cursor to hand on the original image to indicate it is clickable
                image_label.setCursor(Qt.PointingHandCursor)
                image_label.mousePressEvent = lambda event, img_name=image_name: self.go_to_editor.emit(img_name)

            # Add to page
            main_layout.addWidget(container, row, col, Qt.AlignCenter)

    def confirm_delete(self, folder_path):
        """
        Prompts the user for confirmation to delete an image group folder. Deletes
        the folder and refreshes the page if the user confirms.

        Parameters:
            folder_path (Path): The path to the folder containing the image group to be deleted.
        """

        # Prompt user to delete the entire folder
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete this image and all its styles?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Delete the entire folder of that image
            shutil.rmtree(folder_path)
            # Refresh workspace to reflect deletion
            self.refresh_page()

    def refresh_page(self):
        """
        Reloads the gallery view to reflect any deletions by reinitializing the layout.
        """

        # Remove existing layout if present
        existing_layout = self.layout()
        if existing_layout:
            QWidget().setLayout(existing_layout)

        # Reinitialize the UI to load updated image groups
        self.initUI()


class EditorPage(QWidget):
    """
    Represents the image editor page, where users can apply various styles, adjustments,
    and effects to an image. This page allows users to control image properties such as
    brightness, contrast, and saturation, apply artistic filters, add frames, and export result.
    """

    # Signals for navigation to other pages
    go_to_main = pyqtSignal()
    go_to_upload = pyqtSignal()
    go_to_workspace = pyqtSignal()
    go_to_gallery = pyqtSignal()

    def __init__(self, selected_image):
        """
        Initializes the EditorPage with the selected image, creating a temporary
        directory for edited images and setting up the user interface components.

        Parameters:
            selected_image (str): The name of the image selected for editing.
        """

        super().__init__()
        self.selected_image = selected_image
        self.temp_dir = Path("temporary_data") / "editor_temp"
        self.sliders = {}
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface with a grid layout for displaying the image
        and controls for selecting styles, adjusting effects, and exporting.
        This layout includes sliders, dropdowns, and action buttons to enhance
        the image-editing experience.
        """

        #####################################################################
        #                                                                                                                                      #
        # Setup Main Layout                                                                                                      #
        #                                                                                                                                      #
        #####################################################################

        # Main layout for the page with padding and spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Add the toolbar for navigation
        self.toolbar = setup_toolbar(
            self,
            self.go_to_main.emit, # Signal for main page
            self.go_to_upload.emit, # Signal for upload page
            self.go_to_workspace.emit, # Signal for workspace page
            self.go_to_gallery.emit # Signal for gallery page
        )
        # Make the toolbar transparent
        self.toolbar.setStyleSheet("background: none;")
        # Toolbar at the top
        main_layout.addWidget(self.toolbar)

        # Title label centered at the top
        description_label = QLabel(
            "Select your Image Style and Customize it further")
        description_label.setFont(QFont("Arial", 15, QFont.Bold))
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("color: #555555; background: none;")
        description_label.setWordWrap(True)
        # Add to the page
        main_layout.addWidget(description_label)

        # Scrollable area for main content with padding and spacing
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        grid_layout = QGridLayout(content_widget)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(30)
        # Set column stretches: 2 for the left side (image and style), 1 for the right side (editor controls)
        grid_layout.setColumnStretch(0, 2)
        grid_layout.setColumnStretch(1, 1)
        # Set row stretches for height proportions: 4 for the image, 1 for two rows below
        grid_layout.setRowStretch(0, 4)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setRowStretch(2, 1)

        # Set background color for the page
        self.setStyleSheet("background-color: #f7f9fc;")

        #####################################################################
        #                                                                                                                                      #
        # Content Layout                                                                                                            #
        #                                                                                                                                      #
        #####################################################################

        # Add sliders
        def add_slider(label, default_value, layout, callback, min_value=0, max_value=100, step=1):
            """
            Creates and adds a slider to the specified layout with a label for different
            image adjustments or effects. Configures slider properties, callback connections,
            and additional elements like dropdowns for specific sliders (e.g., Tint color).

            Parameters:
                label (str): The label for the slider, describing its purpose (e.g., "Brightness").
                default_value (int): The default starting value of the slider.
                layout (QLayout): The layout to which the slider and related components are added.
                callback (function): The function to be called when the slider's value changes.
                min_value (int): The minimum slider value. Default is 0.
                max_value (int): The maximum slider value. Default is 100.
                step (int): The incremental step size for the slider. Default is 1.
            """

            # Depending on the label, create different layouts
            if label=="Transition":
                # Large centered label above the transition slider
                slider_label = QLabel(label)
                slider_label.setFont(QFont("Arial", 12))
                slider_label.setAlignment(Qt.AlignHCenter)
                # Add to layout
                layout.addWidget(slider_label)
            elif label in ("Exposure", "Gamma", "Brightness", "Contrast", "Saturation", "Hue", "Temperature", "Sharpness"):
                # Small centered labels left of the main editing sliders
                slider_label = QLabel(label)
                slider_label.setFont(QFont("Arial", 7))
                slider_label.setAlignment(Qt.AlignCenter)
                # Add to layout
                layout.addWidget(slider_label)
            elif label == "Tint":
                # For the Tint slider, add a dropdown for selecting tint color to the right
                color_dropdown = QComboBox()
                colors = [
                    ("Pink", "#FF69B4"), ("Red", "#FF0000"), ("Orange", "#FFA500"),
                    ("Yellow", "#FFFF00"), ("Green", "#008000"), ("Cyan", "#00FFFF"),
                    ("Blue", "#0000FF"), ("Purple", "#800080"), ("Gray", "#808080")]
                # Populate dropdown with colors and hex codes
                for name, hex_color in colors:
                    color_dropdown.addItem(name, hex_color)
                # Initially disabled
                color_dropdown.setEnabled(False)
                # Connect dropwdown to the function to change
                color_dropdown.currentIndexChanged.connect(
                    lambda index, dropdown=color_dropdown: self.set_tint_color(dropdown.itemData(index)))
                # Enable or disable the dropdown based on Tint checkbox state
                checkbox.stateChanged.connect(lambda state, dropdown=color_dropdown: dropdown.setEnabled(state == Qt.Checked))
                # Track the dropdown
                self.dropdowns[label] = color_dropdown
                # Add to layout
                layout.addWidget(color_dropdown)

            # Slider setup
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_value, max_value)
            slider.setValue(default_value)
            slider.setSingleStep(step)
            slider.valueChanged.connect(callback)
            # For specific filters, disable slider until checkbox is checked
            if label in ("Blur", "Posterize", "Solarize", "Noise", "Tint", "Paper Texture"):
                slider.setEnabled(False)
                slider.valueChanged.connect(self.apply_all_adjustments)
                checkbox.stateChanged.connect(lambda state, s=slider: s.setEnabled(state == Qt.Checked))
            # Add to layout
            layout.addWidget(slider)

            # Ensure Transition slider is centered by adding a spacer below
            if label == "Transition":
                spacer = QLabel("     ")
                layout.addWidget(spacer)

            # Track the sliders
            self.sliders[label] = slider

        #####################################################################
        # Left Side - Top                                                                                                             #
        #####################################################################

        # Setup the image display section
        self.image_display_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_display_layout.addWidget(self.image_label)
        # Add to page
        grid_layout.addLayout(self.image_display_layout, 0, 0)

        #####################################################################
        # Left Side - Bottom                                                                                                        #
        #####################################################################

        # Style selection title
        style_layout = QVBoxLayout()
        style_label = QLabel("Select Style")
        style_label.setFont(QFont("Arial", 12))
        style_label.setAlignment(Qt.AlignCenter)
        # Add to layout
        style_layout.addWidget(style_label)

        # Style selection dropwdown
        self.style_dropdown = QComboBox()
        self.style_dropdown.addItems([style.capitalize() for style in ["original", "cezanne", "monet", "ukiyoe", "vangogh"]])
        self.style_dropdown.setStyleSheet("padding: 5px;")
        self.style_dropdown.currentIndexChanged.connect(self.update_image_display)
        # Add to layout
        style_layout.addWidget(self.style_dropdown)

        # Add style selection to page
        grid_layout.addLayout(style_layout, 1, 0)

        # Transition title and slider
        style_transition_layout = QVBoxLayout()
        style_transition_layout.setAlignment(Qt.AlignTop)
        add_slider("Transition", 100, style_transition_layout, self.apply_all_adjustments)

        # Add transition to page
        grid_layout.addLayout(style_transition_layout, 2, 0)

        #####################################################################
        # Right Side (Top)                                                                                                           #
        #####################################################################

        # Editor controls layout for image adjustments and filters
        editor_controls_layout = QVBoxLayout()
        editor_controls_layout.setAlignment(Qt.AlignTop)
        self.filters_enabled = {}
        self.dropdowns = {}

        # Filter title
        filter_layout = QVBoxLayout()
        filter_label = QLabel("Filters")
        filter_label.setFont(QFont("Arial", 12))
        # Add to layout
        filter_layout.addWidget(filter_label)

        # Horizontal layour for Sepia, Grayscale, and Colorize filters
        color_filters_layout = QHBoxLayout()
        for filter_name in ["Sepia", "Grayscale", "Colorize", "Invert"]:
            # Setup each checkbox
            checkbox = QCheckBox(filter_name)
            checkbox.setStyleSheet("font-size: 18px;")
            checkbox.stateChanged.connect(self.apply_all_adjustments)
            # Add to layout
            color_filters_layout.addWidget(checkbox)
            # Keep a list of all checkboxes
            self.filters_enabled[filter_name] = checkbox
        # Add to layout
        filter_layout.addLayout(color_filters_layout)

        # Other filters with individual sliders
        for filter_name, slider_params in [
            ("Blur", (50, 0, 100)),
            ("Posterize", (1, 1, 8)),
            ("Solarize", (0, 0, 255)),
            ("Noise", (5, 0, 50)),
            ("Tint", (30, 0, 100)),
            ("Paper Texture", (0, 0, 50))]:
            # Setup each checkbox
            inner_filter_layout = QHBoxLayout()
            checkbox = QCheckBox(filter_name)
            checkbox.setStyleSheet("font-size: 18px;")
            checkbox.stateChanged.connect(self.apply_all_adjustments)
            # Add to layout
            inner_filter_layout.addWidget(checkbox)
            # Setup each slider
            add_slider(filter_name, slider_params[0], inner_filter_layout, self.apply_all_adjustments, slider_params[1], slider_params[2])
            # Add to layout
            filter_layout.addLayout(inner_filter_layout)
            # Keep a list of all checkboxes
            self.filters_enabled[filter_name] = checkbox
        # Add to layout
        editor_controls_layout.addLayout(filter_layout)

        # Editor title
        editing_filter_layout = QVBoxLayout()
        editing_filter_label = QLabel("Editing")
        editing_filter_label.setFont(QFont("Arial", 12))
        # Add to layout
        editing_filter_layout.addWidget(editing_filter_label)

        # Editing sliders
        for filter_name, slider_param in [
            ("Exposure", 50),
            ("Gamma", 50),
            ("Brightness", 50),
            ("Contrast", 50),
            ("Saturation", 50),
            ("Hue", 50),
            ("Temperature", 50),
            ("Sharpness", 50)]:
            # Setup each checkbox
            inner_editing_filter_layout = QHBoxLayout()
            # Setup each slider
            add_slider(filter_name, slider_param, inner_editing_filter_layout, self.apply_all_adjustments)
            # Add to layout
            editing_filter_layout.addLayout(inner_editing_filter_layout)
        # Add to layout
        editor_controls_layout.addLayout(editing_filter_layout)

        # Add editor controls to page
        grid_layout.addLayout(editor_controls_layout, 0, 1)

        #####################################################################
        # Right Side (Bottom)                                                                                                     #
        #####################################################################

        # Frame controls layout
        frame_controls_layout = QVBoxLayout()
        frame_controls_layout.setAlignment(Qt.AlignTop)

        # Frame selection title
        frame_label = QLabel("Frame Style")
        frame_label.setFont(QFont("Arial", 12))
        # Add to layout
        frame_controls_layout.addWidget(frame_label)

        # Frame selection dropdown
        self.frame_dropdown = QComboBox()
        self.frame_dropdown.addItems(["None", "Black", "White", "Gold", "Metallic"])
        self.frame_dropdown.setStyleSheet("padding: 5px;")
        self.frame_dropdown.currentIndexChanged.connect(self.apply_all_adjustments)
        # Track the dropdown
        self.dropdowns["Frame"] = self.frame_dropdown
        # Add to layout
        frame_controls_layout.addWidget(self.frame_dropdown)

        # Add frame controls to page
        grid_layout.addLayout(frame_controls_layout, 1, 1)

        # Export controls layout
        export_controls_layout = QVBoxLayout()
        export_controls_layout.setAlignment(Qt.AlignTop)

        # Export title
        export_label = QLabel("Export")
        export_label.setFont(QFont("Arial", 12))
        # Add to layout
        export_controls_layout.addWidget(export_label)

        # Export buttons
        button_pane = QWidget()
        button_layout = QVBoxLayout(button_pane)
        # Save to Gallery Button
        self.save_button = QPushButton("Save to Gallery")
        self.save_button.setFont(QFont("Arial", 12))
        self.save_button.setStyleSheet("background-color: #1976D2; color: white; padding: 10px; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_to_gallery)
        # Add to layout
        button_layout.addWidget(self.save_button, alignment=Qt.AlignBottom)
        # Export Button
        self.export_button = QPushButton("Export Current Image")
        self.export_button.setFont(QFont("Arial", 12))
        self.export_button.setStyleSheet("background-color: #1976D2; color: white; padding: 10px; border-radius: 5px;")
        self.export_button.clicked.connect(self.export_image)
        # Add to layout
        button_layout.addWidget(self.export_button, alignment=Qt.AlignBottom)
        # Add to layout
        export_controls_layout.addWidget(button_pane)
        # Overlay message for the buttons (hidden by default)
        self.overlay_message = QLabel("", button_pane)
        self.overlay_message.setFont(QFont("Arial", 14.5))
        self.overlay_message.setStyleSheet("background-color: #0F4C81; color: white; padding: 8px 16px; border-radius: 8px;")
        self.overlay_message.setAlignment(Qt.AlignCenter)
        self.overlay_message.setVisible(False)

        # Add export controls to page
        grid_layout.addLayout(export_controls_layout, 2, 1)

        #####################################################################
        #                                                                                                                                      #
        # Set Layout                                                                                                                    #
        #                                                                                                                                      #
        #####################################################################

        # Set the scroll area to contain all content
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Set Layout
        self.setLayout(main_layout)

        # Find original image
        baseline_image_path = Path(f"database/workspace/{self.selected_image}/{self.selected_image}_original.png")
        # Ensure temp directory exists
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir()
        # Save enlarged original image in a temp path
        resized_image = QPixmap(str(baseline_image_path)).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        temp_path_baseline = self.temp_dir / "baseline.png"
        resized_image.save(str(temp_path_baseline))
        # Open the resized original image
        self.baseline_image = Image.open(str(temp_path_baseline)).convert("RGB")
        # Update display to show the original image
        self.update_image_display()

    def update_image_display(self):
        """
        Refreshes the display to show the selected styled version of the image.
        """

        # Set up a temporary folder for editing and clear it if it already exists
        self.temp_subfolder = self.temp_dir / "editing"
        if self.temp_subfolder.exists():
            shutil.rmtree(self.temp_subfolder)
        self.temp_subfolder.mkdir()

        # Get the path for the selected style image
        selected_style = self.style_dropdown.currentText().lower()
        image_path = Path(f"database/workspace/{self.selected_image}/{self.selected_image}_{selected_style}.png")

        # Load, resize, and save the image in the temporary editing folder
        resized_image = QPixmap(str(image_path)).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        temp_path_original = self.temp_subfolder / "original.png"
        resized_image.save(str(temp_path_original))
        self.original_image = Image.open(str(temp_path_original)).convert("RGB")

        # Reset sliders to default values for each adjustment control
        for key, value in self.sliders.items():
            if key == "Transition":
                value.setValue(100)
            elif key == "Posterize":
                value.setValue(1)
            elif key == "Solarize" or key=="Paper Texture":
                value.setValue(0)
            elif key == "Noise":
                value.setValue(10)
            elif key == "Tint":
                value.setValue(30)
            else:
                value.setValue(50)
        # Reset checkboxes to unchecked state
        for key, value in self.filters_enabled.items():
            value.setChecked(False)
        # Reset dropdowns to default selection
        for key, value in self.dropdowns.items():
            value.setCurrentIndex(0)
            self.set_tint_color(value.itemData(0))

        # Apply all adjustments to update the display
        self.apply_all_adjustments()

    def apply_all_adjustments(self):
        """
        Applies a series of image adjustments and effects based on the user's selections and slider values.
        Adjustments include blending, filters, and various editing parameters like exposure, contrast,
        and hue. The final processed image is saved temporarily and displayed in the application.
        """

        # LOAD IMAGES: the original and styled images are loaded as the base for adjustments
        original_image = self.baseline_image.copy()
        styled_image = self.original_image.copy()

        # BLENDING: Blend original and styled images based on the transition slider value
        blend_value = self.sliders["Transition"].value() / 100.0
        blended_image = Image.blend(original_image, styled_image, blend_value)
        # Start adjustments with the blended image as the initial base
        adjusted_image = blended_image

        # FILTERS: Apply various filters if enabled
        # Invert
        if self.filters_enabled["Invert"].isChecked():
            adjusted_image = self.apply_invert(adjusted_image)
        # Grayscale
        if self.filters_enabled["Grayscale"].isChecked():
            adjusted_image = self.apply_grayscale(adjusted_image)
        # Solarize
        if self.filters_enabled["Solarize"].isChecked():
            threshold = self.sliders["Solarize"].value()
            adjusted_image = self.apply_solarize(adjusted_image, threshold)
        # Sepia
        if self.filters_enabled["Sepia"].isChecked():
            adjusted_image = self.apply_sepia(adjusted_image)
        # Colorize
        if self.filters_enabled["Colorize"].isChecked():
            adjusted_image = self.apply_colorize(adjusted_image)
        # Posterize
        if self.filters_enabled["Posterize"].isChecked():
            posterize_bits = self.sliders["Posterize"].value()
            adjusted_image = self.apply_posterize(adjusted_image, posterize_bits)
        # Noise
        if self.filters_enabled["Noise"].isChecked():
            noise_intensity = self.sliders["Noise"].value() / 100
            adjusted_image = self.apply_noise(adjusted_image, noise_intensity)
        # Tint
        if self.filters_enabled["Tint"].isChecked():
            alpha = self.sliders["Tint"].value() / 100
            adjusted_image = self.apply_tint(adjusted_image, alpha=alpha)
        # Blur
        if self.filters_enabled["Blur"].isChecked():
            blur_intensity = self.sliders["Blur"].value() / 5
            adjusted_image = self.apply_blur(adjusted_image, blur_intensity)

        # EDITING: Adjust exposure, gamma, brightness, contrast, saturation, hue, temperature, and sharpness
        # Exposure
        exposure_value = self.sliders["Exposure"].value() / 50.0
        adjusted_image = ImageEnhance.Brightness(adjusted_image).enhance(exposure_value)
        # Gamma
        gamma_value = max(0.1, self.sliders["Gamma"].value() / 50.0)
        inv_gamma = 1.0 / gamma_value
        adjusted_image = adjusted_image.point(lambda p: 255 * ((p / 255) ** inv_gamma))
        # Brightness
        brightness_value = self.sliders["Brightness"].value() / 50.0
        adjusted_image = ImageEnhance.Brightness(adjusted_image).enhance(brightness_value)
        # Contrast
        contrast_value = self.sliders["Contrast"].value() / 50.0
        adjusted_image = ImageEnhance.Contrast(adjusted_image).enhance(contrast_value)
        # Saturation
        saturation_value = self.sliders["Saturation"].value() / 50.0
        adjusted_image = ImageEnhance.Color(adjusted_image).enhance(saturation_value)
        # Hue
        hue_shift = (self.sliders["Hue"].value() - 50) * 3.6
        hsv_image = adjusted_image.convert("HSV")
        h, s, v = hsv_image.split()
        h = h.point(lambda p: (p + hue_shift) % 256)
        adjusted_image = Image.merge("HSV", (h, s, v)).convert("RGB")
        # Temperature
        temperature_shift = self.sliders["Temperature"].value() - 50
        r, g, b = adjusted_image.split()
        if temperature_shift > 0:
            r = r.point(lambda p: min(255, p + temperature_shift))
        else:
            b = b.point(lambda p: min(255, p - temperature_shift))
        adjusted_image = Image.merge("RGB", (r, g, b))
        # Sharpness
        sharpness_value = self.sliders["Sharpness"].value() / 10.0 + 1
        adjusted_image = ImageEnhance.Sharpness(adjusted_image).enhance(sharpness_value)

        # Paper Texture
        if self.filters_enabled["Paper Texture"].isChecked():
            paper_texture_intensity = self.sliders["Paper Texture"].value() / 100.0
            if paper_texture_intensity > 0:
                paper_texture = self.generate_paper_texture(adjusted_image.size, paper_texture_intensity)
                adjusted_image = Image.blend(adjusted_image, paper_texture, paper_texture_intensity)

        # FRAMES: Apply a frame to the image if selected
        adjusted_image = self.apply_frame(adjusted_image)

        # SAVE AND DISPLAY: Save the adjusted image temporarily and update the display
        self.temp_path_edit = self.temp_subfolder / "edit.png"
        adjusted_image.save(str(self.temp_path_edit))
        pixmap = QPixmap(str(self.temp_path_edit))
        self.image_label.setPixmap(pixmap)

    # CREATED BY CHATGPT
    def apply_sepia(self, image):
        """
        Applies a sepia filter to the input image by transforming RGB values to sepia tones.
        Each pixel is modified using specific coefficients to achieve the sepia effect.

        Parameters:
            image (PIL.Image): The original image to apply the sepia effect on.

        Returns:
            PIL.Image: A new image with the sepia filter applied.
        """

        # Convert the image and load it
        sepia_image = image.convert("RGB")
        pixels = sepia_image.load()

        # Loop through each pixel and apply sepia transformations
        for y in range(sepia_image.size[1]):
            for x in range(sepia_image.size[0]):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = min(tr, 255), min(tg, 255), min(tb, 255)

        # Return edited image
        return sepia_image

    # CREATED BY CHATGPT
    def apply_grayscale(self, image):
        """
        Converts the input image to grayscale.

        Parameters:
            image (PIL.Image): The original image to be converted.

        Returns:
            PIL.Image: A new image converted to grayscale and back to RGB for consistent handling.
        """

        # Convert the image and return it
        return image.convert("L").convert("RGB")

    # CREATED BY CHATGPT
    def apply_blur(self, image, blur_radius=2):
        """
        Applies a Gaussian blur filter to the input image.

        Parameters:
            image (PIL.Image): The original image to apply the blur effect on.
            blur_radius (int, optional): The radius of the Gaussian blur. Default is 2.

        Returns:
            PIL.Image: A new image with the blur effect applied.
        """

        # Edit the image and return it
        return image.filter(ImageFilter.GaussianBlur(blur_radius))

    # CREATED BY CHATGPT
    def apply_posterize(self, image, bits=4):
        """
        Applies a posterize effect to the input image by reducing the number of bits per channel.

        Parameters:
            image (PIL.Image): The original image to apply the posterize effect on.
            bits (int, optional): The number of bits per color channel. Default is 4.

        Returns:
            PIL.Image: A new image with the posterize effect applied.
        """

        # Ensure the bits are within a reasonable range (e.g., 1 to 8)
        bits = int(bits)
        # Apply posterize with the specified bit level
        posterized_image = ImageOps.posterize(image, bits)

        # Return the edited image
        return posterized_image

    # CREATED BY CHATGPT
    def apply_invert(self, image):
        """
        Inverts the colors of the input image.

        Parameters:
            image (PIL.Image): The original image to apply the invert effect on.

        Returns:
            PIL.Image: A new image with colors inverted.
        """

        # Edit the image and return it
        return ImageOps.invert(image.convert("RGB"))

    # CREATED BY CHATGPT
    def apply_solarize(self, image, threshold=128):
        """
        Applies a solarize effect to the image, inverting all pixels above a certain threshold.

        Parameters:
            image (PIL.Image): The original image to apply the solarize effect on.
            threshold (int, optional): The pixel intensity threshold to determine inversion. Default is 128.

        Returns:
            PIL.Image: The solarized image.
        """

        # Convert the image and return it
        return ImageOps.solarize(image, threshold)

    # CREATED BY CHATGPT
    def apply_colorize(self, image, black_color="blue", white_color="yellow"):
        """
        Colorizes a grayscale version of the image using specified colors for black and white.

        Parameters:
            image (PIL.Image): The original image to apply colorization on.
            black_color (str, optional): The color to use for black areas in the image. Default is "blue".
            white_color (str, optional): The color to use for white areas in the image. Default is "yellow".

        Returns:
            PIL.Image: A colorized version of the image.
        """

        # Cinvert image to grayscale
        grayscale = image.convert("L")

        # Edit the image and return it
        return ImageOps.colorize(grayscale, black=black_color, white=white_color)

    # CREATED BY CHATGPT
    def apply_noise(self, image, intensity=0.05):
        """
        Adds random noise to the image, simulating a grainy effect.

        Parameters:
            image (PIL.Image): The original image to add noise to.
            intensity (float, optional): Intensity of the noise, between 0 and 1. Default is 0.05.

        Returns:
            PIL.Image: A new image with the noise effect applied.
        """

        # Convert the image to a NumPy array for pixel manipulation
        np_image = np.array(image)
        # Generate random noise and adjust by the intensity factor
        noise = np.random.normal(0, intensity * 255, np_image.shape).astype(np.int16)
        # Add noise and ensure pixel values are within valid range
        noisy_image = Image.fromarray(np.clip(np_image + noise, 0, 255).astype(np.uint8))

        # Return the edited image
        return noisy_image

    # CREATED BY CHATGPT
    def apply_tint(self, image, alpha=0.3):
        """
        Applies a tint overlay to the image with the selected color.

        Parameters:
            image (PIL.Image): The original image to apply the tint to.
            alpha (float, optional): The opacity level of the tint overlay, between 0 and 1. Default is 0.3.

        Returns:
            PIL.Image: The tinted image.
        """

        # Get RGB values of the selected tint color
        try:
            tint_color = self.tint_color.getRgb()[:3]
        # Default to pink tint if no color is selected
        except:
            self.tint_color = QColor("#FF69B4")
            tint_color = self.tint_color.getRgb()[:3]

        # Create a solid color overlay, blend it with the image and return the edited image
        overlay = Image.new("RGB", image.size, tint_color)
        return Image.blend(image, overlay, alpha)

    # CREATED BY CHATGPT
    def generate_paper_texture(self, size, intensity):
        """
        Generates a subtle paper-like texture with grain.

        Parameters:
            size (tuple): Dimensions of the texture to generate, as (width, height).
            intensity (float): Grain intensity, between 0 and 1.

        Returns:
            PIL.Image: A paper-textured image to overlay on the main image.
        """

        # Create a noise pattern with specified intensity
        texture = np.random.normal(127, 127 * intensity, (size[1], size[0], 3)).astype(np.uint8)
        texture_image = Image.fromarray(texture).convert("RGB")

        # Edit the image and return it
        return texture_image.filter(ImageFilter.GaussianBlur(1))

    # CREATED BY CHATGPT
    def apply_basic_frame(self, image, frame_color="Black", frame_width=20, canvas_size=(800, 800)):
        """
        Adds a basic frame around the image by resizing it to fit within the frame dimensions.

        Parameters:
            image (PIL.Image): The image to frame.
            frame_color (str, optional): The color of the frame (e.g., "Black", "White", "Gold", "Metallic"). Default is "Black".
            frame_width (int, optional): The width of the frame in pixels. Default is 20.
            canvas_size (tuple, optional): The size of the entire canvas (frame + image) in pixels. Default is (800, 800).

        Returns:
            PIL.Image: The image with a basic frame applied.
        """

        # Map frame color names to color values
        if frame_color == "Black":
            frame_color = "black"
        elif frame_color == "White":
            frame_color = "white"
        elif frame_color == "Metallic":
            frame_color = "#C0C0C0"
        elif frame_color == "Gold":
            frame_color = "#FFD700"

        # Calculate the inner dimensions of the framed area to determine cropping
        inner_width = canvas_size[0] - 2 * frame_width
        inner_height = canvas_size[1] - 2 * frame_width

        # Center crop the image to fit within the frame
        top = (image.height - inner_height) // 2
        left = (image.width - inner_width) // 2
        right = left + inner_width
        bottom = top + inner_height
        cropped_image = image.crop((left, top, right, bottom))

        # Create a new canvas with the frame color and paste the cropped image onto it
        framed_image = Image.new("RGB", canvas_size, frame_color)
        framed_image.paste(cropped_image, (frame_width, frame_width))

        # Return the edited image
        return framed_image

    def set_tint_color(self, color_hex):
        """"
        Sets the chosen tint color and applies it to the current image.

        Parameters:
            color_hex (str): Hexadecimal color code for the tint (e.g., "#FF69B4").
        """

        # Sets the chosen color
        self.tint_color = QColor(color_hex)

        # Apply the chosen color to the current image
        self.apply_all_adjustments()

    def apply_frame(self, image):
        """
        Applies a frame to the image based on the user's selection from the dropdown.

        Parameters:
            image (PIL.Image): The original image to which the frame will be applied.

        Returns:
            PIL.Image: The image with the selected frame applied.
        """

        # Get the selected frame style from the dropdown
        frame_style = self.frame_dropdown.currentText()

        # Apply and return frame depending on the selection
        if frame_style in ["Black", "White", "Gold", "Metallic"]:
            return self.apply_basic_frame(image, frame_style)

        # If no valid frame style is selected, return the original image
        return image

    def save_to_gallery(self):
        """
        Saves the currently edited image to the gallery along with the original version
        if it is not already present in the gallery (so each edited image coming from an
        original will be stored together with the original).
        """

        # Set up the user folder path and the group folder for the selected image
        user_folder = Path("database/gallery")
        group_folder = user_folder / self.selected_image

        # If the folder doesn't already exist
        if not group_folder.exists():
            # Create a new folder for the image group
            group_folder.mkdir()
            # Save the original image in the newly created folder
            new_original_path = group_folder / f"{self.selected_image}_original.png"
            self.baseline_image.save(new_original_path)

        # Generate a unique identifier for the edited image based on time and UUID
        unique_id = f"{int(time.time_ns())}_{uuid.uuid4().hex[:6]}"
        new_edit_path = group_folder / f"{self.selected_image}_{unique_id}.png"
        # Copy the edited image from its temporary location to the gallery folder
        shutil.copy(self.temp_path_edit, new_edit_path)
        # Show an overlay message confirming the image has been saved
        self.show_overlay_message("Image saved to Gallery.", "gallery")

    def show_overlay_message(self, message, location, duration=5000):
        """
        Displays a temporary overlay message above a specified button for a set duration.

        Parameters:
            message (str): The message to display in the overlay.
            location (str): Indicating what button to use.
            duration (int): Time in milliseconds to keep the message visible.
        """

        # Disable the toolbar to prevent interactions while the message is displayed
        self.toolbar.setDisabled(True)

        # Bring the overlay message QLabel to the front and update its text and visibility
        self.overlay_message.raise_()
        self.overlay_message.setText(message)
        self.overlay_message.setVisible(True)

        # Position the overlay message directly above the specified button
        if location == "gallery":
            button_geometry = self.save_button.geometry()
        else:
            button_geometry = self.export_button.geometry()
        x = button_geometry.left()
        y = button_geometry.top()
        self.overlay_message.setGeometry(x, y, button_geometry.width(), button_geometry.height())

        # Hide the overlay message after the specified duration and re-enable the toolbar
        QTimer.singleShot(duration, lambda: self.hide_overlay_message())

    def hide_overlay_message(self):
        """
        Hides the overlay message and re-enables the toolbar for user interaction.
        """

        # Set the overlay message to invisible
        self.overlay_message.setVisible(False)

        # Re-enable the toolbar to restore user interactions
        self.toolbar.setDisabled(False)

    def export_image(self):
        """
        Opens a file dialog for the user to save the current image in a chosen format.
        Includes commonly used formats and their variations in extensions.
        """

        # Open file dialog with format options for saving the image
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "JPEG (*.jpg *.jpeg);;PNG (*.png);;BMP (*.bmp);;TIFF (*.tif *.tiff);;WEBP (*.webp)"
        )
        # If a file path is chosen
        if file_path:
            # Open and save the image to the selected path
            Image.open(self.temp_path_edit).save(file_path)
            # Show a message confirming export success
            self.show_overlay_message("Image exported.", "export")

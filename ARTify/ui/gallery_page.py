"""
This file defines the `GalleryPage` class for the Art Studio App, which serves as a
comprehensive interface for users to view, manage, and export their styled images.
"""

# Import PyQT5 for GUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QGridLayout, QScrollArea, QPushButton, QCheckBox, QSlider, QMessageBox, QStackedLayout, QHBoxLayout, QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QFont

# Import libraries
from PIL import Image
from pathlib import Path
from datetime import datetime
import shutil
import cv2
import numpy as np

# Import toolbar
from ui.toolbar_helper import setup_toolbar


class GalleryPage(QWidget):
    """
    Displays a gallery of user-uploaded and processed images. Users can view,
    switch between styles, and export images or animations (transition or
    before/after effects). Provides options to delete images and manage styles.
    """

    # Signals for navigation to other pages
    go_to_main = pyqtSignal()
    go_to_upload = pyqtSignal()
    go_to_workspace = pyqtSignal()
    go_to_gallery = pyqtSignal()

    def __init__(self):
        """
        Initializes the GalleryPage layout, setting up a toolbar, description,
        and a scrollable area displaying each image in a grid layout.
        """

        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the gallery page with a toolbar, title, and grid of images.
        If no images are available, displays a message to inform the user.
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
            "View your Masterpieces")
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
        self.thumbnail_size = 400

        #####################################################################
        #                                                                                                                                      #
        # Content Layout                                                                                                            #
        #                                                                                                                                      #
        #####################################################################

        # Look for processed images in the gallery folder
        gallery_folder = Path("database/gallery")
        image_folders = sorted(gallery_folder.glob("*/"),
                                              key=lambda folder: max((file.stat().st_mtime for file in folder.glob("*")), default=0),
                                              reverse=True)
        # If processed images are found
        if image_folders:
            row = 0

            # Iterate through all image folders
            for folder in image_folders:

                # Create a container with no margins for each image
                container = QWidget()
                container_layout = QGridLayout(container)
                # Add to layout
                container_layout.setContentsMargins(0, 0, 0, 0)

                # Spacer above the image
                spacer = QLabel("     ")
                spacer.setStyleSheet("background: none;")
                # Add to layout
                container_layout.addWidget(spacer, 0, 0, Qt.AlignCenter)

                # Display the original image
                original_image_path = folder / f"{folder.name}_original.png"
                image_label = QLabel()
                pixmap = QPixmap(str(original_image_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(pixmap)
                # Add to layout
                container_layout.addWidget(image_label, 1, 1, Qt.AlignTop | Qt.AlignHCenter)

                # Spacer below the image
                spacer_2 = QLabel("     ")
                spacer_2.setStyleSheet("background: none;")
                # Add to layout
                container_layout.addWidget(spacer_2, 2, 2, Qt.AlignCenter)

                # Delete button over the original image to remove the entire image set
                delete_button = QPushButton("✖")
                delete_button.setFixedSize(48, 48)
                delete_button.setStyleSheet("color: white; background-color: #1976D2; border-radius: 12px;")
                delete_button.clicked.connect(lambda _, f=folder: self.confirm_delete_all(f))
                # Add to layout
                container_layout.addWidget(delete_button, 1, 1, Qt.AlignTop | Qt.AlignRight)

                # Styled image display
                styled_image_label = QLabel()
                # Add to layout
                container_layout.addWidget(styled_image_label, 1, 2, Qt.AlignTop | Qt.AlignHCenter)
                # Dropdown for selecting styles
                style_dropdown = QComboBox()
                style_images = sorted((img for img in folder.glob(f"{folder.name}_*.png") if "original" not in str(img)),
                                                    key=lambda img: img.stat().st_mtime,
                                                    reverse=True)
                for style_image in style_images:
                    # display each style with the last update date/time
                    timestamp = style_image.stat().st_mtime
                    date_time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    style_dropdown.addItem(date_time_str, str(style_image))
                # Set default display for styled image
                if style_images:
                    newest_image_path = style_images[0]
                    pixmap = QPixmap(str(newest_image_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    styled_image_label.setPixmap(pixmap)
                # Update displayed image on style change
                style_dropdown.currentIndexChanged.connect(lambda _, lbl=styled_image_label, dropdown=style_dropdown: self.update_image(lbl, dropdown))

                # Editor pane for styling and exporting options
                editor_pane = self.create_editor_pane(style_dropdown, styled_image_label, original_image_path)
                # Add to layout
                container_layout.addWidget(editor_pane, 1, 3, Qt.AlignTop)

                # Add to page
                grid_layout.addWidget(container, row, 0, Qt.AlignCenter)
                row += 1

        # If no processed images are found
        else:
            # Message displayed when no images are available
            no_images_label = QLabel("No images in gallery")
            no_images_label.setFont(QFont("Arial", 14))
            no_images_label.setAlignment(Qt.AlignCenter)
            no_images_label.setStyleSheet("color: #555555;")
            no_images_label.setWordWrap(True)
            # Add to page
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

    def create_editor_pane(self, style_dropdown, styled_image_label, original_image_path):
        """
        Creates an editor pane with options for transitions, exporting images, and exporting animations.

        Parameters:
            style_dropdown (QComboBox): Dropdown widget for selecting different image styles.
            styled_image_label (QLabel): QLabel widget to display the styled image.
            original_image_path (Path): Path to the original image file.

        Returns:
            QWidget: A QWidget containing the editor pane layout.
        """

        # Create an editor layout to hold everything
        editor_pane = QWidget()
        editor_layout = QVBoxLayout(editor_pane)

        # Overlay message label (initially hidden)
        overlay_message = QLabel("", editor_pane)
        overlay_message.setFont(QFont("Arial", 7))
        overlay_message.setStyleSheet("background-color: #0F4C81; color: white; padding: 8px 16px; border-radius: 8px;")
        overlay_message.setAlignment(Qt.AlignCenter)
        overlay_message.setVisible(False)

        #####################################################################
        # Style selection and delete button                                                                                  #
        #####################################################################

        # Style selection and delete button layout
        dropdown_layout = QHBoxLayout()

        # Dropdown for style selection
        dropdown_label = QLabel("Select image version:")
        dropdown_label.setFont(QFont("Arial", 8))
        dropdown_layout.addWidget(dropdown_label)
        dropdown_layout.addWidget(style_dropdown)

        # Delete button next to the dropdown for removing styles
        delete_button_style = QPushButton("✖")
        delete_button_style.setFixedSize(48, 48)
        delete_button_style.setStyleSheet("color: white; background-color: #1976D2; border-radius: 12px;")
        delete_button_style.clicked.connect(
            lambda _, img_label=styled_image_label, dropdown=style_dropdown: self.confirm_delete_image(dropdown.currentData()))
        # Add to layout
        dropdown_layout.addWidget(delete_button_style)

        # Add to page
        editor_layout.addLayout(dropdown_layout)

        #####################################################################
        # Transition and before/after effects                                                                               #
        #####################################################################

        # Transition effect with a checkbox and slider
        transition_layout = QHBoxLayout()
        transition_checkbox = QCheckBox("Enable Transition")
        transition_checkbox.setObjectName("transition_checkbox")
        transition_slider = QSlider(Qt.Horizontal)
        transition_slider.setRange(0, 100)
        transition_slider.setValue(50)
        transition_slider.setEnabled(False)
        transition_slider.valueChanged.connect(lambda value: self.update_transition(
            value, styled_image_label,
            QPixmap(str(original_image_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(style_dropdown.currentData()).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)))

        # Before-After effect with a checkbox and slider
        before_after_layout = QHBoxLayout()
        before_after_checkbox = QCheckBox("Before/After")
        before_after_checkbox.setObjectName("before_after_checkbox")
        before_after_slider = QSlider(Qt.Horizontal)
        before_after_slider.setRange(0, 100)
        before_after_slider.setValue(50)
        before_after_slider.setEnabled(False)
        before_after_slider.valueChanged.connect(lambda value: self.update_before_after(
            value, styled_image_label,
            QPixmap(str(original_image_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(style_dropdown.currentData()).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)))

        # Stylesheet settings for active and disabled buttons
        active_button_stylesheet = (
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }")
        disabled_button_stylesheet = (
            "QPushButton { background-color: grey; color: white; padding: 8px 16px; border-radius: 8px; }")

        # Export Transition button
        export_transition_button = QPushButton("Export Transition")
        export_transition_button.setFont(QFont("Arial", 7))
        export_transition_button.setEnabled(False)
        export_transition_button.setStyleSheet(disabled_button_stylesheet)
        export_transition_button.clicked.connect(lambda: self.export_view(styled_image_label, "Transition", export_transition_button, overlay_message))

        # Export Before/After button
        export_beforeAfter_button = QPushButton("Export Before After")
        export_beforeAfter_button.setFont(QFont("Arial", 7))
        export_beforeAfter_button.setEnabled(False)
        export_beforeAfter_button.setStyleSheet(disabled_button_stylesheet)
        export_beforeAfter_button.clicked.connect(lambda: self.export_view(styled_image_label, "Before/After", export_beforeAfter_button, overlay_message))

        # Checkbox stateChanged connections for Transition effect
        transition_checkbox.stateChanged.connect(
            lambda state, orig_path=original_image_path: ( # If the checkbox is ticked enable and disable various elements
                export_transition_button.setEnabled(state == Qt.Checked),
                export_transition_button.setStyleSheet(active_button_stylesheet),
                transition_slider.setEnabled(state == Qt.Checked),
                before_after_checkbox.setEnabled(False),
                before_after_slider.setEnabled(False),
                export_beforeAfter_button.setEnabled(False),
                export_beforeAfter_button.setStyleSheet(disabled_button_stylesheet),
                self.apply_transition_effect(orig_path, style_dropdown.currentData(), styled_image_label, transition_slider.value())
            ) if state == Qt.Checked else ( #If the checkbox is unticked enable and disable various elements
                export_transition_button.setEnabled(False),
                export_transition_button.setStyleSheet(disabled_button_stylesheet),
                transition_slider.setEnabled(False),
                before_after_checkbox.setEnabled(True),
                styled_image_label.setPixmap(QPixmap(style_dropdown.currentData()).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))))
        # Add to layout
        transition_layout.addWidget(transition_checkbox)
        transition_layout.addWidget(transition_slider)
        transition_layout.addWidget(export_transition_button)
        # Add to page
        editor_layout.addLayout(transition_layout)

        # Checkbox stateChanged connections for Before/After effect
        before_after_checkbox.stateChanged.connect(
            lambda state, orig_path=original_image_path: ( #If the checkbox is ticked enable and disable various elements
                export_beforeAfter_button.setEnabled(state == Qt.Checked),
                export_beforeAfter_button.setStyleSheet(active_button_stylesheet),
                before_after_slider.setEnabled(state == Qt.Checked),
                transition_checkbox.setEnabled(False),
                transition_slider.setEnabled(False),
                export_transition_button.setEnabled(False),
                export_transition_button.setStyleSheet(disabled_button_stylesheet),
                self.apply_before_after_effect(orig_path, style_dropdown.currentData(), styled_image_label, before_after_slider.value())
            ) if state == Qt.Checked else ( #If the checkbox is unticked enable and disable various elements
                export_beforeAfter_button.setEnabled(False),
                export_beforeAfter_button.setStyleSheet(disabled_button_stylesheet),
                before_after_slider.setEnabled(False),
                transition_checkbox.setEnabled(True),
                styled_image_label.setPixmap(QPixmap(style_dropdown.currentData()).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))))
        # Add to layout
        before_after_layout.addWidget(before_after_checkbox)
        before_after_layout.addWidget(before_after_slider)
        before_after_layout.addWidget(export_beforeAfter_button)
        # Add to page
        editor_layout.addLayout(before_after_layout)

        #####################################################################
        # Export buttons                                                                                                              #
        #####################################################################

        # Button style for export options
        button_style = (
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }"
        )

        # Export Original button
        export_original_button = QPushButton("Export Original")
        export_original_button.setFont(QFont("Arial", 8))
        export_original_button.setStyleSheet(button_style)
        export_original_button.clicked.connect(lambda: self.export_image(
            QPixmap(str(original_image_path)).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "Full Original", export_original_button, overlay_message))
        # Add to page
        editor_layout.addWidget(export_original_button)

        # Export Style button
        export_style_button = QPushButton("Export Style")
        export_style_button.setFont(QFont("Arial", 8))
        export_style_button.setStyleSheet(button_style)
        export_style_button.clicked.connect(lambda: self.export_image(
            QPixmap(style_dropdown.currentData()).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "Full Style", export_style_button, overlay_message))
        # Add to page
        editor_layout.addWidget(export_style_button)

        # GIF Export Buttons
        gif_button_layout = QHBoxLayout()

        # Export Transition GIF button
        transition_gif_button = QPushButton("Export Transition GIF")
        transition_gif_button.setFont(QFont("Arial", 8))
        transition_gif_button.setStyleSheet(button_style)
        transition_gif_button.clicked.connect(lambda: self.export_animation_gif(
            "Transition", transition_gif_button, overlay_message,
            QPixmap(str(original_image_path)).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(style_dropdown.currentData()).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        # Add to layout
        gif_button_layout.addWidget(transition_gif_button)

        # Export Before/After GIF button
        BefAft_gif_button = QPushButton("Export Before/After GIF")
        BefAft_gif_button.setFont(QFont("Arial", 8))
        BefAft_gif_button.setStyleSheet(button_style)
        BefAft_gif_button.clicked.connect(lambda: self.export_animation_gif(
            "Before/After", BefAft_gif_button, overlay_message,
            QPixmap(str(original_image_path)).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(style_dropdown.currentData()).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        # Add to layout
        gif_button_layout.addWidget(BefAft_gif_button)

        # Add the GIF buttons row to the editor layout
        editor_layout.addLayout(gif_button_layout)

        # Video Export Buttons
        video_button_layout = QHBoxLayout()

        # Export Transition video button
        transition_video_button = QPushButton("Export Transition Video")
        transition_video_button.setFont(QFont("Arial", 8))
        transition_video_button.setStyleSheet(button_style)
        transition_video_button.clicked.connect(lambda: self.export_animation_video(
            "Transition", transition_video_button, overlay_message,
            QPixmap(str(original_image_path)).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(style_dropdown.currentData()).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        # Add to layout
        video_button_layout.addWidget(transition_video_button)

        # Export Before/After video button
        BefAft_video_button = QPushButton("Export Before/After Video")
        BefAft_video_button.setFont(QFont("Arial", 8))
        BefAft_video_button.setStyleSheet(button_style)
        BefAft_video_button.clicked.connect(lambda: self.export_animation_video(
            "Before/After", BefAft_video_button, overlay_message,
            QPixmap(str(original_image_path)).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(style_dropdown.currentData()).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        # Add to layout
        video_button_layout.addWidget(BefAft_video_button)

        # Add the Video buttons row to the editor layout
        editor_layout.addLayout(video_button_layout)

        #####################################################################
        # Return full pane                                                                                                           #
        #####################################################################

        return editor_pane

    def apply_transition_effect(self, original_image_path, styled_image_path, styled_image_label, slider_value):
        """
        Loads both the original and styled images and applies a transition effect using the slider.

        Parameters:
            original_image_path (str): Path to the original image file.
            styled_image_path (str): Path to the styled image file.
            styled_image_label (QLabel): QLabel widget displaying the styled image.
            slider_value (int): Initial position of the slider, representing the blend percentage.
        """

        # Load and scale both original and styled images to the target thumbnail size
        original_pixmap = QPixmap(str(original_image_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        styled_pixmap = QPixmap(styled_image_path).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Apply transition effect based on the slider value
        self.update_transition(slider_value, styled_image_label, original_pixmap, styled_pixmap)

    def update_transition(self, slider_value, styled_image_label, original_pixmap, styled_pixmap):
        """
        Updates the transition effect between the original and styled images based on the slider position.

        Parameters:
            slider_value (int): The current slider position, representing the blend percentage.
            styled_image_label (QLabel): QLabel widget displaying the blended image.
            original_pixmap (QPixmap): The original image pixmap.
            styled_pixmap (QPixmap): The styled image pixmap.
        """

        # Create a new pixmap for the blended image
        blended_pixmap = QPixmap(original_pixmap.size())

        # Draw the original image fully, then overlay with styled image at specified opacity
        painter = QPainter(blended_pixmap)
        painter.drawPixmap(0, 0, original_pixmap)
        painter.setOpacity(slider_value / 100.0)
        painter.drawPixmap(0, 0, styled_pixmap)
        painter.end()

        # Update QLabel to show the blended image
        styled_image_label.setPixmap(blended_pixmap)

    def apply_before_after_effect(self, original_image_path, styled_image_path, styled_image_label, slider_value):
        """
        Loads both the original and styled images and applies an initial before/after effect based on the slider value.

        Parameters:
            original_image_path (str): Path to the original image file.
            styled_image_path (str): Path to the styled image file.
            styled_image_label (QLabel): QLabel widget displaying the styled image.
            slider_value (int): Initial position of the slider, representing the split percentage.
        """

        # Load and scale both original and styled images to the target thumbnail size
        original_pixmap = QPixmap(str(original_image_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        styled_pixmap = QPixmap(styled_image_path).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Apply before/after effect based on the slider value
        self.update_before_after(slider_value, styled_image_label, original_pixmap, styled_pixmap)

    def update_before_after(self, slider_value, styled_image_label, original_pixmap, styled_pixmap):
        """
        Updates the before/after effect by displaying a horizontal split between the original and styled images.

        Parameters:
            slider_value (int): The current slider position, representing the split percentage.
            styled_image_label (QLabel): QLabel widget displaying the combined before/after image.
            original_pixmap (QPixmap): The original image pixmap.
            styled_pixmap (QPixmap): The styled image pixmap.
        """

        # Determine width and height of the image and create a new pixmap for the blended image
        width = original_pixmap.width()
        height = original_pixmap.height()
        blended_pixmap = QPixmap(width, height)
        blended_pixmap.fill(Qt.transparent)
        painter = QPainter(blended_pixmap)

        # Draw left side with original image
        painter.drawPixmap(0, 0, styled_pixmap.copy(0, 0, width * slider_value // 100, height))
        # Draw right side with styled image
        painter.drawPixmap(width * slider_value // 100, 0, original_pixmap.copy(width * slider_value // 100, 0, width - (width * slider_value // 100), height))
        painter.end()

        # Update QLabel to show the before/after effect
        styled_image_label.setPixmap(blended_pixmap)

    def export_view(self, image_label, description, button, overlay):
        """
        Opens a file dialog to allow the user to save the current displayed image in the desired format.

        Parameters:
            image_label (QLabel): QLabel displaying the current image view to be saved.
            description (str): Description for the save dialog, typically indicating image type or purpose.
            button (QPushButton): The button triggering the export action, used for overlay positioning.
            overlay (QLabel): Overlay label for showing export confirmation messages.
        """

        # Open file dialog with format options for saving the image
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save {description}",
            "",
            "JPEG (*.jpg *.jpeg);;PNG (*.png);;BMP (*.bmp);;TIFF (*.tif *.tiff);;WEBP (*.webp)"
        )
        # If a file path is chosen and image is present, save the image
        if file_path and image_label.pixmap():
            # Get the pixmap from the QLabel and save it to the selected path
            pixmap = image_label.pixmap().scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap.save(file_path)
            # Show a message confirming export success
            self.show_overlay_message("Image exported.", button, overlay)

    def export_image(self, image_pixmap, description, button, overlay):
        """
        Opens a file dialog for saving the specified image pixmap in the chosen format.

        Parameters:
            image_pixmap (QPixmap): The pixmap of the image to be saved.
            description (str): Description for the save dialog, typically indicating image type or purpose.
            button (QPushButton): The button triggering the export action, used for overlay positioning.
            overlay (QLabel): Overlay label for showing export confirmation messages.
        """

        # Open file dialog with format options for saving the image
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save {description}",
            "",
            "JPEG (*.jpg *.jpeg);;PNG (*.png);;BMP (*.bmp);;TIFF (*.tif *.tiff);;WEBP (*.webp)"
        )
        # If a file path is chosen
        if file_path:
            # Save the pixmap to the selected path
            image_pixmap.save(file_path)
            # Show a message confirming export success
            self.show_overlay_message("Image exported.", button, overlay)

    def update_image(self, image_label, dropdown):
        """
        Updates the displayed image in `image_label` based on the style selected in the `dropdown`.
        Resets both the transition and before/after checkboxes.

        Parameters:
            image_label (QLabel): QLabel where the selected image will be displayed.
            dropdown (QComboBox): Dropdown containing image styles with paths as data.
        """

        # Retrieve the file path for the selected style
        selected_image_path = dropdown.currentData()

        # Reset transition and before/after checkboxes if they exist in the specific editor pane
        parent_widget = self.sender().parent()
        transition_checkbox = parent_widget.findChild(QCheckBox, "transition_checkbox")
        before_after_checkbox = parent_widget.findChild(QCheckBox, "before_after_checkbox")
        if transition_checkbox:
            transition_checkbox.setChecked(False)
        if before_after_checkbox:
            before_after_checkbox.setChecked(False)

        # Load the selected image and set it in the label
        pixmap = QPixmap(selected_image_path).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

    def confirm_delete_all(self, folder_path):
        """
        Prompts the user with a confirmation dialog to delete an entire image folder. If confirmed,
        deletes the folder and refreshes the gallery view.

        Parameters:
            folder_path (Path): Path to the folder containing the image and all its versions.
        """

        # Ask for confirmation before deleting all images in the folder
        reply = QMessageBox.question(
            self,
            "Delete Image",
            "Are you sure you want to delete this image and all its processed versions?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        # If yes is clicked
        if reply == QMessageBox.Yes:
            # Delete the entire folder of that image
            shutil.rmtree(folder_path)
            # Refresh gallery to reflect deletion
            self.reload_gallery()

    def confirm_delete_image(self, image_path):
        """
        Prompts the user to confirm deletion of a single styled image. If it's the last image in the folder,
        prompts to delete the entire set. Otherwise, deletes only the selected image.

        Parameters:
            image_path (Path): Path to the specific styled image file.
        """

        # Get the folder of the image
        image_file = Path(image_path)
        folder = image_file.parent

        # List all .png images in the folder to check if only 2 (original and one edited) remain
        styled_images = [f for f in folder.glob("*.png")]

        # If only 2 images remain in the folder
        if len(styled_images) <= 2:
            # Prompt user to delete the entire folder if this is the last styled image
            reply = QMessageBox.question(
                self,
                "Delete Entire Image Set",
                "This is the last styled image in this set. Deleting it will also remove the original. Proceed?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # Delete the entire folder of that image
                shutil.rmtree(folder)
                # Refresh gallery to reflect deletion
                self.reload_gallery()
        # If more than 2 images remain in the folder, there are more than one edited
        else:
            # Prompt to delete only the selected styled image
            reply = QMessageBox.question(
                self,
                "Delete Styled Image",
                "Are you sure you want to delete this styled image?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # Delete the specific styled image
                image_file.unlink(missing_ok=True)
                # Refresh gallery to reflect deletion
                self.reload_gallery()

    def reload_gallery(self):
        """
        Reloads the gallery view to reflect any deletions or updates by reinitializing the layout.
        """

        # Remove existing layout if present
        existing_layout = self.layout()
        if existing_layout:
            QWidget().setLayout(existing_layout)

        # Reinitialize the UI to load updated image groups
        self.initUI()

    def export_animation_gif(self, mode, button, overlay, original_pixmap, styled_pixmap):
        """
        Exports an animation GIF with either a transition or a before/after effect,
        depending on the specified `mode`.

        Parameters:
            mode (str): The animation mode, either "Transition" or "Before/After".
            button (QPushButton): Button that triggers the export, used for overlay positioning.
            overlay (QLabel): Overlay message label for displaying export status.
            original_pixmap (QPixmap): The original image to include in the animation.
            styled_pixmap (QPixmap): The styled image to include in the animation.
        """

        # Create a temporary directory for saving intermediate images
        temp_dir = Path("temporary_data") / "animation_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()

        # Save original and styled images as temporary files
        temp_orig_path = temp_dir / "original.png"
        temp_styled_path = temp_dir / "styled.png"
        original_pixmap.save(str(temp_orig_path))
        styled_pixmap.save(str(temp_styled_path))

        # Open the saved images with PIL for blending
        original_image = Image.open(temp_orig_path).convert("RGBA")
        styled_image = Image.open(temp_styled_path).convert("RGBA")

        # List to store animation frames
        frames = []
        # Generate frames for the animation (from 0 to 100% blend)
        for i in range(101):
            if mode == "Transition":
                # Blend frames progressively for a transition effect
                blended_frame = Image.blend(original_image, styled_image, i / 100.0)
            elif mode == "Before/After":
                # Create a before/after frame, splitting by slider position
                blended_frame = styled_image.copy()
                width = styled_image.width
                split_position = int(width * (i / 100.0))
                # Paste styled image from the split position to the right
                blended_frame.paste(original_image.crop((split_position, 0, width, original_image.height)),
                                    (split_position, 0))
            # Store the generated frame
            frames.append(blended_frame)

        # Open a file dialog to save the animation as a GIF
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Animation", "", "GIF (*.gif)")
        if file_path:
            # Save the frames as an animated GIF
            frames[0].save(file_path, save_all=True, append_images=frames[1:], duration=100, loop=0)

        # Clean up temporary directory after saving
        shutil.rmtree(temp_dir)
        if file_path:
            # Display a success message on overlay
            self.show_overlay_message("Animation exported.", button, overlay)

    def export_animation_video(self, mode, button, overlay, original_pixmap, styled_pixmap):
        """
        Exports an animation video with either a transition or a before/after effect,
        depending on the specified `mode`.

        Parameters:
            mode (str): The animation mode, either "Transition" or "Before/After".
            button (QPushButton): Button that triggers the export, used for overlay positioning.
            overlay (QLabel): Overlay message label for displaying export status.
            original_pixmap (QPixmap): The original image to include in the animation.
            styled_pixmap (QPixmap): The styled image to include in the animation.
        """

        # Create a temporary directory for saving intermediate images
        temp_dir = Path("temporary_data") / "animation_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()

        # Save original and styled images as temporary files
        temp_orig_path = temp_dir / "original.png"
        temp_styled_path = temp_dir / "styled.png"
        original_pixmap.save(str(temp_orig_path))
        styled_pixmap.save(str(temp_styled_path))

        # Open the saved images with PIL for blending
        original_image = Image.open(temp_orig_path).convert("RGBA")
        styled_image = Image.open(temp_styled_path).convert("RGBA")

        # Set video parameters (width, height, frames per second)
        width, height = original_image.size
        fps = 30

        # Open a file dialog to save the animation as a video
        file_path, _ =QFileDialog.getSaveFileName(self, "Save Animation", "", "MP4 (*.mp4);;AVI (*.avi)")
        if not file_path:
            return

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') if file_path.endswith('.mp4') else cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(file_path, fourcc, fps, (width, height))

        # Generate frames for the animation (from 0 to 100% blend)
        for i in range(101):
            if mode == "Transition":
                # Blend frames progressively for a transition effect
                blended_frame = Image.blend(original_image, styled_image, i / 100.0)
            elif mode == "Before/After":
                # Create a before/after frame, splitting by slider position
                blended_frame = styled_image.copy()
                split_position = int(width * (i / 100.0))

                # Paste styled image from the split position to the right
                blended_frame.paste(original_image.crop((split_position, 0, width, height)),
                                    (split_position, 0))

            # Convert PIL image to OpenCV format
            open_cv_image = cv2.cvtColor(np.array(blended_frame), cv2.COLOR_RGBA2BGR)
            video_writer.write(open_cv_image)

        # Release the video writer after all frames are added
        video_writer.release()

        # Clean up temporary directory after saving
        shutil.rmtree(temp_dir)
        if file_path:
            # Display a success message on overlay
            self.show_overlay_message("Animation exported.", button, overlay)

    def show_overlay_message(self, message, button, overlay_message, duration=5000):
        """
        Displays a temporary overlay message above a specified button for a set duration.

        Parameters:
            message (str): The message to display in the overlay.
            button (QWidget): The button above which the overlay message is shown.
            overlay_message (QLabel): The QLabel widget used to display the overlay message.
            duration (int): Time in milliseconds to keep the message visible.
        """

        # Disable the toolbar to prevent interactions while the message is displayed
        self.toolbar.setDisabled(True)

        # Bring the overlay message QLabel to the front and update its text and visibility
        overlay_message.raise_()
        overlay_message.setText(message)
        overlay_message.setVisible(True)

        # Position the overlay message directly above the specified button
        button_geometry = button.geometry()
        x = button_geometry.left()
        y = button_geometry.top()
        overlay_message.setGeometry(x, y, button_geometry.width(), button_geometry.height())

        # Hide the overlay message after the specified duration and re-enable the toolbar
        QTimer.singleShot(duration, lambda: self.hide_overlay_message(overlay_message))

    def hide_overlay_message(self, overlay_message):
        """
        Hides the overlay message and re-enables the toolbar for user interaction.

        Parameters:
            overlay_message (QLabel): The QLabel widget displaying the overlay message.
        """

        # Set the overlay message to invisible
        overlay_message.setVisible(False)

        # Re-enable the toolbar to restore user interactions
        self.toolbar.setDisabled(False)

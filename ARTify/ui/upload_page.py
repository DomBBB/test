"""
This file defines various pages and components for the Art Studio App, focusing on
image upload, selection, processing, and displaying a progress bar during style
transfer operations. The included pages and components are:

- UploadPage: Allows users to upload new images or select sample images to transform.
- SampleSelectionPage: Displays and enables selection of sample images for processing.
- NewUploadPage: Supports uploading user images, capturing new photos, and displaying uploaded images.
- CameraDialog: A dialog for capturing images directly from the camera with a live preview.
- ModelWorker: Background worker that handles style transfer model processing on selected images.
- ProgressBarPage: Displays a progress bar to track the style transfer process.
"""


# Import PyQT5 for GUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QPushButton, QProgressBar, QDialog, QDialogButtonBox, QSizePolicy, QTextEdit, QFileDialog, QHBoxLayout, QSpacerItem
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QObject, QThread
from PyQt5.QtGui import QPixmap, QImage, QFont

# Import libraries
import time
import uuid
import shutil
from pathlib import Path
import cv2

# Import toolbar
from ui.toolbar_helper import setup_toolbar

# Import CycleGAN processing
from utils.run_cycleGAN import run_test_script


class UploadPage(QWidget):
    """
    Page to upload new images or select sample images.
    """

    # Signals for navigation to other pages
    go_to_main = pyqtSignal()
    go_to_upload = pyqtSignal()
    go_to_workspace = pyqtSignal()
    go_to_gallery = pyqtSignal()

    # Signals to go to the next page with sample/new images
    go_to_new_upload = pyqtSignal()
    go_to_sample_selection = pyqtSignal()

    def __init__(self):
        """
        Initializes the UploadPage layout, setting up the toolbar, description label, and
        action buttons for uploading or selecting sample images.
        """

        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the layout with a toolbar, a description label, and navigation buttons.
        This layout provides options to go to pages to either upload new images or select sample images.
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
            "Choose an option to start creating your masterpiece")
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
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(30)

        # Set background color for the page
        self.setStyleSheet("background-color: #f7f9fc;")

        #####################################################################
        #                                                                                                                                      #
        # Content Layout                                                                                                            #
        #                                                                                                                                      #
        #####################################################################

        # Navigation button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_style = (
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }"
        )

        # Upload button to navigate to the upload page
        self.upload_new_button = QPushButton("\n\n\n\n\nUpload Images\n\n\n\n\n")
        self.upload_new_button.setFont(QFont("Arial", 14.5))
        self.upload_new_button.setStyleSheet(button_style)
        self.upload_new_button.clicked.connect(self.go_to_new_upload.emit)
        # Add to the layout
        button_layout.addWidget(self.upload_new_button)

        # Sample button to navigate to the select samples page
        self.select_sample_button = QPushButton("\n\n\n\n\nSelect Sample Images\n\n\n\n\n")
        self.select_sample_button.setFont(QFont("Arial", 14.5))
        self.select_sample_button.setStyleSheet(button_style)
        self.select_sample_button.clicked.connect(self.go_to_sample_selection.emit)
        # Add to the layout
        button_layout.addWidget(self.select_sample_button)

        # Add to the page
        content_layout.addLayout(button_layout)

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


class SampleSelectionPage(QWidget):
    """
    Page to display and select sample images.
    """

    # Signals for navigation to other pages
    go_to_main = pyqtSignal()
    go_to_upload = pyqtSignal()
    go_to_workspace = pyqtSignal()
    go_to_gallery = pyqtSignal()

    # Signal to go to the progress bar
    go_to_progress_bar = pyqtSignal(list)

    def __init__(self):
        """
        Initializes the SampleSelectionPage layout, setting up the toolbar, description,
        image grid, and 'Process' button.
        """

        super().__init__()
        self.selected_images = []
        self.initUI()

    def initUI(self):
        """
        Sets up the layout for displaying sample images from the examples folder, allowing
        selection of one or more images to process.
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
            "Select one or multiple sample images to process")
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
        thumbnail_size =  400

        #####################################################################
        #                                                                                                                                      #
        # Content Layout                                                                                                            #
        #                                                                                                                                      #
        #####################################################################

        row, col = 0, 0
        # Load images from the examples folder and add to grid
        for image_path in Path("database/examples").glob("*.jpg"):
            # Add and display image
            img_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap(str(image_path)).scaled(thumbnail_size, thumbnail_size, Qt.KeepAspectRatio)
            img_label.setPixmap(pixmap)
            # Make image clickable with a border
            img_label.mousePressEvent = lambda event, path=image_path, label=img_label: self.toggle_selection(path, label)
            img_label.setStyleSheet("border: 4px solid transparent;")
            # Add to the layout
            grid_layout.addWidget(img_label, row, col)
            # Update column and row for grid placement (3 images per row)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        #####################################################################
        #                                                                                                                                      #
        # Set Layout 1/2                                                                                                              #
        #                                                                                                                                      #
        #####################################################################

        # Set the scroll area to contain all content
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        #####################################################################
        #                                                                                                                                      #
        # Displayable Footer                                                                                                       #
        #                                                                                                                                      #
        #####################################################################

        # Style for navigation buttons
        button_style = (
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }"
        )
        # 'Process' button to proceed with selected images
        self.next_button = QPushButton("\nProcess\n                                                           ")
        self.next_button.setFont(QFont("Arial", 14.5))
        self.next_button.setStyleSheet(button_style)
        self.next_button.setVisible(False)
        self.next_button.clicked.connect(lambda: self.go_to_progress_bar.emit(self.selected_images))
        # Add to the page
        main_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        #####################################################################
        #                                                                                                                                      #
        # Set Layout 2/2                                                                                                              #
        #                                                                                                                                      #
        #####################################################################

        # Set Layout
        self.setLayout(main_layout)

    def toggle_selection(self, image_path, label):
        """
        Toggles the selection state of an image and updates the image border.
        Shows the 'Process' button if any images are selected.

        Parameters:
            image_path (Path): The path to the image file being toggled.
            label (QLabel): The QLabel widget displaying the image, whose
                                      border is updated to reflect selection state.
        """

        # Deselect and make border transparent if image is already selected
        if image_path in self.selected_images:
            self.selected_images.remove(image_path)
            label.setStyleSheet("border: 4px solid transparent;")
        # Select and make border visible if image is not selected
        else:
            self.selected_images.append(image_path)
            label.setStyleSheet("border: 4px solid #1976D2;")

        # Show 'Process' button if any images are selected
        self.next_button.setVisible(len(self.selected_images) > 0)


class NewUploadPage(QWidget):
    """
    Page to allow users to upload and display their own images, with options to upload
    multiple images, manage image selections, take a new picture, and navigate to processing.
    """

    # Signals for navigation to other pages
    go_to_main = pyqtSignal()
    go_to_upload = pyqtSignal()
    go_to_workspace = pyqtSignal()
    go_to_gallery = pyqtSignal()

    # Signal to go to the progress bar
    go_to_progress_bar = pyqtSignal(list)

    def __init__(self):
        """
        Initializes the NewUploadPage, setting up the directory for uploaded images
        and preparing the layout for image selection.
        """

        super().__init__()
        self.selected_images = []
        self.max_images = 12
        # Create empty temporary uploads folder
        self.folder_path = Path("temporary_data/uploads")
        if self.folder_path.exists():
            shutil.rmtree(self.folder_path)
        self.folder_path.mkdir()
        self.initUI()
        self.cameras_checked = False

    def initUI(self):
        """
        Sets up the layout with navigation toolbar, header, upload and capture buttons,
        and grid for displaying uploaded images.
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

        #####################################################################
        # Header                                                                                                                          #
        #####################################################################
        header_layout = QHBoxLayout()

        # Title label centered at the top
        header_label = QLabel(
            "Upload up to 12 images or take a new one")
        header_label.setFont(QFont("Arial", 15, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #555555; background: none;")
        header_label.setWordWrap(True)
        # Add to the layout
        header_layout.addWidget(header_label)

        # Button layout for upload and capture functions
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_style = (
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }"
        )
        # Upload Images button
        self.upload_button = QPushButton("Upload Images")
        self.upload_button.setFont(QFont("Arial", 14.5))
        self.upload_button.setStyleSheet(button_style)
        self.upload_button.clicked.connect(self.upload_images)
        button_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        # Capture Image button
        self.capture_button = QPushButton("Capture Image (takes some seconds)")
        self.capture_button.setFont(QFont("Arial", 14.5))
        self.capture_button.setStyleSheet(button_style)
        self.capture_button.clicked.connect(self.open_camera_dialog)
        button_layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)
        # Spacer to the right of the buttons
        spacer = QLabel("     ")
        spacer.setStyleSheet("background: none;")
        button_layout.addWidget(spacer)
        # Add to the layout
        header_layout.addLayout(button_layout)
        main_layout.addLayout(header_layout)

        # Overlay for displaying temporary messages
        self.overlay_message = QLabel("", self)
        self.overlay_message.setFont(QFont("Arial", 12.5))
        self.overlay_message.setStyleSheet("background-color: #0F4C81; color: white; padding: 8px 16px; border-radius: 8px;")
        self.overlay_message.setAlignment(Qt.AlignCenter)
        self.overlay_message.setVisible(False)

        #####################################################################
        # Content                                                                                                                         #
        #####################################################################

        # Scrollable area for main content with padding and spacing
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.grid_layout.setSpacing(30)

        # Set background color for the page
        self.setStyleSheet("background-color: #f7f9fc;")

        # Set thumbnail size
        self.thumbnail_size =  400

        #####################################################################
        #                                                                                                                                      #
        # Set Layout 1/2                                                                                                              #
        #                                                                                                                                      #
        #####################################################################

        # Set the scroll area to contain all content
        scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(scroll_area)

        #####################################################################
        #                                                                                                                                      #
        # Displayable Footer                                                                                                       #
        #                                                                                                                                      #
        #####################################################################

        # Style for navigation buttons
        button_style = (
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }"
        )
        # 'Process' button to proceed with selected images
        self.next_button = QPushButton("\nProcess\n                                                           ")
        self.next_button.setFont(QFont("Arial", 14.5))
        self.next_button.setStyleSheet(button_style)
        self.next_button.setVisible(False)
        self.next_button.clicked.connect(lambda: self.go_to_progress_bar.emit(self.selected_images))
        # Add to the page
        main_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        #####################################################################
        #                                                                                                                                      #
        # Set Layout 2/2                                                                                                              #
        #                                                                                                                                      #
        #####################################################################

        # Set Layout
        self.setLayout(main_layout)
        self.update_upload_button_status()

    def upload_images(self):
        """
        Opens a dialog for selecting images to upload, with support for PNG, JPG, JPEG, and XPM files.
        """

        # Calculate remaining slots
        remaining_slots = self.max_images - len(self.selected_images)

        # File dialog for selecting images
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.xpm *.jpg *.jpeg)")

        # Filter out unsupported files and limit the number of images
        allowed_extensions = {".png", ".jpg", ".jpeg", ".xpm"}
        unsupported_files = [f for f in file_paths if Path(f).suffix.lower() not in allowed_extensions]
        file_paths = [f for f in file_paths if Path(f).suffix.lower() in allowed_extensions]
        # Limit the number of images selected if necessary
        if len(file_paths) > remaining_slots:
            file_paths = file_paths[:remaining_slots]
            if unsupported_files:
                self.show_overlay_message(f"Max. 12 images! First {remaining_slots} supported file types are processed.")
            else:
                self.show_overlay_message(f"Max. 12 images! First {remaining_slots} images are processed.")
        elif unsupported_files:
            self.show_overlay_message("Unsupported files. Only PNG/JPG/JPEG/XPM are processed.")

        # Process and add images to the layout
        for file_path in file_paths:
            processed_path = self.process_and_save_image(file_path)
            if processed_path:
                self.add_image(processed_path)

        # Update the visibility of the Next button
        self.next_button.setVisible(len(self.selected_images) > 0)

        # Update the visibility of the Upload button
        self.update_upload_button_status()

    def check_connected_cameras(self):
        """
        Checks for available cameras connected to the system by testing main (index 0)
        and secondary (index 1) camera inputs. Updates the capture button state
        based on the available cameras.

        Returns:
            list or None: A list containing the indices of available cameras (if any).
        """

        # Assume cameras are unavailable initially
        main_camera_available = False
        secondary_camera_available = False

        # Test main camera (index 0)
        main_cap = cv2.VideoCapture(0)
        if main_cap.isOpened():
            main_camera_available = True
        main_cap.release()

        # Test secondary camera (index 1)
        secondary_cap = cv2.VideoCapture(1)
        if secondary_cap.isOpened():
            secondary_camera_available = True
        secondary_cap.release()

        # Determine which cameras are available and update the checked list
        if main_camera_available and secondary_camera_available:
            # If both cameras are available
            self.cameras_checked = [0,1]
            return self.cameras_checked
        elif main_camera_available:
            # If only main cameras is available
            self.cameras_checked = [0]
            return self.cameras_checked
        elif secondary_camera_available:
            # If only secondary cameras is available
            self.cameras_checked = [1]
            return self.cameras_checked
        else:
            # If no camera is available, update the capture button
            self.capture_button.setText("Cameras unavailable")
            self.capture_button.setEnabled(False)
            button_style = (
                "QPushButton { background-color: grey; color: white; padding: 8px 16px; border-radius: 8px; }"
            )
            self.capture_button.setStyleSheet(button_style)

    def open_camera_dialog(self):
        """
        Opens a dialog for capturing an image using the connected camera. If no
        camera has been previously checked, it initiates a check. Captured images
        are saved in the user folder after resizing and converting them.
        """

        # Check cameras if not done previously
        if not self.cameras_checked:
            camera_index_to_use = self.check_connected_cameras()
        else:
            camera_index_to_use = self.cameras_checked
        # Stop window opening if no camera is available
        if not camera_index_to_use:
            return

        # Open camera dialog for capturing image
        camera_dialog = CameraDialog(self, camera_index_to_use)
        if camera_dialog.exec_() == QDialog.Accepted:
            frame = camera_dialog.captured_image
            if frame is not None:
                # Generate a unique filename for the captured image
                image_name = f"capture_{int(time.time())}_{uuid.uuid4().hex[:6]}.jpg"
                save_path = self.folder_path / image_name

                # Convert the captured frame from BGR to RGB format and resize for saving
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
                image = self.resize_and_crop_image(image, 256, 256)

                # Save the image and display it
                image.save(str(save_path), "JPEG")
                self.add_image(save_path)

        # Update the visibility of the Next button
        self.next_button.setVisible(len(self.selected_images) > 0)

        # Update the visibility of the Upload button
        self.update_upload_button_status()

    def add_image(self, file_path):
        """
        Adds an image to the grid layout after processing and saving it. The image
        is displayed alongside a delete button, allowing users to remove the image if needed.

        Parameters:
            file_path (Path): The path to the image file to be added to the layout.
        """

        # Create a container widget with no margins to hold both the image and the delete button
        container = QWidget()
        container_layout = QGridLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Spacer above the image
        spacer = QLabel("     ")
        spacer.setStyleSheet("background: none;")
        # Add to layout
        container_layout.addWidget(spacer, 0, 0, Qt.AlignCenter)

        # Load and display the processed image in the QLabel
        img_label = QLabel()
        pixmap = QPixmap(str(file_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_label.setPixmap(pixmap)
        # Add to layout
        container_layout.addWidget(img_label, 1, 1, Qt.AlignCenter)

        # Spacer below the image
        spacer_2 = QLabel("     ")
        spacer_2.setStyleSheet("background: none;")
        # Add to layout
        container_layout.addWidget(spacer_2, 2, 2, Qt.AlignCenter)

        # Create a delete button overlay on top of the image
        delete_button = QPushButton("✖")
        delete_button.setFixedSize(48, 48)
        delete_button.setStyleSheet("color: white; background-color: #1976D2; border-radius: 12px;")
        delete_button.clicked.connect(lambda: self.remove_image(img_label, delete_button, file_path))
        # Add to layout
        container_layout.addWidget(delete_button, 1, 1, Qt.AlignTop | Qt.AlignRight)

        # Calculate the grid position for the new image container
        row = len(self.selected_images) // 3
        col = len(self.selected_images) % 3
        # Add to page
        self.grid_layout.addWidget(container, row, col)

        # Track the image path
        self.selected_images.append(file_path)

    def remove_image(self, img_label, delete_button, file_path):
        """
        Removes the specified image from the grid layout and deletes it from the local folder.
        The grid is reorganized after removal to maintain layout structure.

        Parameters:
            img_label (QLabel): The QLabel widget displaying the image.
            delete_button (QPushButton): The delete button associated with the image.
            file_path (Path): The file path of the image to be removed.
        """

        # Delete the image file from storage
        if file_path.exists():
            file_path.unlink()

        # Remove the image path from the selected images list
        self.selected_images.remove(file_path)

        # Clear all items from the grid layout
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Re-add remaining images to the grid layout to reset positions
        for index, image_path in enumerate(self.selected_images):
            # Create a container widget with no margins to hold both the image and the delete button
            container = QWidget()
            container_layout = QGridLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)

            # Spacer above the image
            spacer = QLabel("     ")
            spacer.setStyleSheet("background: none;")
            # Add to layout
            container_layout.addWidget(spacer, 0, 0, Qt.AlignCenter)

            # Load and display the processed image in the QLabel
            img_label = QLabel()
            pixmap = QPixmap(str(image_path)).scaled(self.thumbnail_size, self.thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img_label.setPixmap(pixmap)
            # Add to layout
            container_layout.addWidget(img_label, 1, 1, Qt.AlignCenter)

            # Spacer below the image
            spacer_2 = QLabel("     ")
            spacer_2.setStyleSheet("background: none;")
            # Add to layout
            container_layout.addWidget(spacer_2, 2, 2, Qt.AlignCenter)

            # Create a delete button overlay on top of the image
            delete_button = QPushButton("✖")
            delete_button.setFixedSize(48, 48)
            delete_button.setStyleSheet("color: white; background-color: #1976D2; border-radius: 12px;")
            delete_button.clicked.connect(lambda _, lbl=img_label, btn=delete_button, path=image_path:
                                          self.remove_image(lbl, btn, path))
            # Add to layout
            container_layout.addWidget(delete_button, 1, 1, Qt.AlignTop | Qt.AlignRight)

            # Calculate the grid position for the new image container
            row = index // 3
            col = index % 3
            # Add to page
            self.grid_layout.addWidget(container, row, col)

        # Update the visibility of the Next button
        self.next_button.setVisible(len(self.selected_images) > 0)

        # Update the visibility of the Upload button
        self.update_upload_button_status()

    def show_overlay_message(self, message, duration=7000):
        """
        Displays a temporary overlay message for a specified duration.
        Disables the toolbar while the message is displayed.

        Parameters:
            message (str): The message to display.
            duration (int): Duration in milliseconds to display the message.
        """

        # Disable the toolbar while the overlay message is visible
        self.toolbar.setDisabled(True)

        # Bring the overlay message to the front of other widgets
        self.overlay_message.raise_()
        # Set the message text
        self.overlay_message.setText(message)
        # Make the overlay message visible
        self.overlay_message.setVisible(True)

        # Position the overlay message over the upload and capture buttons
        button_geometry = self.upload_button.geometry()
        button_2_geometry = self.capture_button.geometry()
        x = button_geometry.left()
        y = button_geometry.top()
        self.overlay_message.setGeometry(x, y, button_geometry.width() + 20 + button_2_geometry.width(), button_geometry.height())

        # Hide the overlay message after the specified duration and re-enable the toolbar
        QTimer.singleShot(duration, lambda: self.hide_overlay_message())

    def hide_overlay_message(self):
        """
        Hides the overlay message and re-enables the toolbar.
        """

        # Set the overlay message visibility to False
        self.overlay_message.setVisible(False)
        # Re-enable the toolbar
        self.toolbar.setDisabled(False)

    def update_upload_button_status(self):
        """
        Enables or disables the upload and capture buttons based on the current number of selected images.
        If the maximum number of images is reached, both buttons are disabled and their styles and tooltips are updated.
        Otherwise, the buttons remain enabled, and their styles and tooltips are reset.
        """

        if len(self.selected_images) >= self.max_images:
            # Style the buttons as disabled
            button_style = (
                "QPushButton { background-color: grey; color: white; padding: 8px 16px; border-radius: 8px; }"
            )
            self.upload_button.setStyleSheet(button_style)
            self.capture_button.setStyleSheet(button_style)
            # Disable both the upload and capture buttons
            self.upload_button.setDisabled(True)
            self.capture_button.setDisabled(True)
            # Update tooltips with max image limit message
            self.upload_button.setToolTip("Maximum of 12 images reached. Please remove images to upload more.")
            self.capture_button.setToolTip("Maximum of 12 images reached. Please remove images to capture more.")
        else:
            # Style the buttons as enabled
            button_style = (
                "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
                "QPushButton:hover { background-color: #0F4C81; }"
            )
            # Restore the original button style
            self.upload_button.setStyleSheet(button_style)
            self.capture_button.setStyleSheet(button_style)
            # Enable both the upload and capture buttons
            self.upload_button.setDisabled(False)
            self.capture_button.setDisabled(False)
            # Clear the tooltips
            self.upload_button.setToolTip("")
            self.capture_button.setToolTip("")

    def process_and_save_image(self, file_path):
        """
        Processes an image by resizing and cropping it to 256x256 pixels,
        then saves it as a .jpg file in the user's upload folder.

        Parameters:
            file_path (Path): The path to the image file to process.

        Returns:
            Path or None: The path to the saved image file if successful.
        """

        # Load the image from the provided file path
        image = QImage(file_path)

        # Resize and crop the image to 256x256 pixels
        image = self.resize_and_crop_image(image, 256, 256)

        # Define a unique save path using a timestamp and unique identifier
        timestamp = int(time.time())
        unique_id = uuid.uuid4().hex[:6]
        image_name = f"{Path(file_path).stem}_{timestamp}_{unique_id}.jpg"
        save_path = self.folder_path / image_name

        # Save the processed image as a .jpg
        image.save(str(save_path), "JPEG")

        # Return the save path if the image file exists, otherwise return None
        return save_path if save_path.exists() else None

    def resize_and_crop_image(self, image, target_width, target_height):
        """
        Resizes and crops an image to fit specified dimensions, maintaining aspect ratio.

        Parameters:
            image (QImage): The image to resize and crop.
            target_width (int): The desired width of the output image.
            target_height (int): The desired height of the output image.

        Returns:
            QImage: A resized and cropped image with the specified target dimensions.
        """

        # Get original width and height of the image
        width, height = image.width(), image.height()

        # Scale the image to ensure it fully covers the target dimensions while maintaining aspect ratio
        if width > height:
            image = image.scaledToHeight(target_height, Qt.SmoothTransformation)
        else:
            image = image.scaledToWidth(target_width, Qt.SmoothTransformation)

        # Calculate offsets to center-crop the image to the target width and height
        x_offset = (image.width() - target_width) // 2
        y_offset = (image.height() - target_height) // 2

        # Return a cropped version of the image
        return image.copy(x_offset, y_offset, target_width, target_height)


class CameraDialog(QDialog):
    """
    Dialog for capturing images from a connected camera.
    This class provides a live preview of the camera feed and allows capturing and switching between cameras.
    """

    def __init__(self, parent, camera_index_to_use):
        """
        Initializes the CameraDialog with a live camera preview and controls for capturing images.

        Parameters:
            parent (QWidget): The parent widget for the dialog.
            camera_index_to_use (list): List of available camera indices (e.g., [0, 1]).
        """

        super().__init__(parent)
        self.camera_index_to_use = camera_index_to_use
        self.camera_resolution = 600
        self.setWindowTitle("Capture Image")

        # Main layout with a fixed-size preview area and buttons
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Set up QLabel for the camera feed preview
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.camera_resolution, self.camera_resolution)
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_label.setStyleSheet(
            "border: 2px solid #1976D2; background-color: #f7f9fc; color: #333333;"
        )
        self.layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Button styling
        button_style = (
            "QPushButton { background-color: #1976D2; color: white; padding: 12px 24px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }"
        )
        # Initialize capture button
        self.capture_button = QPushButton("Capture")
        self.capture_button.setStyleSheet(button_style)
        self.capture_button.setFont(QFont("Arial", 16))
        self.capture_button.clicked.connect(self.capture_image)
        # Initialize switch camera button
        self.switch_camera_button = QPushButton("Switch Camera")
        self.switch_camera_button.setStyleSheet(button_style)
        self.switch_camera_button.setFont(QFont("Arial", 16))
        self.switch_camera_button.clicked.connect(self.switch_camera)
        # Disable switch button if only one camera is available
        if len(self.camera_index_to_use) != 2:
            self.switch_camera_button.setText("Switch unavailable")
            self.switch_camera_button.setEnabled(False)

        # Add buttons to layout below the image area
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.switch_camera_button, alignment=Qt.AlignCenter)
        self.layout.addLayout(button_layout)

        # Set layout for the dialog
        self.setLayout(self.layout)

        # Initialize camera feed and timer for updating the preview
        self.camera_index = self.camera_index_to_use[0]
        self.cap = cv2.VideoCapture(self.camera_index)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Attribute to store captured image
        self.captured_image = None

    def update_frame(self):
        """
        Captures frames continuously from the camera feed and displays them in QLabel.
        """

        # Read the frame
        ret, frame = self.cap.read()

        if ret:
            # Crop frame to a square centered on the frame
            height, width, _ = frame.shape
            min_dim = min(height, width)
            y_offset = (height - min_dim) // 2
            x_offset = (width - min_dim) // 2
            square_frame = frame[y_offset:y_offset + min_dim, x_offset:x_offset + min_dim]

            # Resize to fit QLabel and convert to RGB format for display
            square_frame_resized = cv2.resize(square_frame, (self.camera_resolution, self.camera_resolution))
            frame_rgb = cv2.cvtColor(square_frame_resized, cv2.COLOR_BGR2RGB)

            # Convert to QImage and display in QLabel
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def capture_image(self):
        """
        Captures and saves the current frame displayed in the dialog.
        """

        # Read the frame
        ret, frame = self.cap.read()
        if ret:
            # Store the captured frame
            self.captured_image = frame
            # Close the dialog
            self.accept()

    def switch_camera(self):
        """
        Switches between available cameras (if multiple are available).
        """

        # Temporarily release the current camera
        self.timer.stop()
        self.cap.release()

        # Toggle between camera indices (e.g., between 0 and 1)
        self.camera_index = 1 - self.camera_index

        # Introduce a delay to avoid freezing
        QTimer.singleShot(100, self.initialize_new_camera)

    def initialize_new_camera(self):
        """
        Reinitializes the camera after switching with a short delay to avoid freezing.
        """

        # Reinitialize the camera
        self.cap = cv2.VideoCapture(self.camera_index)
        # Restart the frame update timer
        self.timer.start(30)

    def closeEvent(self, event):
        """
        Handles the dialog close event by releasing the camera and stopping the timer.
        """

        self.timer.stop()
        self.cap.release()
        event.accept()


class ModelWorker(QObject):
    """
    Worker class for processing images through multiple style transfer models asynchronously.
    This class is used in a separate thread to avoid blocking the main GUI.
    """

    # Signals for reporting progress and completion status
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)

    def __init__(self, selected_images):
        """
        Initializes the worker with selected images for processing.

        Parameters:
            selected_images (list): List of paths to the images selected for style transfer.
        """

        super().__init__()
        self.selected_images = selected_images

    def run(self):
        """
        Copies selected images into a temporary directory, runs each style transfer model,
        and emits progress updates. Emits a completion signal with the results when finished.
        """

        # Remove previous datasets folder if it exists
        parent_path_data = Path("temporary_data/datasets")
        if parent_path_data.exists():
            shutil.rmtree(parent_path_data)

        # Create the new datasets directory for images to be processed
        folder_path = Path("temporary_data/datasets/images/testB")
        folder_path.mkdir(parents=True)
        # Copy each selected image to the processing folder
        for image_path in self.selected_images:
            shutil.copy(image_path, folder_path)

        # Remove temporary uploads folder
        parent_path_uploads = Path("temporary_data/uploads")
        if parent_path_uploads.exists():
            shutil.rmtree(parent_path_uploads)

        # Clear out previous results folder
        parent_path_results = Path("temporary_data/results")
        if parent_path_results.exists():
            shutil.rmtree(parent_path_results)

        # Dictionary to store model paths and statuses
        artists = {
            "style_cezanne_pretrained": False,
            "style_monet_pretrained": False,
            "style_ukiyoe_pretrained": False,
            "style_vangogh_pretrained": False}
        progress = 0

        # Execute each style transfer model and update progress
        for artist in artists:
            # Run the model script
            execution = run_test_script(artist)
            # If execution was successful
            if not execution:
                # Update dictionary with output path
                artists[artist] = f"temporary_data/results/{artist}/test_latest/images"
                progress += 25
                # Emit progress update
                self.progress.emit(progress)
            # If model failed
            else:
                # Store error message
                artists[artist] = execution

        # Emit finished signal with results summary
        if progress == 100:
            self.finished.emit(["success", artists])
        else:
            self.finished.emit(["error", artists])


class ProgressBarPage(QWidget):
    """
    Page to display a progress bar and manage the processing of selected images
    through various style transfer models.
    """

    # Signals to go to the processed page (incl. error handling)
    go_to_main = pyqtSignal()
    go_to_workspace = pyqtSignal()

    def __init__(self, selected_images, my_sizing):
        """
        Initializes the progress bar page with the list of selected images and screen size.

        Parameters:
            selected_images (list[Path]): List of paths to the selected images.
            my_sizing (tuple[int, int]): Screen width and height for sizing the overlay.
        """

        super().__init__()
        self.selected_images = selected_images
        self.initUI()
        self.show_loading_overlay(my_sizing)
        self.start_model_processing()

    def initUI(self):
        """
        Sets up the layout for the page, initializing it with an empty vertical layout.
        """

        # Main layout for the page
        layout = QVBoxLayout()

        # Set Layout
        self.setLayout(layout)

    def show_loading_overlay(self, my_sizing):
        """
        Creates and displays a semi-transparent overlay with a progress bar centered on the screen.

        Parameters:
            my_sizing (tuple[int, int]): Screen width and height for setting overlay dimensions.
        """

        # Set up a dark, semi-transparent overlay covering the whole screen
        self.overlay = QWidget(self)
        self.overlay.setGeometry(0, 0, my_sizing[0], my_sizing[1])
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        # Centered progress bar with styling
        self.progress_bar = QProgressBar(self.overlay)
        self.progress_bar.setFixedSize(my_sizing[0] * 0.6, my_sizing[0] * 0.05)
        self.progress_bar.move((my_sizing[0] - self.progress_bar.width()) / 2, my_sizing[1] / 2 - (my_sizing[0]*0.05)/2)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Processing... %p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #f0f4f8;
                color: #333333;
                border: 4px solid #1976D2;
                border-radius: 10px;
                text-align: center;
                font: bold 40px Arial;
            }
            QProgressBar::chunk {
                background-color: #1976D2;
                border-radius: 2px;
            }
        """)

        # Display overlay
        self.overlay.show()

    def start_model_processing(self):
        """
        Initiates model processing in a separate thread to avoid blocking the main UI thread.
        """

        # Set up background thread and ModelWorker instance
        self.thread = QThread()
        self.worker = ModelWorker(self.selected_images)
        self.worker.moveToThread(self.thread)

        # Connect worker signals for progress and completion
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_processing_finished)

        # Start processing in the background
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def update_progress(self, value):
        """
        Updates the progress bar based on progress received from the worker.

        Parameters:
            value (int): The new progress value to set on the progress bar.
        """

        self.progress_bar.setValue(value)

    def on_processing_finished(self, results):
        """
        Handles completion of processing, hides the overlay, and navigates based on results.

        Parameters:
            results (list): Processing results, including success status and processed image paths.
        """

        # Hide the overlay
        self.overlay.hide()

        # Stop and clean up the processing thread
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()

        # If processing was sucessful
        if results[0] == "success":
            # Move results
            self.process_and_move_images()
            # Continue to workspace
            self.go_to_workspace.emit()
        # If processing was not successful
        else:
            # Show an error dialog with details if processing failed
            error_popup = QDialog(self)
            error_popup.setWindowTitle("Processing Error")
            error_popup.setFixedSize(800, 600)

            # Layout for error dialog with error message and detailed log
            layout = QVBoxLayout()

            # Error label
            label = QLabel("An error occurred during processing:")
            layout.addWidget(label)
            text_edit = QTextEdit()
            error_message = "\n".join([key + ": " + value for key,value in results[1].items()])
            text_edit.setPlainText(error_message)
            text_edit.setReadOnly(True)
            # Add to layout
            layout.addWidget(text_edit)

            # Add a close button at the bottom of the popup
            button_box = QDialogButtonBox(QDialogButtonBox.Close)
            button_box.rejected.connect(lambda: (self.go_to_main.emit(), error_popup.close()))
            # Add to layout
            layout.addWidget(button_box)

            # Add to dialog
            error_popup.setLayout(layout)

            # Override the close event to emit the same action as the Close button
            def on_close_event(event):
                # Emit the signal to go to the main page
                self.go_to_main.emit()
                # Accept the close event to close the dialog
                event.accept()
            error_popup.closeEvent = on_close_event

            # Show the error popup
            error_popup.exec_()

    def process_and_move_images(self):
        """
        Organizes processed images by moving them into a dedicated user directory
        with each image group in its own subfolder.
        """

        # New image folders and paths
        temp_image_folder = Path("temporary_data/datasets/images/testB")
        style_folders = [Path(f"temporary_data/results/style_{style}_pretrained/test_latest/images")
                                    for style in ["cezanne", "monet", "ukiyoe", "vangogh"]]
        user_folder = Path("database/workspace")

        # For each original image, create a unique folder and move all versions
        for original_image in temp_image_folder.glob("*.jpg"):

            # Generate a unique ID for this image group
            unique_id = f"{int(time.time_ns())}_{uuid.uuid4().hex[:6]}"
            group_folder = user_folder / unique_id
            group_folder.mkdir()

            # Move the original image
            new_original_path = group_folder / f"{unique_id}_original.png"
            shutil.move(str(original_image), str(new_original_path))

            # Move each styled version of the image
            original_name = original_image.stem
            for style_folder in style_folders:
                style_image = style_folder / f"{original_name}_fake.png"
                style_name = style_folder.parts[-3].split('_')[1]
                new_style_path = group_folder / f"{unique_id}_{style_name}.png"
                shutil.move(str(style_image), str(new_style_path))

        # Delete datasets folder after processing
        parent_path_data = Path("temporary_data/datasets")
        if parent_path_data.exists():
            shutil.rmtree(parent_path_data)

        # Delete results folder after processing
        parent_path_results = Path("temporary_data/results")
        if parent_path_results.exists():
            shutil.rmtree(parent_path_results)

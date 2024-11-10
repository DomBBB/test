"""
This file defines the `MainPage` class, which serves as the landing page for the Art Studio App.
It provides users with a welcoming interface, navigational links, and a preview of the app’s
functionality, including the ability to view a random pair of original and edited images from
the gallery.
"""

# Import PyQT5 for GUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor

# Import libraries
import random
from pathlib import Path

# Import toolbar
from ui.toolbar_helper import setup_toolbar


class MainPage(QWidget):
    """
    Main page for the Art Studio App, including navigation toolbar, welcome message,
    random image display, and navigation buttons for different sections.
    """

    # Signals for navigation to other pages
    go_to_main = pyqtSignal()
    go_to_upload = pyqtSignal()
    go_to_workspace = pyqtSignal()
    go_to_gallery = pyqtSignal()

    def __init__(self):
        """
        Initializes the main page layout, setting up the toolbar, welcome message,
        random image display, and navigation buttons.
        """

        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the main page layout, adding toolbar, welcome message, random image display,
        navigation buttons, and footer with creator information.
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

        # Scrollable area for main content with padding and spacing
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(40)

        # Set background color for the page
        self.setStyleSheet("background-color: #f7f9fc;")

        # Title label centered at the top
        title_label = QLabel("Welcome to ARTify Studio")
        title_label.setFont(QFont("Arial", 30, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333333;")
        # Add to the page
        content_layout.addWidget(title_label)

        #####################################################################
        #                                                                                                                                      #
        # Content Layout                                                                                                            #
        #                                                                                                                                      #
        #####################################################################

        #####################################################################
        # Top Content                                                                                                                 #
        #####################################################################

        # Top layout with a description on the left and images on the right
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)

        # Left side: description section with app info
        description_layout = QVBoxLayout()
        description_layout.setAlignment(Qt.AlignCenter)
        description_label = QLabel(
            "Transform your photos into masterpieces inspired by iconic artists.\n\n"
            "Using advanced deep learning models, ARTify Studio reimagines your images "
            "with the styles of Monet, Van Gogh, Cezanne, and Ukiyoe. Start by uploading a photo, "
            "explore the workspace to apply effects and filters, and store your masterpiece in the gallery.\n\n"
            "Get creative and make art that’s truly unique!")
        description_label.setFont(QFont("Arial", 14))
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("color: #555555; padding-left: 40px;")
        description_label.setWordWrap(True)
        description_layout.addWidget(description_label)
        # Add to the layout
        top_layout.addLayout(description_layout, stretch=1)

        # Right side: Random gallery images display
        self.image_container = QVBoxLayout()
        self.image_container.setAlignment(Qt.AlignCenter)
        # Two QLabel widgets to display original and edited images
        self.original_image_label = QLabel()
        self.edited_image_label = QLabel()
        image_row = QHBoxLayout()
        image_row.addWidget(self.original_image_label)
        image_row.addWidget(self.edited_image_label)
        self.image_container.addLayout(image_row)
        # Button to load a random image
        randomize_button = QPushButton("Show Random Image")
        randomize_button.setFont(QFont("Arial", 14))
        randomize_button.setStyleSheet(
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }")
        randomize_button.clicked.connect(self.load_random_image)
        self.image_container.addWidget(randomize_button, alignment=Qt.AlignCenter)
        # Load an initial random image
        self.load_random_image()
        # Add to the layout
        top_layout.addLayout(self.image_container, stretch=1)

        # Add to the page
        content_layout.addLayout(top_layout)

        #####################################################################
        # Middle Content                                                                                                            #
        #####################################################################

        # Empty divider
        divider = QFrame()
        divider.setStyleSheet("color: #f7f9fc;")
        # Add to the page
        content_layout.addWidget(divider)

        # Navigation button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_style = (
            "QPushButton { background-color: #1976D2; color: white; padding: 8px 16px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #0F4C81; }"
        )

        # Upload button to navigate to the upload page
        self.upload_button = QPushButton("\n\n\n\n\nUpload Image\n\n\n\n\n")
        self.upload_button.setFont(QFont("Arial", 14.5))
        self.upload_button.setStyleSheet(button_style)
        self.upload_button.clicked.connect(self.go_to_upload.emit)
        # Add to the layout
        button_layout.addWidget(self.upload_button)

        # Workspace button to navigate to the workspace
        self.workspace_button = QPushButton("\n\n\n\n\nWorkspace\n\n\n\n\n")
        self.workspace_button.setFont(QFont("Arial", 14.5))
        self.workspace_button.setStyleSheet(button_style)
        self.workspace_button.clicked.connect(self.go_to_workspace.emit)
        # Add to the layout
        button_layout.addWidget(self.workspace_button)

        # Gallery button to navigate to the gallery
        self.gallery_button = QPushButton("\n\n\n\n\nGallery\n\n\n\n\n")
        self.gallery_button.setFont(QFont("Arial", 14.5))
        self.gallery_button.setStyleSheet(button_style)
        self.gallery_button.clicked.connect(self.go_to_gallery.emit)
        # Add to the layout
        button_layout.addWidget(self.gallery_button)

        # Add to the page
        content_layout.addLayout(button_layout)

        #####################################################################
        # Footer                                                                                                                           #
        #####################################################################

        # Footer section
        footer_layout = QVBoxLayout()
        footer_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("color: #cccccc;")
        # Add to the layout
        footer_layout.addWidget(divider)

        # Footer text displaying credits
        footer_label = QLabel(
            "Developed by Katja Zimmermann and Dominik Buchegger | Powered by CycleGAN (https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)"
        )
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setFont(QFont("Arial", 10))
        footer_label.setStyleSheet("color: #777777;")
        # Add to the layout
        footer_layout.addWidget(footer_label)

        # Add to the page
        content_layout.addLayout(footer_layout)

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

    def load_random_image(self):
        """
        Loads a random original and edited image from the gallery folder and displays them side-by-side.
        """

        # Location where the gallery images are stored
        gallery_path = Path("database/gallery")
        folders = list(gallery_path.glob("*"))

        # If there are images in the gallery
        if folders:
            # Select a random image folder
            selected_folder = random.choice(folders)
            # Select the original image
            original_image_path = selected_folder / f"{selected_folder.name}_original.png"
            # Select a random edited image
            edited_images = list(selected_folder.glob(f"{selected_folder.name}_*.png"))
            edited_image_path = random.choice([img for img in edited_images if "original" not in img.name])

            # Load and scale the images side-by-side
            original_pixmap = QPixmap(str(original_image_path)).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            edited_pixmap = QPixmap(str(edited_image_path)).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Display the images
            self.original_image_label.setPixmap(original_pixmap)
            self.edited_image_label.setPixmap(edited_pixmap)
        # If there are no images in the gallery
        else:
            # Create a placeholder image
            placeholder_pixmap = QPixmap(400, 400)
            placeholder_pixmap.fill(Qt.lightGray)
            painter = QPainter(placeholder_pixmap)
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(placeholder_pixmap.rect(), Qt.AlignCenter, "No images in gallery")
            painter.end()

            # Display the placeholder on both image labels
            self.original_image_label.setPixmap(placeholder_pixmap)
            self.edited_image_label.setPixmap(placeholder_pixmap)

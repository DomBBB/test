"""
This module defines the main application window for the Art Studio App.
It manages different pages within the app, including the main page, upload page,
workspace, editor, and gallery. It also sets up navigation between these pages
and configures the main window settings such as title, icon, and window size.

The main function serves as the entry point, launching the application
and displaying the main window.
"""

# Import PyQT5 for GUI
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Import libraries
import sys

# Import pages
from ui.main_page import MainPage
from ui.upload_page import UploadPage, NewUploadPage, SampleSelectionPage, ProgressBarPage
from ui.workspace_page import WorkspacePage, EditorPage
from ui.gallery_page import GalleryPage


class ArtStudioApp(QMainWindow):
    """
    Main application window for the Art Studio App.
    This class manages the main window settings, layout, and different pages display.
    """

    def __init__(self):
        """
        Initializes the main window, sets the title, adjusts the size,
        centers the window on the screen, and loads the main page.
        """
        super().__init__()
        # Set the window title for the main application
        self.setWindowTitle("ARTify Studio")
        # Set the app icon
        self.setWindowIcon(QIcon("assets/app_icon.ico"))
        # Set scalable size and center the window
        self.resize_and_center()
        # Display the main page on startup
        self.show_main_page()

    def resize_and_center(self):
        """
        Sets the main window size to 80% of the screen resolution for adaptability
        across different screen sizes, and centers the window on the screen.
        """
        # Get screen resolution and calculate 80% of available width and height
        screen = QApplication.primaryScreen().availableGeometry()
        width, height = int(screen.width() * 0.8), int(screen.height() * 0.8)
        self.my_sizing = [width, height]

        # Disable the help button across the application
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DisableWindowContextHelpButton)

        # Set the calculated width and height for the main window size
        self.setGeometry(0, 0, width, height)

        # Center the main window on the screen
        self.move((screen.width() - width) // 2, (screen.height() - height) // 2)

    def show_main_page(self):
        """
        Displays the MainPage within the main window.
        """
        # Instantiate the main page
        self.main_page = MainPage()

        # Connect signals from main page to navigate to different sections
        self.main_page.go_to_main.connect(self.show_main_page)
        self.main_page.go_to_upload.connect(self.show_image_upload)
        self.main_page.go_to_workspace.connect(self.show_workspace)
        self.main_page.go_to_gallery.connect(self.show_gallery)

        # Set main page as central content in the window
        self.setCentralWidget(self.main_page)

    def show_image_upload(self):
        """
        Displays the UploadPage for uploading or selecting images.
        """
        # Instantiate upload page
        self.upload_page = UploadPage()

        # Connect signals from upload page to navigate to different sections
        self.upload_page.go_to_main.connect(self.show_main_page)
        self.upload_page.go_to_upload.connect(self.show_image_upload)
        self.upload_page.go_to_workspace.connect(self.show_workspace)
        self.upload_page.go_to_gallery.connect(self.show_gallery)

        # Connect specific signals to navigate to New Upload and Sample Selection pages
        self.upload_page.go_to_new_upload.connect(self.show_new_upload_page)
        self.upload_page.go_to_sample_selection.connect(self.show_sample_selection_page)

        # Set upload page as central content in the window
        self.setCentralWidget(self.upload_page)

    def show_new_upload_page(self):
        """
        Displays the New Upload Page for uploading user-selected images.
        """
        # Instantiate new upload page
        self.new_upload_page = NewUploadPage()

        # Connect signals from new upload page to navigate to different sections
        self.new_upload_page.go_to_main.connect(self.show_main_page)
        self.new_upload_page.go_to_upload.connect(self.show_image_upload)
        self.new_upload_page.go_to_workspace.connect(self.show_workspace)
        self.new_upload_page.go_to_gallery.connect(self.show_gallery)

        # Navigate to the progress bar page after image selection
        self.new_upload_page.go_to_progress_bar.connect(self.show_progress_bar_page)

        # Set new upload page as central content in the window
        self.setCentralWidget(self.new_upload_page)

    def show_sample_selection_page(self):
        """
        Displays the Sample Selection Page for choosing sample images.
        """
        # Instantiate sample selection page
        self.sample_selection_page = SampleSelectionPage()

        # Connect signals from sample selection page to navigate to different sections
        self.sample_selection_page.go_to_main.connect(self.show_main_page)
        self.sample_selection_page.go_to_upload.connect(self.show_image_upload)
        self.sample_selection_page.go_to_workspace.connect(self.show_workspace)
        self.sample_selection_page.go_to_gallery.connect(self.show_gallery)

        # Navigate to the progress bar page after sample selection
        self.sample_selection_page.go_to_progress_bar.connect(self.show_progress_bar_page)

        # Set sample selection page as central content in the window
        self.setCentralWidget(self.sample_selection_page)

    def show_progress_bar_page(self, selected_images):
        """
        Displays the Progress Bar Page that shows the progress of image processing.

        Parameters:
            selected_images (list): List of selected images to process.
        """
        # Instantiate progress bar page
        self.progress_bar_page = ProgressBarPage(selected_images, self.my_sizing)

        # Navigate to the workspace page after processing (incl. error handling)
        self.progress_bar_page.go_to_workspace.connect(self.show_workspace)
        self.progress_bar_page.go_to_main.connect(self.show_main_page)

        # Set progress bar page as central content in the window
        self.setCentralWidget(self.progress_bar_page)

    def show_workspace(self):
        """
        Displays the Workspace Page for managing and editing images.
        """
        # Instantiate workspace page
        self.workspace_page = WorkspacePage()

        # Connect signals from workspace page to navigate to different sections
        self.workspace_page.go_to_main.connect(self.show_main_page)
        self.workspace_page.go_to_upload.connect(self.show_image_upload)
        self.workspace_page.go_to_workspace.connect(self.show_workspace)
        self.workspace_page.go_to_gallery.connect(self.show_gallery)

        # Navigate to the editor page for detailed editing
        self.workspace_page.go_to_editor.connect(self.show_editor_page)

        # Set workspace page as central content in the window
        self.setCentralWidget(self.workspace_page)

    def show_editor_page(self, selected_image):
        """
        Displays the Editor Page for detailed image editing.

        Parameters:
            selected_image (str): Path of the selected image to edit.
        """
        # Instantiate editor page
        self.editor_page = EditorPage(selected_image)

        # Connect signals from editor page to navigate to different sections
        self.editor_page.go_to_main.connect(self.show_main_page)
        self.editor_page.go_to_upload.connect(self.show_image_upload)
        self.editor_page.go_to_workspace.connect(self.show_workspace)
        self.editor_page.go_to_gallery.connect(self.show_gallery)

        # Set editor page as central content in the window
        self.setCentralWidget(self.editor_page)

    def show_gallery(self):
        """
        Displays the Gallery Page to view saved images.
        """
        # Instantiate gallery page
        self.gallery_page = GalleryPage()

        # Connect signals from gallery page to navigate to different sections
        self.gallery_page.go_to_main.connect(self.show_main_page)
        self.gallery_page.go_to_upload.connect(self.show_image_upload)
        self.gallery_page.go_to_workspace.connect(self.show_workspace)
        self.gallery_page.go_to_gallery.connect(self.show_gallery)

        # Set the EditorPage as the central widget
        self.setCentralWidget(self.gallery_page)


def main():
    """
    Main entry point for the application. Initializes the QApplication,
    opens the main application window, and starts the event loop.
    """
    # Initialize the application
    app = QApplication(sys.argv)
    # Create an instance of the main app window
    window = ArtStudioApp()
    # Display the main window
    window.show()
    # Run the application event loop and exit on close
    sys.exit(app.exec_())

# Execute main function if this file is run directly
if __name__ == "__main__":
    main()

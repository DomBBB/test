# Import PyQT5 for GUI
from PyQt5.QtWidgets import QToolBar, QAction


def setup_toolbar(parent, show_main, show_image_upload, show_workspace, show_gallery):
    """
    Creates a shared toolbar with navigation actions for Home, Image Upload,
    Workspace, and Gallery.

    Parameters:
        parent (QWidget): The widget to attach the toolbar to.
        show_main (function): Function to call when "Home" is selected.
        show_image_upload (function): Function to call when "Image Upload" is selected.
        show_workspace (function): Function to call when "Workspace" is selected.
        show_gallery (function): Function to call when "Gallery" is selected.

    Returns:
        QToolBar: The configured toolbar with the specified actions.
    """
    # Initialize the toolbar with a title and attach it to the parent widget
    toolbar = QToolBar("Main Navigation", parent)
    # Prevent the toolbar from being moved
    toolbar.setMovable(False)

    # Create and add "Home" action
    main_action = QAction("Home", parent)
    # Connect action to show_main function
    main_action.triggered.connect(show_main)
    # Add action to the toolbar
    toolbar.addAction(main_action)

    # Create and add "Image Upload" action
    upload_action = QAction("Image Upload", parent)
    # Connect action to show_image_upload function
    upload_action.triggered.connect(show_image_upload)
    # Add action to the toolbar
    toolbar.addAction(upload_action)

    # Create and add "My Workspace" action
    workspace_action = QAction("My Workspace", parent)
    # Connect action to show_workspace function
    workspace_action.triggered.connect(show_workspace)
    # Add action to the toolbar
    toolbar.addAction(workspace_action)

    # Create and add "Gallery" action
    gallery_action = QAction("Gallery", parent)
    # Connect action to show_gallery function
    gallery_action.triggered.connect(show_gallery)
    # Add action to the toolbar
    toolbar.addAction(gallery_action)

    # Return the configured toolbar
    return toolbar

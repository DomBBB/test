"""
This module provides functionality to run the test script for a CycleGAN model.
The CycleGAN model uses pretrained checkpoints to transform images
with a specific artistic style.

For more information on CycleGAN, visit:
https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix

The pretrained checkpoints and the example images are downloaded from:
https://efrosgans.eecs.berkeley.edu/cyclegan/
"""

# Import libraries
import subprocess
import sys
import os
from pathlib import Path


def run_test_script(model_name):
    """
    Executes the CycleGAN test script with specified model checkpoints
    to apply style transfer on images.

    Parameters:
        model_name (str): The name of the model to use for the CycleGAN.

    Returns:
        bool or str: Returns False if the script runs successfully. If an error
                           occurs, it returns the error message as a string.

    This function builds the necessary command to execute `test.py` within
    the CycleGAN directory. It sets up paths for input images, checkpoints,
    and output results. The function then uses subprocess to run the command,
    capturing any output or errors for logging purposes.
    """

    # Define the base directory for the project (two levels up from this script's location)
    base_dir = Path(__file__).parent.parent

    # Define the command to run the CycleGAN test script
    command = [
        sys.executable, # Use the current Python interpreter
        str(base_dir / "CycleGAN" / "test.py"), # Path to the test.py script
        '--dataroot', str(base_dir / "temporary_data" / "datasets" / "images" / "testB"), # Input images path
        '--name', model_name, # Model name
        '--checkpoints_dir', str(base_dir / "CycleGAN" / "checkpoints"), # Checkpoints directory
        '--model', "test", # Specify test mode
        '--direction', "BtoA", # Specify transformation direction (image to style)
        '--results_dir', str(base_dir / "temporary_data" / "results"), # Output directory for results
        '--no_dropout', # Disable dropout for inference
        '--gpu_ids', "-1" # Use CPU by setting GPU ID to -1
    ]
    try:
        # Run the command using subprocess, capturing stdout and stderr
        result = subprocess.run(
            command,
            check=True, # Raises an exception if the command fails
            stdout=subprocess.PIPE, # Capture standard output
            stderr=subprocess.PIPE, # Capture standard error
            text=True, # Decode output as text instead of bytes
            cwd=base_dir # Run the command from the base directory
        )
        # Output the result from the script if it runs successfully (return False)
        print("Output from test.py:")
        print(result.stdout)
        return False
    except subprocess.CalledProcessError as e:
        # Output the standard error if process error is caught (also return the error)
        print("An error occurred while executing test.py:")
        print(e.stderr)
        return e.stderr

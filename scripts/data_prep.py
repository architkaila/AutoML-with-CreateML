import os
import shutil
import pandas as pd
import argparse

def create_directory(source, dest_train, dest_test):
    """
    This function creates the train and test directories

    Args:
        source (str): The path to the source directory
        dest_train (str): The path to the train directory
        dest_test (str): The path to the test directory

    Returns:
        None
    """
    
    print("[INFO] Creating the train and test directories...")

    # Create the train directory if it does not exist
    
    if os.path.exists(dest_train):
        shutil.rmtree(dest_train)
    os.makedirs(dest_train)
    
    if os.path.exists(dest_test):
        shutil.rmtree(dest_test)

    # Copy the test images to the test directory
    shutil.copytree(os.path.join(source, 'test'), dest_test)

def prepare_train_data(source, dest_train):
    """
    This function takes the source directory and copies the images to the train and test directories

    Args:
        source (str): The path to the source directory
        dest_train (str): The path to the train directory
    
    Returns:
        None
    """

    # Read the train dataframe
    train_df = pd.read_csv(os.path.join(source, 'train.csv'))

    # Create a new directory for each of the training labels
    print("[INFO] Creating directories for each of the training labels...")
    for label in train_df['label'].unique():
        os.mkdir(os.path.join(dest_train, label))
    
    # Iterate over the rows of the train dataframe
    print("[INFO] Copying images to the train directory...")
    for index, row in train_df.iterrows():
        
        # Create the source path
        source_image_path = os.path.join(source, 'train', row["image_ID"])

        # Create the destination path
        destination_path = os.path.join(dest_train, row["label"])

        # Copy the image from the source to the destination
        shutil.copy(source_image_path, destination_path)
    
    # Iterate over the train label directories to get count of images in each label
    print("[INFO] Counting the number of images in each label...")
    for root, dirs, files in os.walk(dest_train):
        # Count the number of files in the current directory
        file_count = len(files)
        try:
            print(root.split("/")[3], file_count)
        except:
            pass


if __name__ == '__main__':

    # Initialize the parser
    parser = argparse.ArgumentParser(
        prog="Script to prepare the dataset for training and testing.",
        epilog="Example use: python scripts/data_prep.py --source ./data/raw_data --dest_train ./data/train --dest_test ./data/test"
    )

    # Add the command line arguments
    parser.add_argument("--source", default="./data/raw_data", help="Path to source directory containing data")
    parser.add_argument("--dest_train", default="./data/train", help="Path to destination training directory")
    parser.add_argument("--dest_test", default="./data/test", help="Path to destination testing directory")
    
    # Parse the arguments
    args = parser.parse_args()

    # Create the train and test directories
    create_directory(args.source, args.dest_train, args.dest_test)

    # Prepare the data
    prepare_train_data(args.source, args.dest_train)


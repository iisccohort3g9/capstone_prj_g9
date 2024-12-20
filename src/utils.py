import os
import kaggle

def download_kaggle_dataset(dataset_name, download_path):
    """
    Downloads a dataset from Kaggle.
    """
    os.makedirs(download_path, exist_ok=True)
    kaggle.api.dataset_download_files(dataset_name, path=download_path, unzip=True)
    print(f"Dataset downloaded to {download_path}")

if __name__ == "__main__":
    dataset_name = "gauravduttakiit/resume-dataset"
    download_path = "../data/raw/"
    download_kaggle_dataset(dataset_name, download_path)

import requests
import tempfile
import zipfile
import shutil
from pathlib import Path

from scanner import scan_folder
from risk_score import calculate_global_score, get_verdict


def download_repo_zip(repo_url, temp_dir):
    zip_url = repo_url.rstrip("/") + "/archive/refs/heads/main.zip"
    zip_path = Path(temp_dir) / "repo.zip"

    response = requests.get(zip_url, timeout=20)
    response.raise_for_status()

    zip_path.write_bytes(response.content)
    return zip_path


def extract_zip(zip_path, temp_dir):
    extract_path = Path(temp_dir) / "repo"

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path


def scan_github_repo(repo_url):
    temp_dir = tempfile.mkdtemp()

    try:
        zip_path = download_repo_zip(repo_url, temp_dir)
        repo_path = extract_zip(zip_path, temp_dir)

        file_results, total_files = scan_folder(repo_path)
        score = calculate_global_score(file_results, total_files)
        verdict = get_verdict(score)

        return score, verdict, file_results, total_files

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
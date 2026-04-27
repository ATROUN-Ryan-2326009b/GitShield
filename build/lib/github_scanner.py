import requests
import tempfile
import zipfile
import shutil
from pathlib import Path

from scanner import scan_folder
from risk_score import calculate_global_score, get_verdict


def normalize_github_url(repo_url):
    repo_url = repo_url.strip()

    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]

    return repo_url.rstrip("/")


def build_zip_url(repo_url, branch):
    repo_url = normalize_github_url(repo_url)
    return f"{repo_url}/archive/refs/heads/{branch}.zip"


def download_repo_zip(repo_url, temp_dir):
    branches_to_try = ["main", "master"]
    zip_path = Path(temp_dir) / "repo.zip"

    last_error = None

    for branch in branches_to_try:
        zip_url = build_zip_url(repo_url, branch)

        try:
            response = requests.get(zip_url, timeout=30)

            if response.status_code == 200:
                zip_path.write_bytes(response.content)
                return zip_path, branch

            last_error = f"Branch '{branch}' returned HTTP {response.status_code}"

        except requests.RequestException as error:
            last_error = str(error)

    raise RuntimeError(f"Unable to download repository ZIP. Last error: {last_error}")


def extract_zip(zip_path, temp_dir):
    extract_path = Path(temp_dir) / "repo"

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path


def scan_github_repo(repo_url):
    temp_dir = tempfile.mkdtemp()

    try:
        zip_path, branch = download_repo_zip(repo_url, temp_dir)
        repo_path = extract_zip(zip_path, temp_dir)

        file_results, total_files, skipped_files = scan_folder(repo_path)
        score = calculate_global_score(file_results, total_files)
        verdict = get_verdict(score)

        return {
            "repo_url": normalize_github_url(repo_url),
            "branch": branch,
            "score": score,
            "verdict": verdict,
            "file_results": file_results,
            "total_files": total_files,
            "skipped_files": skipped_files
        }

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
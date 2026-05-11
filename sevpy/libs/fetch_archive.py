from bs4 import BeautifulSoup
from packaging.version import Version
from pathlib import Path
from requests.exceptions import HTTPError
from tqdm import tqdm
import requests
import re
import json
import time

URL = "https://www.python.org/downloads/source/"

HOME_DIR = Path.home()
CACHE_DIR = HOME_DIR / ".cache" / "sevpy"

CACHE_FILE = CACHE_DIR / "python_versions.json"
TARBALL_DIR = CACHE_DIR /  "tarballs"

def process_versions(versions):
    processed = {}

    for version in versions:
        major, minor, patch = map(int, version.split("."))

        if major not in processed:
            processed[major] = {}

        if minor not in processed[major]:
            processed[major][minor] = []

        processed[major][minor].append(patch)

    # sort patches descending
    for major in processed:
        for minor in processed[major]:
            processed[major][minor].sort(reverse=True)

    return processed


def fetch_python_versions(debug=False):

    # Load cache if valid
    if CACHE_FILE.exists():

        with open(CACHE_FILE, "r") as f:
            data = json.load(f)

        # 24 hours cache validity
        if time.time() - data["timestamp"] < 24 * 3600:

            if debug:
                print("[DEBUG] Using cached versions.")

            # restore integer keys/types
            versions = {
                int(major): {
                    int(minor): list(map(int, patches))
                    for minor, patches in minors.items()
                }
                for major, minors in data["versions"].items()
            }

            return versions

    if debug:
        print(f"[DEBUG] Fetching versions from {URL}...")

    response = requests.get(
        URL,
        headers={
            "User-Agent": "sevpy"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    matches = re.findall(r"\d+\.\d+\.\d+", text)

    versions = sorted(
        set(matches),
        key=Version,
        reverse=True
    )

    versions = process_versions(versions)

    # Save cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with open(CACHE_FILE, "w") as f:
        json.dump(
            {
                "versions": versions,
                "timestamp": time.time()
            },
            f,
            indent=4
        )

    return versions

def resolve(version):

    versions = fetch_python_versions()

    latest = False

    if version.endswith("@latest"):
        latest = True
        version = version.replace("@latest", "")

    # global latest
    if version == "":
        major = max(versions.keys())
        minor = max(versions[major].keys())
        patch = versions[major][minor][0]

        return f"{major}.{minor}.{patch}"

    indices = version.split(".")

    if len(indices) == 1:

        major = int(indices[0])

        if major not in versions:
            raise ValueError(f"Python {major} not found")

        minor = max(versions[major].keys())

        patch = versions[major][minor][0]

    elif len(indices) == 2:

        major = int(indices[0])
        minor = int(indices[1])

        if major not in versions:
            raise ValueError(f"Python {major} not found")

        if minor not in versions[major]:
            raise ValueError(f"Python {major}.{minor} not found")

        patch = versions[major][minor][0]

    elif len(indices) == 3:

        major = int(indices[0])
        minor = int(indices[1])
        patch = int(indices[2])

    else:
        raise ValueError("Invalid version format")

    return f"{major}.{minor}.{patch}"

def download_archive(version, debug=False):

    filename = f"Python-{version}.tar.xz"

    url = f"https://www.python.org/ftp/python/{version}/{filename}"

    TARBALL_DIR.mkdir(parents=True, exist_ok=True)

    output_path = TARBALL_DIR / filename

    # skip if already downloaded
    if output_path.exists():

        if debug:
            print(f"[DEBUG] Using cached tarball: {output_path}")

        return output_path

    if debug:
        print(f"[DEBUG] Downloading {url}")

    try:
        response = requests.get(
            url,
            stream=True,
            headers={
                "User-Agent": "sevpy"
            }
        )

        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("[ERROR] Failed to download archive. Please check the version and try again. Maybe the version is not available yet or it is a pre-release one!")
        return None

    except Exception as e:
        print(f"[ERROR] An error occurred while downloading the archive: {e}")
        return None

    total_size = int(response.headers.get("content-length", 0))

    with open(output_path, "wb") as f:

        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=filename
        ) as pbar:

            for chunk in response.iter_content(chunk_size=8192):

                if chunk:

                    f.write(chunk)

                    pbar.update(len(chunk))

    if debug:
        print(f"[DEBUG] Saved archive to {output_path}")

    return output_path

if __name__ == "__main__":

    version = resolve("@latest")
    download_archive(version, debug=True)
    
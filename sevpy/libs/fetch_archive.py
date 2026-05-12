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

ARCHIVE_FORMATS = [
    "tar.xz",
    "tar.gz",
    "tgz",
    "tar.bz2",
    "zip",
]

def download_archive(version, debug=False):

    TARBALL_DIR.mkdir(parents=True, exist_ok=True)

    for ext in ARCHIVE_FORMATS:

        filename = f"Python-{version}.{ext}"

        url = f"https://www.python.org/ftp/python/{version}/{filename}"

        output_path = TARBALL_DIR / filename

        if output_path.exists():
            print(f"[INFO] Using cached tarball: {output_path}")
            return output_path

        try:
            response = requests.get(
                url,
                stream=True,
                headers={
                    "User-Agent": "sevpy"
                }
            )

            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            with open(output_path, "wb") as f:
                print(f"[INFO] Downloading source file {url}")
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

        except HTTPError:

            if debug:
                print(f"[DEBUG] {ext} not available for {version}")

            continue

        except Exception as e:
            print(f"[ERROR] {e}")
            return None

    print(f"[ERROR] No compatible archive found for Python {version}")
    return None

SIGNATURE_FORMATS = [
    "asc",
    "sig"
]

SIGNATURE_DIR = CACHE_DIR / "signatures"


def download_file(url, output_path, debug=False):

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        print(f"[INFO] Using cached file: {output_path}")
        return output_path

    response = requests.get(
        url,
        stream=True,
        headers={
            "User-Agent": "sevpy"
        }
    )

    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    with open(output_path, "wb") as f:

        print(f"[INFO] Downloading {url}")

        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=output_path.name
        ) as pbar:

            for chunk in response.iter_content(chunk_size=8192):

                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    if debug:
        print(f"[DEBUG] Saved file to {output_path}")

    return output_path


def fetch_signature(version, archive_path, debug=False):

    archive_path = Path(archive_path)

    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    SIGNATURE_DIR.mkdir(parents=True, exist_ok=True)

    archive_name = archive_path.name

    for ext in SIGNATURE_FORMATS:

        filename = f"{archive_name}.{ext}"

        url = f"https://www.python.org/ftp/python/{version}/{filename}"

        output_path = SIGNATURE_DIR / filename

        try:

            signature_path = download_file(
                url,
                output_path,
                debug=debug
            )

            if ext == "sig":

                crt_filename = f"{archive_name}.crt"

                crt_url = (
                    f"https://www.python.org/ftp/python/"
                    f"{version}/{crt_filename}"
                )

                crt_output_path = SIGNATURE_DIR / crt_filename

                try:

                    crt_path = download_file(
                        crt_url,
                        crt_output_path,
                        debug=debug
                    )

                    return {
                        "signature": signature_path,
                        "certificate": crt_path
                    }

                except HTTPError:

                    print(
                        "[ERROR] Signature exists but "
                        "certificate file is missing."
                    )

                    return None

            return {
                "signature": signature_path,
                "certificate": None
            }

        except HTTPError:

            if debug:
                print(f"[DEBUG] Signature format .{ext} not available")

            continue

        except Exception as e:

            print(f"[ERROR] {e}")

            return None

    print(f"[ERROR] No compatible signature found for {archive_name}")

    return None

if __name__ == "__main__":

    version = resolve("3.10.0")
    print(download_archive(version, debug=False))
    
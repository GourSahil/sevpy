"""
    Sevpy - A pythonic solution for python
    Author - Sahil Gour (aka Sevrus)
    Date - May 11, 2026
"""

VERSION = "0.0.1"

from libs.fetch_archive import resolve, download_archive, fetch_python_versions, fetch_signature
from libs.unpack import unpack_archive, verify_release
from libs.verify import extract_sigstore_metadata
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sevpy"
VERSIONS_CACHE_DIR = CACHE_DIR / "versions"
VERSIONS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class Sevpy:
    def __init__(self, version=""):
        self.version = resolve(version)
        print(f"[INFO] Attempting to Setup Python-{self.version}")

    def download(self, debug=False):
        return download_archive(self.version, debug=debug)

    def unpack(self, archive_path):
        return unpack_archive(archive_path, VERSIONS_CACHE_DIR)
    
    def fetch_signature(self, version, archive_path, debug=False):
        return fetch_signature(version, archive_path, debug=debug)

if __name__ == "__main__":
    sevpy = Sevpy("2.3@latest")
    archive_path = sevpy.download(debug=False)
    if not archive_path:
        print("[ERROR] Failed to download archive!")
        exit(1)
    signature = sevpy.fetch_signature(sevpy.version, archive_path, debug=False)
    if not signature:
        print("[ERROR] Failed to fetch signature!")
        exit(1)
    if signature["certificate"]:
        metadata = extract_sigstore_metadata(signature["certificate"])
        identity = metadata["identity"]
        oidc_issuer = metadata["oidc_issuer"]
    else:
        identity = None
        oidc_issuer = None
    status = verify_release(
        archive_path=archive_path,
        signature_path=signature["signature"],
        certificate_path=signature["certificate"],
        identity=identity,
        oidc_issuer=oidc_issuer
    )
    if status:
        print("[INFO] Release verification successful!")
        unpack_archive(archive_path, VERSIONS_CACHE_DIR)
    else:
        print("[ERROR] Release verification failed!")
# Changelog

## May 12, 2026, 11:31 PM IST

### sevpy/sevpy.py
- Added the main `Sevpy` class to resolve Python versions, download archives, unpack releases, and fetch signatures.
- Configured local cache directories under `~/.cache/sevpy` and `versions`.
- Implemented a CLI-style `__main__` block for downloading, signature fetching, Sigstore metadata extraction, verification, and unpacking.

### sevpy/libs/fetch_archive.py
- Added Python version scraping from the official Python source downloads page.
- Implemented version caching with 24-hour validity and structured version processing.
- Added support for resolving partial version inputs such as major-only or major.minor.
- Added archive download support for multiple formats and cached downloads.
- Added reusable file download helper and signature fetching support.

### sevpy/libs/unpack.py
- Added archive unpacking support for tar and zip formats.
- Added helper to derive archive root directory names from common Python archive suffixes.

### sevpy/libs/verify.py
- Added GPG-based signature verification with auto-import of missing public keys from multiple keyservers.
- Added Sigstore verification support for modern `.sig` signatures and certificate metadata extraction.
- Added `verify_release` orchestration for both legacy `.asc` and modern `.sig` verification flows.

### sevpy/libs/init.py
- Added project directory initialization logic for creating cache directories.

---

## 11 May 2026, 4:13 PM IST

* Initialized the project
* Planned the flow of project
* Created README.md with project aim
* Added `sevpy.libs.init.create_dirs` to create required cache directories under `~/.cache/sevpy`
* Added `VERSION` constant in `sevpy/sevpy.py`
* Added `sevpy/libs/fetch_archive.py` with Python source version discovery, local caching, version resolution, and archive download support
* Implemented `fetch_python_versions`, `resolve`, and `download_archive` in `sevpy/libs/fetch_archive.py` with debug output and error handling
import tarfile
import zipfile
from pathlib import Path

def get_archive_root_name(path: Path):

    name = path.name

    suffixes = [
        ".tar.gz",
        ".tar.xz",
        ".tar.bz2",
        ".tgz",
        ".zip"
    ]

    for suffix in suffixes:

        if name.endswith(suffix):
            return name.removesuffix(suffix)

    return path.stem


def unpack_archive(archive_path, extract_to):

    archive_path = Path(archive_path)
    extract_to = Path(extract_to)

    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    extract_to.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Unpacking archive to: {extract_to}", end="\r")

    if tarfile.is_tarfile(archive_path):

        with tarfile.open(archive_path) as tar:
            tar.extractall(path=extract_to)

    elif zipfile.is_zipfile(archive_path):

        with zipfile.ZipFile(archive_path) as zip_ref:
            zip_ref.extractall(path=extract_to)

    else:
        raise ValueError(f"Unsupported archive format: {archive_path}")

    extracted_dir = extract_to / get_archive_root_name(archive_path)
    print(f"[INFO] Unpacked archive to: {extracted_dir}")
    return extracted_dir

import re
import subprocess
from pathlib import Path


KEYSERVERS = [
    "hkps://keys.openpgp.org",
    "hkps://keyserver.ubuntu.com",
    "hkp://keyserver.ubuntu.com:80"
]


def extract_missing_key(stderr):

    match = re.search(
        r"using .* key ([A-F0-9]+)",
        stderr
    )

    if match:
        return match.group(1)

    return None

def import_gpg_key(keyid):

    print("[INFO] Missing GPG public key detected.")
    print(f"[INFO] Required Key: {keyid}")

    choice = input(
        "[PROMPT] Fetch public key from servers? [Y/n]: "
    ).strip().lower()

    if choice not in ["", "y", "yes"]:
        print("[INFO] User declined key import.")
        return False

    for server in KEYSERVERS:

        print(f"\n[INFO] Trying keyserver: {server}")

        cmd = [
            "gpg",
            "--keyserver",
            server,
            "--recv-keys",
            keyid
        ]

        print("[INFO] Importing key with command:\n")
        print(" ".join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            print(
                "[INFO] Public key imported successfully."
            )

            print(result.stderr)

            return True

        print(
            f"[WARN] Failed using server: {server}"
        )

        if result.stderr:
            print(result.stderr)

    print("[ERROR] All keyservers failed.")

    return False

def verify_gpg_signature(signature_path, archive_path):

    cmd = [
        "gpg",
        "--verify",
        str(signature_path),
        str(archive_path)
    ]

    print(f"[INFO] Verifying Signature:\n")
    print(" ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    #
    # Success
    #
    if result.returncode == 0:

        print(result.stderr)

        print("[INFO] Signature verification successful!")

        return True

    #
    # Missing public key
    #
    if "No public key" in result.stderr:

        keyid = extract_missing_key(result.stderr)

        if keyid:

            imported = import_gpg_key(keyid)

            if imported:

                print("[INFO] Retrying verification...\n")

                retry = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True
                )

                if retry.returncode == 0:

                    print(retry.stderr)

                    print(
                        "[INFO] Signature verification successful!"
                    )

                    return True

                print("[ERROR] Verification still failed.")
                print(retry.stderr)

                return False

    print("[ERROR] Verification failed.")
    print(result.stderr)

    return False


def verify_sigstore_signature(
    archive_path,
    signature_path,
    certificate_path,
    identity,
    oidc_issuer
):

    print(f"[INFO] Verifying release using Sigstore...")
    print(f"\t* Signature: {signature_path}")
    print(f"\t* Certificate: {certificate_path}")
    print(f"\t* Identity: {identity}")
    print(f"\t* OIDC Issuer: {oidc_issuer}")

    cmd = [
        "sigstore",
        "verify",
        "identity",

        "--cert",
        str(certificate_path),

        "--signature",
        str(signature_path),

        "--cert-identity",
        identity,

        "--cert-oidc-issuer",
        oidc_issuer,

        str(archive_path)
    ]

    print(f"[INFO] Verifying Signature:\n")
    print(" ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        print(result.stdout)

        print("[INFO] Signature verification successful!")

        return True

    print("[ERROR] Verification failed.")
    print(result.stderr)

    return False


def verify_release(
    archive_path,
    signature_path,
    certificate_path=None,
    identity=None,
    oidc_issuer=None
):

    archive_path = Path(archive_path)
    signature_path = Path(signature_path)

    if not archive_path.exists():
        raise FileNotFoundError(
            f"Archive not found: {archive_path}"
        )

    if not signature_path.exists():
        raise FileNotFoundError(
            f"Signature not found: {signature_path}"
        )

    signature_ext = signature_path.suffix.lower()

    #
    # Legacy OpenPGP verification
    #
    if signature_ext == ".asc":

        return verify_gpg_signature(
            signature_path,
            archive_path
        )

    #
    # Modern Sigstore verification
    #
    elif signature_ext == ".sig":

        if certificate_path is None:
            raise ValueError(
                "Sigstore verification requires "
                "a certificate file."
            )

        if identity is None:
            raise ValueError(
                "Sigstore verification requires "
                "an identity."
            )

        if oidc_issuer is None:
            raise ValueError(
                "Sigstore verification requires "
                "an OIDC issuer."
            )

        return verify_sigstore_signature(
            archive_path,
            signature_path,
            certificate_path,
            identity,
            oidc_issuer
        )

    raise ValueError(
        f"Unsupported signature format: "
        f"{signature_ext}"
    )
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def extract_sigstore_metadata(cert_path):

    with open(cert_path, "rb") as f:
        cert_data = f.read()

    cert = x509.load_pem_x509_certificate(
        cert_data,
        default_backend()
    )

    identity = None
    oidc_issuer = None

    #
    # Extract email identity
    #
    try:

        san = cert.extensions.get_extension_for_class(
            x509.SubjectAlternativeName
        )

        emails = san.value.get_values_for_type(
            x509.RFC822Name
        )

        if emails:
            identity = emails[0]

    except Exception:
        pass

    #
    # Extract Sigstore OIDC issuer
    #
    for ext in cert.extensions:

        oid = ext.oid.dotted_string

        if oid == "1.3.6.1.4.1.57264.1.1":

            oidc_issuer = ext.value.value.decode()

    return {
        "identity": identity,
        "oidc_issuer": oidc_issuer
    }
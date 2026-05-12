# Sevpy - A pythonic solution for python itself
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sevpy is a user-local Python source installer for Linux that provides clean multi-version Python installations without modifying system Python.
A Predictable system-like Python installs without shell hacks.

---

## Idea
> Most Linux distributions only package a limited set of Python versions, and managing multiple interpreters consistently across systems can become messy. So I came up with an idea to provide an interactive but stable approach to use different python versions.

I wanna clearly state some points ->
* Python will be source compiled.
* **GPG** signatures will be verified from source.
* **Tkinter** Support is made optional, by default it will be enabled. You can also disable it.
* **Idle** is also installed if **Tkinter** enabled.
* **User local installation** -> Python is installed locally for the current user to prevent conflicts with the system-wide Python installation.

---

## Benefits
- Clean user-local Python installations
- No modification of system Python
- No shell shims or PATH hacks
- Multiple Python versions can coexist
- Native-feeling interpreter usage
- Simple installation and removal
- Optional Tkinter and Idle support
- Verified source downloads using GPG
- Usage will become easy as shown in example
```bash
    python3.12 -m pip install requests # python3.12 
    python3.10 -m pip install requests # python3.10
```

---

## Requirement
* Linux Operating System
* Currently tested on **Arch Linux**

---

## Output

* Python-3.14.5
```bash
[INFO] Attempting to Setup Python-3.14.5
[INFO] Downloading source file https://www.python.org/ftp/python/3.14.5/Python-3.14.5.tar.xz
Python-3.14.5.tar.xz: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 22.8M/22.8M [00:04<00:00, 4.91MB/s]
[INFO] Downloading https://www.python.org/ftp/python/3.14.5/Python-3.14.5.tar.xz.sig
Python-3.14.5.tar.xz.sig: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 97.0/97.0 [00:00<00:00, 339kB/s]
[INFO] Downloading https://www.python.org/ftp/python/3.14.5/Python-3.14.5.tar.xz.crt
Python-3.14.5.tar.xz.crt: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.01k/1.01k [00:00<00:00, 138kB/s]
[INFO] Verifying release using Sigstore...
        * Signature: /home/sahil/.cache/sevpy/signatures/Python-3.14.5.tar.xz.sig
        * Certificate: /home/sahil/.cache/sevpy/signatures/Python-3.14.5.tar.xz.crt
        * Identity: hugo@python.org
        * OIDC Issuer: https://github.com/login/oauth
[INFO] Verifying Signature:

sigstore verify identity --cert /home/sahil/.cache/sevpy/signatures/Python-3.14.5.tar.xz.crt --signature /home/sahil/.cache/sevpy/signatures/Python-3.14.5.tar.xz.sig --cert-identity hugo@python.org --cert-oidc-issuer https://github.com/login/oauth /home/sahil/.cache/sevpy/tarballs/Python-3.14.5.tar.xz

[INFO] Signature verification successful!
[INFO] Release verification successful!
[INFO] Unpacked archive to: /home/sahil/.cache/sevpy/versions/Python-3.14.5
```

* Python3.8
```bash
((venv) ) sahil@aether ~/Projects/sevpy ➜ python3 sevpy/sevpy.py 
[INFO] Attempting to Setup Python-3.8.20
[INFO] Downloading source file https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tar.xz
Python-3.8.20.tar.xz: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 18.1M/18.1M [00:03<00:00, 5.71MB/s]
[INFO] Downloading https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tar.xz.asc
Python-3.8.20.tar.xz.asc: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 833/833 [00:00<00:00, 1.91MB/s]
[INFO] Verifying Signature:

gpg --verify /home/sahil/.cache/sevpy/signatures/Python-3.8.20.tar.xz.asc /home/sahil/.cache/sevpy/tarballs/Python-3.8.20.tar.xz
gpg: Signature made Sat 07 Sep 2024 03:54:21 PM IST
gpg:                using RSA key E3FF2839C048B25C084DEBE9B26995E310250568
gpg: Good signature from "Łukasz Langa (GPG langa.pl) <lukasz@langa.pl>" [unknown]
gpg:                 aka "Łukasz Langa <rplktr@rplktr.com>" [unknown]
gpg:                 aka "Łukasz Langa <lukasz@python.org>" [unknown]
gpg:                 aka "Łukasz Langa <lukasz.langa@pyfound.org>" [unknown]
gpg:                 aka "Łukasz Langa <lukasz@edgedb.com>" [unknown]
gpg:                 aka "Łukasz Langa (Work e-mail account) <ambv@fb.com>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: E3FF 2839 C048 B25C 084D  EBE9 B269 95E3 1025 0568

[INFO] Signature verification successful!
[INFO] Release verification successful!
[INFO] Unpacked archive to: /home/sahil/.cache/sevpy/versions/Python-3.8.20
```

* Python-2.3.7
```bash
[INFO] Attempting to Setup Python-2.3.7
[INFO] Downloading source file https://www.python.org/ftp/python/2.3.7/Python-2.3.7.tgz
Python-2.3.7.tgz: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8.29M/8.29M [00:00<00:00, 11.7MB/s]
[INFO] Downloading https://www.python.org/ftp/python/2.3.7/Python-2.3.7.tgz.asc
Python-2.3.7.tgz.asc: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 189/189 [00:00<00:00, 366kB/s]
[INFO] Verifying Signature:

gpg --verify /home/sahil/.cache/sevpy/signatures/Python-2.3.7.tgz.asc /home/sahil/.cache/sevpy/tarballs/Python-2.3.7.tgz
[INFO] Missing GPG public key detected.
[INFO] Required Key: 6AF053F07D9DC8D2
[PROMPT] Fetch public key from servers? [Y/n]: y

[INFO] Trying keyserver: hkps://keys.openpgp.org
[INFO] Importing key with command:

gpg --keyserver hkps://keys.openpgp.org --recv-keys 6AF053F07D9DC8D2
[WARN] Failed using server: hkps://keys.openpgp.org
gpg: keyserver receive failed: No data


[INFO] Trying keyserver: hkps://keyserver.ubuntu.com
[INFO] Importing key with command:

gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys 6AF053F07D9DC8D2
[INFO] Public key imported successfully.
gpg: key 6AF053F07D9DC8D2: 2 duplicate signatures removed
gpg: key 6AF053F07D9DC8D2: public key "Martin v. Löwis <martin@v.loewis.de>" imported
gpg: Total number processed: 1
gpg:               imported: 1

[INFO] Retrying verification...

gpg: Signature made Tue 11 Mar 2008 11:39:32 PM IST
gpg:                using DSA key 6AF053F07D9DC8D2
gpg: Good signature from "Martin v. Löwis <martin@v.loewis.de>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: CBC5 4797 8A39 64D1 4B9A  B36A 6AF0 53F0 7D9D C8D2

[INFO] Signature verification successful!
[INFO] Release verification successful!
[INFO] Unpacked archive to: /home/sahil/.cache/sevpy/versions/Python-2.3.7
```
---

> If you wanna contribute in the project or wanna give your opinion or wanna suggest something, you can write an email to me at **[Here](mailto:itzsevrus@duck.com)**.
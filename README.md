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

> If you wanna contribute in the project or wanna give your opinion or wanna suggest something, you can write an email to me at **[Here](mailto:itzsevrus@duck.com)**.
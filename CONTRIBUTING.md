# Contributing to biz.dfch.AsdSte100Lookup

Thank you for your interest in contributing to **biz.dfch.AsdSte100Lookup**!  
This document describes how to propose changes, report bugs, and submit patches.

The project is licensed under the **GNU General Public License v3.0 (GPLv3)**.  
By contributing, you agree that your contributions will be licensed under the
same license as the project.

To contribute, clone the repository, create a branch, develop your changes and 
then create a pull request.

---

## 1. Code of Conduct

Please be respectful and constructive in all interactions.

This project has a `CODE_OF_CONDUCT.md`, you must follow it.

---

## 2. How to Ask Questions and Report Bugs

- **Bug reports**: Open an issue in the GitHub issue tracker:
  - URL: `https://github.com/dfch/biz.dfch.AsdSte100Lookup/issues`
  - Include:
    - Steps to reproduce
    - Expected behavior
    - Actual behavior
    - Environment details (OS, Python version, PROJECT_NAME version)
    - Relevant logs, stack traces, or screenshots where appropriate

- **Feature requests / ideas**: Also use the issue tracker, marking them as
  feature requests or enhancements.

Before opening a new issue, please **search existing issues** to avoid duplicates.

---

## 3. Development Setup

### 3.1. Prerequisites

- Python **3.11** and Python **3.12**
- `git`
- Recommended: `python -m venv`
- Recommended: `unittest`

### 3.2. Clone and create a virtual environment

```bash
git clone https://github.com/dfch/biz.dfch.AsdSte100Lookup.git
cd biz.dfchAsdSte100Lookup

python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate[.bat|.ps1]

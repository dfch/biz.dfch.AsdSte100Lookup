# biz.dfch.AsdSte100Lookup

[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)
[![Pylint and unittest](https://github.com/dfch/biz.dfch.AsdSte100Lookup/actions/workflows/ci.yml/badge.svg)](https://github.com/dfch/biz.dfch.AsdSte100Lookup/actions/workflows/ci.yml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=coverage)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dfch_biz.dfch.AsdSte100Lookup&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dfch_biz.dfch.AsdSte100Lookup)

_A dictionary lookup for [ASD-STE100 Issue 9](https://www.asd-ste100.org/index.html) manual_

* The program uses the dictionary words from the standard [ASD-STE100 Issue 9](https://www.asd-ste100.org/index.html) manual.
* The program lets you lookup dictionary words, technical nouns and technical verbs from that standard and shows
  - the "Approved" words in green, "Rejected" words in red, "Technical" word in dark green
  - the "Type" of the words
  - the "Meanings" for these words
  - the "STE examples" and "Non-STE examples" for these words
  - the "Alternatives" for the words
  - the "Spellings" and "Tenses" of these words in blue
  - the "Notes" in yellow
* The program also lets you lookup rules from the standard.

* The program lets you use regular expressions as the input.
* The program is written in Python (and tested with v3.11.2 on Microsoft Windows 11 and WSLv2 Debian x64).
* The program
  - Copyright by (c) 2025 Ronald Rink.
  - Licensed under "GNU General Public License v3" (GPLv3)
* ASD-STE100
  - Copyright by (c) [ASD](https://www.asd-europe.org/).
* I am in no way afiliated with ASD. ASD does not endorse my work.

## Setting up VSCode

In addition to my *user* `settings.json` this is the project specific `settings.json`:

```json
{
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "tests",
        "-t",
        ".",
        "-p",
        "test_*.py"
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}/src"
    ],
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}/src"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true
}
```

This is mainly used to:
* enable the tests find the `src`
* auto-complete modules starting with `biz....`

## Build as one-file executable

1. Download the files from the repository into a directory on your system. We refer to this directory as `<prj-root>`.
1. Under `<prj-root>` there is a directory with the name `src`. This is the directory with all the source files.
1. Virtual environment

    a. Also under `<prj-root>`, there is a directory with the name `venv`. This is the directory for a "virtual environment" under the Windows x64 operating system.
   
    b. Also under `<prj-root>`, there is a directory with the name `venvdeb`. This is the directory for a "virtual environment" under the Debian amd64 operating system.
   
    c. If you have a different operating system, you must create a "virtual environment" that is applicable to your operating system.

1. Activate the "virtual environment" for your operating system.
1. Use this command:

    a. This command builds the program into a single executable file for your operating system. This includes the Python runtime.

    b. The result is in the directory with the name `dist`. The name of the exutable is `AsdSte100Lookup` or `AsdSte100Lookup.exe`.

```bash
(venv) <prj-root> $ pyinstaller --clean --onefile --name AsdSte100Lookup \
  --add-data "./src/logging.conf:." \
  --add-data "./src/biz/dfch/asdste100lookup:./biz/dfch/asdste100lookup/" \
  -p "./src" \
  -p "./src/biz" \
  ./src/biz/__main__.py
```

```bash
(venv) <prj-root> $ pyinstaller --clean --onefile --name AsdSte100Lookup `
  --add-data "./src/logging.conf:." `
  --add-data "./src/biz/dfch/asdste100lookup:./biz/dfch/asdste100lookup/" `
  -p "./src" `
  -p "./src/biz" `
  ./src/biz/__main__.py
```

## Run

There are two ways to use the program.

1. Use the executable from the previous step.
2. Use the Python interpreter.

    a. Activate the "virtual environement" for your operating system.
    b. Make sure all necessary libraries are available.
    c. Use this command to change into the `src` directory: `cd src`.
    d. Operate this command: `python -m biz`.

3. After some time you see a prompt. Use this prompt to examine the dictionary.
4. You can use regular expressions in the prompt.

## Images

<img width="2808" height="1468" alt="image" src="https://github.com/user-attachments/assets/11d5f6c9-41d5-451a-bdc2-79499aef2ca4" />

<img width="2811" height="1356" alt="image" src="https://github.com/user-attachments/assets/739402ab-a5af-4512-acb1-2b6f03712911" />

<img width="2809" height="1577" alt="image" src="https://github.com/user-attachments/assets/e1d4a29a-fb53-4a44-a6f1-299fb787994e" />

<img width="2800" height="1393" alt="image" src="https://github.com/user-attachments/assets/0c1f5e81-df76-451b-8834-a73e32b09d20" />

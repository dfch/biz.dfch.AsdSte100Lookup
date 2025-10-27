# biz.dfch.AsdSte100Lookup

_A dictionary lookup for [ASD-STE100 Issue 9](https://www.asd-ste100.org/index.html) manual_

* The program uses the dictionary words from the [ASD-STE100 Issue 9](https://www.asd-ste100.org/index.html) manual.
* The program lets you lookup words from that manual and shows
  - the "Approved" words in green, and "Rejected" words in red,
  - the "Type" of the words,
  - the "Meanings" for these words,
  - the "STE examples" and "Non-STE examples" for these words,
  - the "Alternatives" for the words,
  - the "Spellings" and "Tenses" in blue,
  - the "Notes" in yellow.
* The program lets you use regular expressions as the input.
* The program is written in Python (and tested with v3.11.2 on Microsoft Windows 11 and WSLv2 Debian x64).
* The program
  - Copyright by (c) 2025 Ronald Rink.
  - Licensed under "GNU General Public License v3" (GPLv3)
* ASD-STE100
  - Copyright by (c) [ASD](https://www.asd-europe.org/).
* I am in no way afiliated with ASD. ASD does not endorse my work.

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

    b. The result is in the directory with the name `sub`. The name of the exutable is `AsdSte100Lookup` or `AsdSte100Lookup.exe`.

```
(venv) <prj-root> $ pyinstaller --clean --onefile --name AsdSte100Lookup \
  --add-data "./src/logging.conf:." \
  --add-data "./src/biz/dfch/asdste100lookup:./biz/dfch/asdste100lookup/" \
  -p "./src" \
  -p "./src/biz" \
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

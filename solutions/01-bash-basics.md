## Quick reference card

| Command | Full name                       | File-explorer equivalent         |
| ------- | ------------------------------- | -------------------------------- |
| `pwd`   | Print Working Directory         | Read the address bar             |
| `cd`    | Change Directory                | Double-click a folder            |
| `ls`    | List                            | Open a folder                    |
| `mkdir` | Make Directory                  | New folder                       |
| `mv`    | Move                            | Drag and drop / rename           |
| `cp`    | Copy                            | Copy-paste                       |
| `scp`   | Secure Copy                     | Copy to/from remote server       |
| `touch` | Touch                           | New empty file                   |
| `rm`    | Remove                          | Delete                           |
| `find`  | Find                            | Search                           |
| `grep`  | Global Regular Expression Print | Ctrl+F in many files             |
| `sed`   | Stream Editor                   | Find-and-replace in a file       |
| `cat`   | Concatenate                     | Open file to read                |
| `head` / `tail` | First / last lines      | Scroll to top or bottom of file  |
| `wc`    | Word Count                      | Count lines in a file            |
| `clear` | Clear screen                    | Clear the terminal window        |
| `man`   | Manual                          | Help documentation               |
| `\|`    | Pipe                            | (no equivalent — chains actions) |

# Class 1 — Bash Basics and VS code

Throughout this class you can work on your computer or (optional but recommended) from the remote server **uc3** (`uc3.scc.kit.edu`). 

## 1. VS Code — interface and remote access

We use **VS Code** as our editor and terminal. The layout has four main areas:

```
||---------------------------------------------------------------||
||           ||              Editor               ||  Secondary  ||
|| Side bar  ||         (open files, code)        ||  side bar   ||
|| (folder)  ||-----------------------------------||   (LLMs)    ||
||           ||           Terminal                ||             ||
||---------------------------------------------------------------||
```

| Area | What it is | Open / toggle |
| ---- | ---------- | ------------- |
| **Side bar** (left) | File explorer — only shows files after you **Open Folder** (typically a git repo; we cover that next week) | `CTRL+B` |
| **Editor** (centre) | Where you read and edit files |  |
| **Second side bar** (right) | LLM use | `CTRL+ALT+B` |
| **Terminal** (bottom) | Run bash commands | `CTRL+J` |

### i. Privacy and telemetry (recommended because Microsoft sucks)

Press **`CTRL+,`** to open Settings, search for **`telemetry level`**, and set **Telemetry: Telemetry Level** to **`off`**.

### ii. Open a terminal

Press **`CTRL+J`** in VS Code to open the terminal panel at the bottom. If the shell is not bash, click the **`˅`** next to **`+`** in the terminal tab bar and select **Git Bash**.

### iii. Connect to UC3 (daily)

1. `CTRL+SHIFT+P` → **Connect to Host…** → select **uc3** → select **Linux**
2. Enter your **OTP + password or passphrase**

> When typing your password or passphrase in the VS Code terminal, **no characters appear**, that is normal. Type it and press Enter.

## 2. Terminal navigation with bash

Before we start doing data analysis, we need to be comfortable moving around the **filesystem** from a terminal. Think of Bash as a **text-based *file explorer***, every click-and-drag action has a command equivalent (also called shell command), and many tasks that would take hours in a GUI take seconds here.

| *File explorer*        | Bash              |
| ---------------------- | ----------------- |
| Click through folders  | `cd`, `ls`, `pwd` |
| Drag files to a folder | `mv`, `cp`        |
| Delete a file          | `rm`              |
| Search in a folder     | `find`, `grep`    |

### i. `pwd` — Print Working (current) Directory

Shows the full path of the directory (a.k.a. folder in Windows) you are currently in, *like reading the address bar in a file explorer*.

```bash
pwd
# Example output (uc3): /home/fr/fr_fr/fr_ad1149/bash-sandbox
# Example output (laptop): /Users/damseaux-a/Documents/FuFo/coding_course/coding-course/bash-sandbox
```

> Directories are separated with a `/` symbol.

---

### ii. `mkdir` — Make Directory

Creates a new directory called `data`.

```bash
mkdir data
```

---

### iii. `cd` — Change Directory

Moves you into another directory, *like click on a folder in file explorer*.

```bash
# enter the 'data/' subdirectory
cd data/
# go to an absolute path          
cd /home/fr/fr_fr/fr_ad1149/bash-sandbox/data
```

> An absolute path will always start with `/` (e.g. `/Users`), whereas a relative path (a path that only exists in your current directory) starts with the directory name (e.g. `data`).

#### `.` and `..` are current and parent directory

```bash
# move to the current directory (i.e. don't move)
cd .
# move to the parent (above/upper) directory             
cd ..                 
```

> *The last command* `cd ..` *is like using the back arrow in file explorer*.

#### `~` is your home directory

```bash
cd ~
```

---

### iv. `ls` — List

Lists files and directories, *what you see in the file explorer window*.

```bash
ls
```

---

### v. `mv` — Move (and rename)

Moves files and directories. *In a file explorer this is drag-and-drop*.

```bash
mv report.txt data/    # move file into data/
```

This command is also used to rename files.

```bash
mv old_name.txt new_name.txt
```

---

### vi. `cp` — Copy

Creates a copy of a file or a directory.

```bash
cp data/report.txt data/report_backup.txt
cp -r data/ data_backup/   # -r = recursive (needed for directories)
```

---

### vii. `scp` — Secure Copy

Copies files between your machine and a remote server (like uc3).

```bash
# copy files from the server
scp -r fr_ad1149@uc3:/home/fr/fr_fr/fr_ad1149/bash-sandbox/data .

# copy a directory to the server
scp -r dummy-dir/ fr_ad1149@uc3:/home/fr/fr_fr/fr_ad1149/bash-sandbox
```

> It is recommend to always use this command on your computer and not on the remote server.

---

### viii. `*` — Wildcard (glob)

The `*` is not a command, it is a pattern that Bash expands before running the command. It lets you target many files at once.

```bash
ls *                     # same as ls
ls *_post-processed.txt  # all post-processed files
```

Other useful patterns:

| Pattern          | Matches                        |
| ---------------- | ------------------------------ |
| `*`              | anything                       |
| `??-07-2024.txt` | exactly one character + `.txt` |
| `[0-9]*`         | names starting with a digit    |

## Exercise A — Download the course data from uc3

During the course, we are going to use the time-series being currently reccorded at Staufen, and a netCDF provided by Christopher Jung.

The exercise files for this course are stored on the remote server **uc3**. Download them to your local machine:

1. Create a local `processed_data` directory
2. Copy the course files from uc3 to that directory `/pfs/work9/workspace/scratch/fr_ad1149-coding-course/processed_data/`

> If you are not on UC3, the files should also sit in `X:/01_General/02_Central_infrastructure/SES_ModelLab/coding_course/exercises`. On macOS it is usually in `/Volumes/un042rd01/01_General/02_Central_infrastructure/SES_ModelLab/coding_course/exercises` instead.

**Solution:**

```bash
mkdir -p processed_data
scp -r fr_ab1234@uc3.scc.kit.edu:/pfs/work9/workspace/scratch/fr_ad1149-coding-course/processed_data/ .
```

Replace `fr_ab1234` with your bwUniCluster username (e.g. `fr_` + your Uni Freiburg username).

## Exercise B — Why the terminal beats the file explorer

Your research group receives daily exports from meteorological station **FF-MET-042**. Over two years, the data pipeline produced **1 440 files** (720 days × 2 versions each):

- `YYYY-MM-DD_raw-data.txt` — unprocessed sensor readings
- `YYYY-MM-DD_post-processed.txt` — cleaned, analysis-ready data

All files currently sit in `/pfs/work9/workspace/scratch/fr_ad1149-coding-course/exercises/`. Your task: 

1. Copy the folder `exercises/` to your current directory
2. Move only the post-processed files from `meteorological/incoming` into `meteorological/post-processed/`, leaving the raw files in place.
3. Delete all the January files from the second year because they have been corrupted

> If you are not on UC3, the files should also sit in `X:/01_General/02_Central_infrastructure/SES_ModelLab/coding_course/exercises`. On macOS it is usually in `/Volumes/un042rd01/01_General/02_Central_infrastructure/SES_ModelLab/coding_course/exercises` instead.

**Solution:**

```bash
cp -r /pfs/work9/workspace/scratch/fr_ad1149-coding-course/exercises/ .

# Move them
cd exercises/meteorological/
mv incoming/*_post-processed.txt post-processed/

# Remove files
cd post-processed/
rm 2024-01-*txt
```

## 4. More `bash` commands

### i. `rm` — Remove

Deletes files and directories. **There is no trash bin; deleted files are gone!**

```bash
rm old_plot.txt    # delete one file
rm *_raw-data.txt  # delete all matching files (uses *)
rm -r temp_folder/ # -r = recursive (needed for directories)
```

> Be careful with `rm`: double-check the path with `ls` before pressing Enter. A typo like `rm ~` can delete you entire drive.

---

### ii. `touch` — Create an empty file

Creates a new empty file, *like choosing **New file** in a file explorer.*

```bash
touch notes.txt
```

---

### iii. `find` — Find files

Locates files by name or properties, *like the search bar in a file explorer*.

```bash
find . -name "README.txt"
```

---

### iv. `grep` — Global Regular Expression Print

Searches for text inside files, *like Ctrl+F across many files at once*.

```bash
# lines containing NODATA
grep "NODATA" station_FF-MET-042_2024-Q1.txt
```

---

### v. `cat` — Concatenate and display

Prints a file to the terminal.

```bash
cat station_FF-MET-042_2024-Q1.txt
cat file1.txt > file2.txt              # move content from file1 to file2
cat file1.txt file2.txt > combined.txt # merge files
```

---

### vi. `head` / `tail` — First / last lines

```bash
head -5 data.csv          # first 5 lines
tail -20 log.txt          # last 20 lines
```

---

### vii. `wc` — Word Count

```bash
wc -l *.txt               # line count for each file
```
---

### viii. `clear` — Clear the terminal screen

```bash
clear
```

---

### iv. `sed` — Stream Editor

Edits text line by line. In this course we use it for find-and-replace inside a file.

```bash
# replace every "error" with "ERROR" and print the result (does NOT change the file)
sed 's/error/ERROR/g' log.txt

# write the result to a new file (> saves output to a file instead of the terminal)
sed 's/error/ERROR/g' log.txt > log_clean.txt
```

The substitution syntax is `s/old/new/g`, inside single quotes:

| Part | Meaning |
| ---- | ------- |
| `s` | **S**ubstitute — start a find-and-replace |
| `/error/` | Text to find (`old`) |
| `/ERROR/` | Text to replace it with (`new`) |
| `g` | **G**lobal — replace **all** matches on each line (without `g`, only the first match per line is replaced) |

> The `>` symbol is an **output redirect**: it sends command output to a file instead of the screen (and overwrites the file if it already exists).

---

### ix. `man` — Manual

```bash
man grep                  # full documentation for grep
```

---

### x. `|` — Pipe

Chains commands together so the output of the left command feeds into the right one.

```bash
# Count how many post-processed files exist
ls *_post-processed.txt | wc -l
```

## 5. Flags

For sake of time, I didn't mention all the **flags** used above. A flag (also called an **option**) modifies how a command behaves. Flags (generally) start with `-` and are placed after the command name.

General flags (used by several commands):

| Flag | Meaning |
| ---- | ------- |
| `-r` | Recursive — include subdirectories (used with `cp`, `scp`, `rm`) |
| `-p` | Parents — create missing parent directories (used with `mkdir -p`) |

`grep` flags:

| Flag | Meaning |
| ---- | ------- |
| `-n` | Show line numbers |
| `-c` | Count matching lines (prints a number, not the lines) |
| `-l` | List filenames that contain a match (not the matching lines) |
| `-o` | Print only the matching text (useful to count occurrences) |

`find` options:

| Flag | Meaning |
| ------ | ------- |
| `-name "pattern"` | Match files by name (supports `*` wildcards) |
| `-type f` | Only regular f*iles (not directories) |
| `-exec cmd {} \;` | Run `cmd` on each file found (`{}` = filename) |

`head` / `tail` / `wc` flags:

| Flag | Meaning |
| ---- | ------- |
| `-5` (head) | Show the first 5 lines (`-10` for 10 lines, etc.) |
| `-20` (tail) | Show the last 20 lines |
| `-l` (wc) | Line count only |

> Tip: run `man grep`, `man find`, or `grep --help` to see all available flags.

## 6. Exercise C (Bonus) — Find and replace missing values with `grep` and `sed`

The quarterly export `station_FF-MET-042_2024-Q1.txt` (in `exercises/nodata-replace/`) contains hourly records from station **FF-MET-042**. Some sensor readings failed and were stored as the string `NODATA`. Before analysis, every `NODATA` must be replaced with the numeric missing-value code `-9999`.

This exercise uses the flags from the section above.

**Solution:**

Use `sed` as shown above. The `g` flag replaces every `NODATA` on a line, not just the first one.

```bash
# Solution
sed 's/NODATA/-9999/g' station_FF-MET-042_2024-Q1.txt > station_FF-MET-042_2024-Q1_clean.txt

# Confirm no NODATA remains (-c should print 0)
grep -c "NODATA" station_FF-MET-042_2024-Q1_clean.txt

# Show only the lines that originally had NODATA, already cleaned
grep "NODATA" station_FF-MET-042_2024-Q1.txt | sed 's/NODATA/-9999/g'
```
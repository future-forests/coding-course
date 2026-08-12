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
| `head` / `tail` | First / last lines        | Scroll to top or bottom of file  |
| `wc`    | Word Count                      | Count lines in a file            |
| `clear` | Clear screen                    | Clear the terminal window        |
| `man`   | Manual                          | Help documentation               |
| `\|`    | Pipe                            | (no equivalent — chains actions) |

# Class 1 — Bash Basics

Before we start doing data analysis, we need to be comfortable moving around the **filesystem** from a terminal. Think of Bash as a **text-based *file explorer***, every click-and-drag action has a command equivalent (also called shell command), and many tasks that would take hours in a GUI take seconds here.


| *File explorer*        | Bash              |
| ---------------------- | ----------------- |
| Click through folders  | `cd`, `ls`, `pwd` |
| Drag files to a folder | `mv`, `cp`        |
| Delete a file          | `rm`              |
| Search in a folder     | `find`, `grep`    |


Throughout this class you will work on your computer and access files from the  remote server **uc3** (`uc3.scc.kit.edu`). If you don't have access to this folder, we will share the files on [...]. The exercises below use fake meteorological data files to practice.

## Let's start with our fist `bash` commands

### `pwd` — Print Working (current) Directory

Shows the full path of the directory (a.k.a. folder in Windows) you are currently in, *like reading the address bar in a file explorer*.

```bash
pwd
# Example output: /Users/damseaux-a/Documents/FuFo/fufo_coding_course
```

> Directories are separated with a `/` symbol.

---

### `cd` — Change Directory

Moves you into another directory, *like click on a folder in file explorer*.

```bash
cd data                        # enter the 'data' subdirectory (if it exists)
cd /Users/damseaux-a/Documents  # go to an absolute path
```

> An absolute path will always start with `/` (e.g. `/Users`), whereas a relative path (a path that only exists in your current directory) starts with the directory name (e.g. `data`).

#### `.` and `..` are current and parent directory

```bash
cd .                  # move to the current directory (i.e. don't move)
cd ..                 # move to the parent (above/upper) directory
```

> *The last command* `cd ..` *is like using the back arrow in file explorer*.

---

### `ls` — List

Lists files and directories, *what you see in the file explorer window*.

```bash
ls
```

---

### `mkdir` — Make Directory

Creates a new directory called `data`.

```bash
mkdir data
mkdir -p data/exercises    # -p creates parent folders if they don't exist yet
```

> `-p` is a "flag". See the end of this document for more information.

---

### `mv` — Move (and rename)

Moves files and directories. *In a file explorer this is drag-and-drop*.

```bash
mv report.txt archive/           # move file into archive/
```

This command is also used to rename files.

```bash
mv old_name.txt new_name.txt
```

---

### `cp` — Copy

Creates a copy of a file or a directory.

```bash
cp station_data.txt station_data_backup.txt
cp -r raw_files/ backup/         # -r = recursive (needed for directories)
```

---

#### `scp` — Secure Copy

Copies files between your machine and a remote server (like uc3).

```bash
# copy files from the server
scp fr_username@uc3.scc.kit.edu:/path/to/files/ data

# copy a directory to the server
scp -r data fr_username@uc3.scc.kit.edu:~/backup/
```

> It is recommend to always use this command on your computer and not on the remote server.

---

### `*` — Wildcard (glob)

The `*` is not a command, it is a pattern that Bash expands before running the command. It lets you target many files at once.

```bash
ls *_post-processed.txt          # all post-processed files
```

Other useful patterns:


| Pattern          | Matches                        |
| ---------------- | ------------------------------ |
| `*`              | anything                       |
| `??-07-2024.txt` | exactly one character + `.txt` |
| `[0-9]*`         | names starting with a digit    |

## Exercise 1 — Download the course data from uc3

During the course, we are going to use the time-series being currently reccorded at Staufen, and a netCDF provided by Christopher Jung.

The exercise files for this course are stored on the remote server **uc3**. Download them to your local machine:

1. Create a local `fufo_cc_data` directory
2. Copy the course files from uc3 to the directory above (path is `/path/to/fufo_coding_course/exercises/`)

**Solution:**

1. Create a local data directory:

```bash
mkdir -p data
```

2. Copy the course files from uc3 (replace `fr_username` with your university username):

```bash
scp -r fr_username@uc3.scc.kit.edu:/path/to/fufo_coding_course/exercises/ data/
```

## Exercise 2 — Why the terminal beats the file explorer

### Scenario

Your research group receives daily exports from meteorological station **FF-MET-042**. Over two years, the data pipeline produced **1 440 files** (720 days × 2 versions each):

- `YYYY-MM-DD_raw-data.txt` — unprocessed sensor readings
- `YYYY-MM-DD_post-processed.txt` — cleaned, analysis-ready data

All files currently sit in `data/exercises/meteorological/incoming/`. Your task: **move only the post-processed files** into `data/exercises/meteorological/post-processed/`, leaving the raw files in place.

### File format

Each file has one header row and one data row with 10 meteorological inputs:

```
station_id date temp_c humidity_pct wind_ms precip_mm pressure_hPa solar_wm2 dewpoint_c visibility_km cloud_cover_pct
FF-MET-042 2024-06-15 12.1 67.5 3.0 0.0 1013.0 418.0 6.5 12.5 42
```

**Solution:**

```bash
cd data/exercises/meteorological/incoming

# Move them
mv *_post-processed.txt ../post-processed/
```

## More `bash` commands

### `touch` — Create an empty file

Creates a new empty file, *like choosing **New file** in a file explorer.*

```bash
touch notes.txt
```

---

### `rm` — Remove

Deletes files and directories. *In a file explorer this is Delete — but there is no trash bin; deleted files are gone.*

```bash
rm old_plot.txt                  # delete one file
rm *_raw-data.txt                # delete all matching files (uses *)
rm -r temp_folder/               # -r = recursive (needed for directories)
```

> Be careful with `rm`: double-check the path before pressing Enter. A typo like `rm -r data/` can delete an entire dataset folder.

---

### `find` — Find files

Locates files by name or properties, *like the search bar in a file explorer*.

```bash
find . -name "README.txt"
```

---

### `grep` — Global Regular Expression Print

Searches for text inside files, *like Ctrl+F across many files at once*.

```bash
# lines containing NODATA
grep "NODATA" station_FF-MET-042_2024-Q1.txt
```

---

### `sed` — Stream Editor

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

### `cat` — Concatenate and display

Prints a file to the terminal.

```bash
cat station_FF-MET-042_2024-Q1.txt
cat file1.txt > file2.txt              # move content from file1 to file2
cat file1.txt file2.txt > combined.txt # merge files
```

---

### `head` / `tail` — First / last lines

```bash
head -5 data.csv          # first 5 lines
tail -20 log.txt          # last 20 lines
```

---

### `wc` — Word Count

```bash
wc -l *.txt               # line count for each file
```
---

### `clear` — Clear the terminal screen

```bash
clear
```

---

#### `man` — Manual

```bash
man grep                  # full documentation for grep
```

---

### `|` — Pipe

Chains commands together so the output of the left command feeds into the right one.

```bash
# Count how many post-processed files exist
ls *_post-processed.txt | wc -l
```

## Flags

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

## Exercise 3 — Find and replace missing values with `grep` and `sed`

The quarterly export `station_FF-MET-042_2024-Q1.txt` (in `data/exercises/nodata-replace/`) contains hourly records from station **FF-MET-042**. Some sensor readings failed and were stored as the string `NODATA`. Before analysis, every `NODATA` must be replaced with the numeric missing-value code `-9999`.

This exercise uses the flags from the section above.

**Solution:**

### Step 1 — Explore the file with `grep`

```bash
cd data/exercises/nodata-replace

# How many lines contain NODATA? (-c = count)
grep -c "NODATA" station_FF-MET-042_2024-Q1.txt

# Show them with line numbers (-n)
grep -n "NODATA" station_FF-MET-042_2024-Q1.txt
```

### Step 2 — Replace with `sed`

Use `sed` as shown above. The `g` flag replaces every `NODATA` on a line, not just the first one.

```bash
# Preview the replacement (prints to terminal, does NOT modify the file)
sed 's/NODATA/-9999/g' station_FF-MET-042_2024-Q1.txt | head -5

# Write the cleaned file (keep the original!)
sed 's/NODATA/-9999/g' station_FF-MET-042_2024-Q1.txt > station_FF-MET-042_2024-Q1_clean.txt

# Confirm no NODATA remains (-c should print 0)
grep -c "NODATA" station_FF-MET-042_2024-Q1_clean.txt

# Count how many -9999 values were inserted (-o prints each match)
grep -o "\-9999" station_FF-MET-042_2024-Q1_clean.txt | wc -l
```

### Step 3 — Combine commands with a pipe

```bash
# Show only the lines that originally had NODATA, already cleaned
grep "NODATA" station_FF-MET-042_2024-Q1.txt | sed 's/NODATA/-9999/g'
```
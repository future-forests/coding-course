# FuFo Coding Course

Coding course course dedicated to data analysis and the use of Python and LLMs, designed for students in [Future Forests](https://uni-freiburg.de/futureforests/).

## Course overview

| Class | Date  | Material                                                     | Topics |
| ----- | ----- | ------------------------------------------------------------ | -------|
| 1     | 24/09 | `01-bash-basics.md` | Terminal navigation, file operations, `grep`, `sed`, `find` |
| 2     | 24/09 | `02-git-and-collaboration.md` | Git basics, branching, merge conflicts, GitLab workflow     |
| 3a    | 24/09 | `03a-python-basics.ipynb`  | ? |

## Requirements

### 1. System tools (install once)

| Tool        | Windows                             | 
| ----------- | ----------------------------------- | 
| **Git**     | https://git-scm.com/install/windows |
| **VS Code** | https://code.visualstudio.com       |


VS Code extensions (`CTRL+MAJ+X`):

- **Remote - SSH** (Microsoft)
- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **Pixi Code** (renan-r-santos)
- (Optional) **Rainbow CSV** (mechatroner)

### 2. Remote server (HPC) access

This is optional, but I strongly recommend using a remote server (or HPC for High-Performance Computing) during the course. We will use **UC3**, a powerful remote computer available to every students in Baden-Württemberg, where you can store your data (500GB free!) and run computationally intensive analyses from your laptop. You can access it remotely, so your calculations can continue running even when your laptop is turned off.

Before the start of the course (at least one week in advance), please register and create your bwUniCluster account by following steps A, B, and C on the [bwUniCluster registration page](https://wiki.bwhpc.de/e/Registration/bwUniCluster).

### 3. Python environment (Pixi)

**Recommended timing:** Please complete this part between Class 2 and Class 3.

Pixi is a cross-platform environment manager (similar idea to conda, but open-source and simpler for projects). All Python dependencies for this course are defined in `[pixi.toml](pixi.toml)` at the repo root.

1. Clone the repository (if you missed Class 2)

Open a **Bash terminal** (Terminal on macOS/Linux, or **Git Bash** on Windows) and run:

```bash
git clone git@gitlab.kit.edu:fufo/fufo_coding_course.git
cd fufo_coding_course
```

2. Install [Pixi](https://pixi.sh)

```bash
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.bashrc   # or restart the terminal
```

3. Create the Python environment

From the repository root:

```bash
pixi install
pixi run code .
```

This reads `pixi.toml` and installs the course packages into a local `.pixi/` environment.

4. Open the class notebook of the day (e.g. `03a-python-basics.ipynb`) in VS Code

```sh
code 03a-python-basics.ipynb
```

Top right click on "Select Kernel" -> "Python Environment" -> select **Python 3.13.15** or type "pixi" -> Enter

## Course exercise data

During the first class, we will download the data we will use throughout the course together. If you were unable to attend the first class, here is what you need to do.

### 1. If you have access to uc3

**From uc3 (Class 1):** copy shared course data to your machine.

```bash
mkdir -p data
scp -r YOUR_USERNAME@uc3.scc.kit.edu:/path/to/fufo_coding_course/exercises/ data/
```

Replace `YOUR_USERNAME` with your bwUniCluster username (e.g. `fr_ab1234`). You need to be on the **Uni-Freiburg network or VPN** for uc3.

### 2. If you don't have access to uc3

TODO
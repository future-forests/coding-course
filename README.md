# FuFo Coding Course

Coding course dedicated to data analysis and the use of Python and LLMs, designed for students in [Future Forests](https://uni-freiburg.de/futureforests/).

## 1. Course overview and calendar

| Class | Topics | Date | Drop-in clinic date |
| ----- | ------ | ---- | ------------------- |
| 1  | Introduction, VS code, terminal navigation (bash), remote cluster | 24/09 09:30–10:30 | 28/09 14:00-16:00|
| 2  | Version control (git) and collaboration (GitLab) | 01/10 09:30–10:30 | 02/10 14:00-16:00 |
| 3a | Python basics: variables, types, built-in functions, packages | 05/10 **08:30–09:30** | 07/10 14:00-16:00 |
| 3b | Python Basics: NumPy arrays, loops, conditions | 08/10 09:30–10:30 | 09/10 14:00-16:00 |
| 4  | Tabular data: vectorisation, table operations (pandas), matplotlib | 12/10 09:30–10:30 | 21/10 14:00-16:00 |
| 5  | Geospatial data: netCDF, raster operations (xarray) | 22/10 09:30–10:30 | 26/10 14:00-16:00 |
| 6  | Advanced Python: user functions, profiling, publishing code with a DOI | 29/10 09:30–10:30 | 02/11 14:00-16:00 |
| 7  | Using LLMs in coding: modes, prompting, reviewing | 05/11 09:30–10:30 | 09/11 14:00-16:00 |
| 8  | Critical thinking about LLMs: limits and bias | 12/11 09:30–10:30 | - |

How to subscribe to the automatic calendar (recommended to refresh every day):

- **Thunderbird:** Calendar tab → right-click in the calendar list → **New Calendar…** → **On the Network** → **iCalendar (ICS)** → paste the link below
- **Outlook:** Add calendar → Subscribe from web → paste the link below
- **Apple Calendar:** File → New Calendar Subscription → paste the link below
- **Google Calendar:** Settings → Add calendar → From URL → paste the link below

**Calendar feed URL:** `https://gitlab.uni-freiburg.de/future-forests/ses_model_lab/fufo-coding-course/-/raw/main/fufo-coding-course.ics`

## 2. Five requirements

### i. System tools (install once)

| Tool        | Windows                                  | 
| ----------- | ---------------------------------------- | 
| **Git**     | https://git-scm.com/install/windows      |
| **VS Code** | https://code.visualstudio.com            |
| **Python**  | https://www.python.org/downloads/windows |


VS Code extensions (`CTRL+MAJ+X`):

- **Remote - SSH** (Microsoft)
- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **DataFrame Viewer** (ChristofKaufmann)
- (Optional) **Pixi Code** (renan-r-santos) — helpful on your laptop; not required on UC3
- (Optional) **Rainbow CSV** (mechatroner)

---

### ii. Remote server (HPC) access (Optional)

This is optional, but I strongly recommend using a remote server (or HPC for High-Performance Computing) during the course. We will use **UC3**, a powerful remote computer available to every students in Baden-Württemberg, where you can store your data (500GB free!) and run computationally intensive analyses from your laptop. You can access it remotely, so your calculations can continue running even when your laptop is turned off.

Before the start of the course (at least one week in advance), please register and create your bwUniCluster account by following steps A, B, and C on the [bwUniCluster registration page](https://wiki.bwhpc.de/e/Registration/bwUniCluster).

---

### iii. Register to Gitlab/Codeberg TODO

---

### iv. Python environment (Pixi)

**Recommended timing:** between Class 2 and Class 3. Dependencies are in [`pixi.toml`](pixi.toml).

Run once (on **UC3** or your **laptop**):

```bash
git clone git@gitlab.kit.edu:fufo/fufo_coding_course.git
cd fufo_coding_course
curl -fsSL https://pixi.sh/install.sh | bash && source ~/.bashrc
pixi install
pixi run install-kernel
```

**UC3 (VS Code Remote SSH):** `export PATH="$HOME/.pixi/bin:$PATH"`, reconnect. In a notebook: **Select Kernel → Jupyter Kernel → Python (fufo course)**.

**Laptop:** `pixi run code .` from the repo root, open a notebook, same kernel.

---

### v. GitHub Education registration (Optional)

This is optional and only needed for Classes 7 and 8, where we use **GitHub Copilot Pro** in VS Code.

Apply as a **teacher** (faculty or researcher), 🚨 **not as a student** 🚨, to [GitHub Education](https://education.github.com). Verified teachers get free Copilot Pro.

Open your [GitHub Education benefits](https://github.com/settings/education/benefits) page and click **Start an application**. Follow [Apply to GitHub Education as a teacher](https://docs.github.com/en/education/about-github-education/github-education-for-teachers/apply-to-github-education-as-a-teacher) if you need the full steps.

---

### vi. Course exercise data (if you miss class 1)

During the first class, we will download the data we will use throughout the course together. If you were unable to attend the first class, here is what you need to do.

#### a. If you have access to uc3

**From uc3 (Class 1):** copy shared course data to your machine.

```bash
mkdir -p data
scp -r YOUR_USERNAME@uc3.scc.kit.edu:/path/to/fufo_coding_course/exercises/ data/
```

Replace `YOUR_USERNAME` with your bwUniCluster username (e.g. `fr_ab1234`). You need to be on the **Uni-Freiburg network or VPN** for uc3.

#### b. If you don't have access to uc3

TODO
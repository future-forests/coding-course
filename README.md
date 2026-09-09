# Future Forests Coding Course

Coding course dedicated to data analysis and the use of Python and LLMs, designed for students in [Future Forests](https://uni-freiburg.de/futureforests/).

## 1. Course overview and calendar

| Class | Topics | Date | Drop-in clinic date |
| ----- | ------ | ---- | ------------------- |
| 1  | Introduction, VS code, terminal navigation (bash), remote cluster | 24/09 09:30–10:30 | 28/09 14:00-16:00|
| 2  | Version control (git) and collaboration (GitHub) | 01/10 09:30–10:30 | 02/10 14:00-16:00 |
| 3a | Python basics: variables, types, built-in functions, packages | 05/10 **08:30–09:30** | 07/10 14:00-16:00 |
| 3b | Python Basics: NumPy arrays, loops, conditions | 08/10 09:30–10:30 | 09/10 14:00-16:00 |
| 4  | Tabular data: vectorisation, table operations (pandas), matplotlib | 12/10 09:30–10:30 | 21/10 14:00-16:00 |
| 5  | Geospatial data: netCDF, raster operations (xarray) | 22/10 09:30–10:30 | 26/10 15:00-17:00 |
| 6  | Advanced Python: user functions, profiling, publishing code with a DOI | 29/10 09:30–10:30 | 02/11 14:00-16:00 |
| 7  | Using LLMs in coding: modes, prompting, reviewing | 05/11 09:30–10:30 | 09/11 14:00-16:00 |
| 8  | Critical thinking about LLMs: limits and bias | 12/11 09:30–10:30 | - |

How to subscribe to the automatic calendar (if asked, refresh every day):

- **Thunderbird:** Calendar tab → right-click in the calendar list → **New Calendar…** → **On the Network** → paste the link below on "Location" and check "This location doesn't require credentials"
- **Outlook:** Add calendar → Subscribe from web → paste the link below
- **Apple Calendar:** File → New Calendar Subscription → paste the link below
- **Google Calendar:** Settings → Add calendar → From URL → paste the link below

**Calendar feed URL:** `https://raw.githubusercontent.com/future-forests/ses-model-lab-webpage/refs/heads/main/model_lab_calendar.ics`

## 2. Five requirements

### i. System tools (install once)

| Tool        | Windows                                  | 
| ----------- | ---------------------------------------- | 
| **Git**     | https://git-scm.com/install/windows      |
| **VS Code** | https://code.visualstudio.com            |
| **Python**  | https://www.python.org/downloads/windows |


Start VS Code (as admin) and install these VS Code extensions (`CTRL+MAJ+X`):

- **Remote - SSH** (Microsoft)
- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **DataFrame Viewer** (ChristofKaufmann)
- (Optional) **Pixi Code** (renan-r-santos) — helpful on your laptop; not required on UC3
- (Optional) **Rainbow CSV** (mechatroner)

---

### ii. Register to GitHub (and create an SSH key)

1. Create a free account at [github.com](https://github.com) **and send me your username**.
2. Start VS Code (as admin) and open a terminal: `CTRL+J` (or **View → Terminal**).
3. Clone, pull, and push from the terminal requires authentication. **Use an SSH key** (you will reuse it for UC3 in the next step):
   - `ssh-keygen -t ed25519 -C "FF-laptop"` → Enter for the default path → set a passphrase
   - Copy the public key: `cat ~/.ssh/id_ed25519.pub`
   - On GitHub: **Settings → SSH and GPG keys → New SSH key** → paste the public key

---

### iii. Remote server (HPC) access (optional)

This is optional, but I strongly recommend using a remote server (or HPC for High-Performance Computing) during the course. We will use **UC3**, a powerful remote computer available to every students in Baden-Württemberg, where you can store your data (500GB free!) and run computationally intensive analyses from your laptop. You can access it remotely, so your calculations can continue running even when your laptop is turned off.

Before the start of the course (at least one week in advance), please register and create your bwUniCluster account by following steps A, B, and C on the [bwUniCluster registration page](https://wiki.bwhpc.de/e/Registration/bwUniCluster).

Then open VS Code (as admin) to set-up Remote SSH:

1. Register the **same public key** at [login.bwidm.de](https://login.bwidm.de): **Index → My SSH Pubkeys → Add SSH Key** (name: `FF-laptop`, key: paste from clipboard at step ii.)
2. Command Palette (`CTRL+SHIFT+P`) → **Open SSH Configuration File** → add (replace `fr_ab1234` with your username):

```
Host uc3
    HostName     uc3.scc.kit.edu
    User         fr_ab1234
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

3. Save, restart VS Code. To connect daily: Command Palette (`CTRL+SHIFT+P`) → **Connect to Host → uc3** → enter OTP + passphrase (once per day).

---

### iv. Python environment (Pixi)

**Recommended timing:** between Classes 2 and Class 3. Dependencies are in [`pixi.toml`](pixi.toml).

Run once (on **UC3** or your **laptop**):

```bash
git clone git@github.com:future-forests/coding-course.git
cd coding-course
curl -fsSL https://pixi.sh/install.sh | bash && source ~/.bashrc
pixi install
pixi run install-kernel
```

**UC3 (VS Code Remote SSH):** `export PATH="$HOME/.pixi/bin:$PATH"`, reconnect. In a notebook: **Select Kernel → Jupyter Kernel → Python (Future Forests course)**.

**Laptop:** `pixi run code .` from the repo root, open a notebook, same kernel.

---

### v. GitHub Education registration (optional)

Only for Classes 7 and 8, where we use **GitHub Copilot Pro** in VS Code.

Apply as a **teacher** (faculty or researcher), 🚨 **not as a student** 🚨, to [GitHub Education](https://education.github.com). Verified teachers get free Copilot Pro.

Open your [GitHub Education benefits](https://github.com/settings/education/benefits) page and click **Start an application**. Follow [Apply to GitHub Education as a teacher](https://docs.github.com/en/education/about-github-education/github-education-for-teachers/apply-to-github-education-as-a-teacher) if you need the full steps.

---

### Course exercise data (if you miss class 1)

During the first class, we will download the data we will use throughout the course together. If you were unable to attend the first class, here is what you need to do.

#### a. If you have access to uc3

**From uc3 (Class 1):** copy shared course data to your machine.

```bash
mkdir -p processed_data
scp -r YOUR_USERNAME@uc3.scc.kit.edu:/path/to/coding-course/exercises/ processed_data/
```

Replace `YOUR_USERNAME` with your bwUniCluster username (e.g. `fr_ab1234`). You need to be on the **Uni-Freiburg network or VPN** for uc3.

#### b. If you don't have access to uc3

Copy the folder `processed_data` from our shared drive, to your working directly:

```
un042rd01/01_General/02_Central_infrastructure/SES_ModelLab/coding-course/
```
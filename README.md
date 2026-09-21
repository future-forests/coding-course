# Future Forests Coding Course

Coding course dedicated to data analysis and the use of Python and LLMs, designed for students in [Future Forests](https://uni-freiburg.de/futureforests/).

## 1. Course overview and calendar

### Autumn course

| Class | Topics | Date | Drop-in clinic date |
| ----- | ------ | ---- | ------------------- |
| 1  | Introduction, VS Code, terminal navigation (bash), remote cluster | 24/09 09:30–10:30 | 28/09 14:00-16:00|
| 2  | Version control (git) and collaboration (GitHub) | 01/10 09:30–10:30 | 02/10 14:00-16:00 |
| 3a | Python basics: variables, packages, NumPy arrays | 05/10 **08:30–09:30** | 07/10 14:00-16:00 |
| 3b | Python basics: loops, conditions, vectorisation | 08/10 09:30–10:30 | 09/10 14:00-16:00 |
| 4  | Tabular data: table operations (pandas), plotting (matplotlib) | 12/10 09:30–10:30 | 21/10 14:00-16:00 |
| 5a  | Geospatial data: netCDF, raster operations (xarray) | 22/10 09:30–10:30 | 26/10 15:00-17:00 |
| 5b  | Survey data: survey analysis (scikit-learn) | 22/10 13:30–14:30 | 26/10 15:00-17:00 |
| 6  | Advanced Python: user functions, profiling, publishing code with a DOI | 29/10 09:30–10:30 | 02/11 14:00-16:00 |
| 7  | Using LLMs in coding: modes, prompting, reviewing | 05/11 09:30–10:30 | 09/11 14:00-16:00 |
| 8  | Critical thinking about LLMs: limits and bias | 12/11 09:30–10:30 | - |

### How to subscribe to the automatic calendar (if asked, refresh every day):

- **Thunderbird:** Calendar tab → right-click in the calendar list → **New Calendar…** → **On the Network** → paste the link below on "Location" and check "This location doesn't require credentials"
- **Outlook:** Add calendar → Subscribe from web → paste the link below
- **Apple Calendar:** File → New Calendar Subscription → paste the link below
- **Google Calendar:** Settings → Add calendar → From URL → paste the link below

**Calendar feed URL:** `https://raw.githubusercontent.com/future-forests/ses-model-lab-webpage/refs/heads/main/model_lab_calendar.ics`

### Planning

| When | What |
| ---- | ---- |
| Day before class | Class notebook published |
| Class (60 min + 20 min optional) | Assistant-guided exercises |
| Drop-in clinic (2 h) | Q&A and clarification |
| Day after clinic | Solutions published |

## 2. Six requirements

### i. System tools (install once)

| Tool        | Windows                                  | 
| ----------- | ---------------------------------------- | 
| **Git**     | https://git-scm.com/install/windows      |
| **VS Code** | https://code.visualstudio.com            |
| **Python**  | https://www.python.org/downloads/windows |


Start VS Code and install these VS Code extensions (`CTRL+SHIFT+X`):

- **Remote - SSH** (Microsoft)
- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **Pixi Code** (renan-r-santos) — mandatory on your laptop; not required on UC3
- **DataFrame Viewer** (ChristofKaufmann)
- (Optional) **Rainbow CSV** (mechatroner)

---

### ii. Register on GitHub (and create an SSH key)

1. Create a free account at [github.com](https://github.com) **and send me your GitHub username on Element!**
2. Start VS Code and open a terminal: `CTRL+J` (or **View → Terminal**)
3. Cloning, pulling, and pushing from the terminal require authentication. **Use an SSH key** (you will reuse it for UC3 in the next step):
   - Type in the terminal `ssh-keygen -t ed25519 -C "FF-laptop"` → Press Enter for the default path → set a passphrase
   - Type `cat ~/.ssh/id_ed25519.pub` and copy the public key (e.g. `ssh-ed25519 AEEEDSC3NzaC1lZDI1NTE5AAAAIzU4dokRTfksQ0ytDQ+C/V8hWTNxFz8/s8Vb6Ouag2I ff-laptop`)
   - On GitHub: **Settings → SSH and GPG keys → New SSH key** → paste the public key

---

### iii. Remote server (HPC) access (optional)

This is optional, but I strongly recommend using a remote server (or HPC for High-Performance Computing) during the course. We will use **UC3**, a powerful remote computer available to every student in Baden-Württemberg, where you can store your data (500GB free!) and run computationally intensive analyses from your laptop. You can access it remotely, so your calculations can continue running even when your laptop is turned off.

If you think you will never need it for your research, you can certainly do without it.

Before the start of the course (at least one week in advance), please register and create your bwUniCluster account by following steps A, B, and C on the [bwUniCluster registration page](https://wiki.bwhpc.de/e/Registration/bwUniCluster).

When you are done, **please send me your UC3 username on Element (e.g. fr_ab1234)!**

Then open VS Code to set up Remote SSH:

1. Register the **same public key** at [login.bwidm.de](https://login.bwidm.de): **Index or übersicht (top-right) → My SSH Pubkeys → Add SSH Key** (name: `FF-laptop`, key: paste from clipboard at step ii.)
2. Command Palette (`CTRL+SHIFT+P`) → **Open SSH Configuration File** → add the following:

(replace `fr_ab1234` with your bwidm username (it's `fr_` + Uni Freiburg username); replace `USER` with your Windows username: in Git Bash, run `echo $USERNAME`)

```
Host uc3
    HostName     uc3.scc.kit.edu
    User         fr_ab1234
    IdentityFile C:\Users\USER\.ssh\id_ed25519
    IdentitiesOnly yes
```

3. Open **File → Preferences → Settings** (`CTRL+,`) and:
   - Search for **Remote SSH: Show Login Terminal** → check it
   - Search for **Remote SSH: Use Local Server** → uncheck it (required so OTP prompts appear in the terminal instead of Output)
4. **Windows only:** open a terminal and paste the code below (to fix permission issues):
```powershell
$ssh = "$env:USERPROFILE\.ssh"
$me  = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
function Fix-SshAcl($path) {
    icacls $path /inheritance:r
    icacls $path /grant:r "${me}:(OI)(CI)F"
    icacls $path /grant:r "NT AUTHORITY\SYSTEM:(OI)(CI)F"
}
function Fix-SshFileAcl($path) {
    icacls $path /inheritance:r
    icacls $path /grant:r "${me}:R"
    icacls $path /grant:r "NT AUTHORITY\SYSTEM:R"
}
Fix-SshAcl $ssh
if (Test-Path "$ssh\config")     { Fix-SshFileAcl "$ssh\config" }
if (Test-Path "$ssh\id_ed25519") { Fix-SshFileAcl "$ssh\id_ed25519" }
```
Save, restart VS Code.

5. To connect daily: Command Palette (`CTRL+SHIFT+P`) → **Connect to Host → uc3** → select Linux → enter OTP + passphrase in the **terminal** (once per day).
6. **Create a separate SSH key on UC3 for GitHub** (your laptop key from step ii. only works on your laptop — you need a second key to `git clone` from UC3):
   - Connect to UC3 in VS Code, open a terminal (`CTRL+J` → **`+`**), and type `ssh-keygen -t ed25519 -C "uc3"` (press "Enter" key, then enter a passphrase two times), then type `cat ~/.ssh/id_ed25519.pub` and copy the result to your clipboard
   - On GitHub: **Settings → SSH and GPG keys → New SSH key → paste the public key**

---

### iv. Pull course materials

Wait until I've added you to our GitHub organization before doing this one.

> **Windows users (no UC3):** VS Code opens **PowerShell** by default. Before running any terminal command in this course, switch to **Git Bash**: click the **`˅`** next to **`+`** in the terminal tab bar → **Select Default Profile** → **Git Bash**, then open a new terminal (`CTRL+J`)

Type (on **UC3** or your **laptop**, on Windows use **Git Bash** as terminal):

```bash
git clone git@github.com:future-forests/coding-course.git
cd coding-course
```

---

### v. Set up Python environment (Pixi)

**Recommended timing:** between Classes 2 and Class 3

Type in the root folder `coding-course` (on **UC3** or your **laptop**):

```bash
curl -fsSL https://pixi.sh/install.sh | bash && source ~/.bashrc
pixi install
pixi run install-kernel
```

**UC3 (VS Code Remote SSH):** Type in the terminal `export PATH="$HOME/.pixi/bin:$PATH"`

---

### vi. GitHub Education registration (optional)

Only for Classes 7 and 8, where we use **GitHub Copilot Pro** in VS Code.

Apply as a **teacher** (faculty or researcher), 🚨 **not as a student** 🚨, to [GitHub Education](https://education.github.com). Verified teachers get free Copilot Pro.

Open your [GitHub Education benefits](https://github.com/settings/education/benefits) page and click **Start an application**. Follow [Apply to GitHub Education as a teacher](https://docs.github.com/en/education/about-github-education/github-education-for-teachers/apply-to-github-education-as-a-teacher) if you need the full steps.

## 3. Open and use a notebook (from Class 3)

- Reload VS Code: open Palette (`CTRL+SHIFT+P`) → Reload Window
- Type in the terminal `code notebooks/03a-python-basics.ipynb`
- Top-left of the notebook: **Select Kernel → Jupyter Kernel → Python (Future Forests course)**

## 4. Course exercise data (if you miss Class 1)

During the first class, we will download the data we will use throughout the course together. If you were unable to attend the first class, here is what you need to do.

### a. If you have access to UC3

**From UC3 (Class 1):** copy shared course data to your machine.

```bash
cd processed_data/ # if fails, try to find it
scp -r YOUR_USERNAME@uc3.scc.kit.edu:/pfs/work9/workspace/scratch/fr_ad1149-coding-course/processed_data/ .
```

Replace `YOUR_USERNAME` with your bwUniCluster username (e.g. `fr_ab1234`). You need to be on the **Uni-Freiburg network or VPN** for UC3.

### b. If you don't have access to UC3

Copy the contents of the `processed_data` folder from our shared drive to your working directory:

```
un042rd01/01_General/02_Central_infrastructure/SES_ModelLab/coding-course/processed_data
```

## 5. Using an LLM before Class 7

When you get stuck on an exercise, we recommend **not** using an LLM (e.g. ChatGPT, Claude, Gemini). Instead, look for help online on forums such as [Stack Overflow](https://stackoverflow.com) or Reddit, or in the official documentation of the packages you use. We will cover LLMs properly in Classes 7 and 8, don't worry.

If you still want to use an LLM (GitHub Copilot, Cursor, ChatGPT, etc.), do not use it to generate solutions. Before **every** new chat, add the instructions from [`LLM_PROMPT.md`](LLM_PROMPT.md) — paste its contents at the start of the conversation, or reference the file with `@LLM_PROMPT.md` in Cursor or VS Code. The model should act as a tutor: point you to documentation and give small hints only, never code that completes the exercise.

When you ask for help, say what you tried, paste any error message, and name the concept you are unsure about.

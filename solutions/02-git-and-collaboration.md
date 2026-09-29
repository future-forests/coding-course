## Quick reference card

| Command | What it does |
| ------- | ----------------------------------- |
| `git init` | Initialize repository, start a new project |
| `git status` | Show repository status, or "What changed since my last save?" |
| `git add` | Add to staging area, choose which changes go into the next snapshot |
| `git commit` | Record a snapshot, save a named checkpoint you can return to |
| `git log` | Show commit history, scroll through previous versions |
| `git diff` | Show differences, see exactly what changed line by line |
| `git branch` | List or create branches |
| `git checkout (-b)` | Move to (and create) branch |
| `git merge` | Combine branches, fold your draft back into the main version |
| `git rm` | Remove and track deletion, delete a file and record that deletion |
| `git clone` | Copy a remote repository, download a GitHub project |
| `git pull` | Fetch and merge remote changes, get your colleagues' latest work |
| `git push` | Upload local commits, share your checkpoints with the team |

# Class 2 — Version Control and Collaboration (Git Basics + GitHub)

You will probably be involved in research projects that can last months or year. As your research develops, you will write and modify analysis scripts, process new data, test different approaches, and collaborate with others who may need to reproduce, review, or build on your work. Sooner or later you need to answer:

- *Which version of the code produced this figure?*
- *What exactly changed since last week?*
- *Can I try a new analysis without breaking what already works?*

That is what **version control** is for: a system that **tracks every change** to your project over time, lets you **go back**, **compare** versions, and **work in parallel** without overwriting what is stable.

**Git** is the tool we use to do version control. Instead of saving `protocol_v2_final.docx`, version control keeps **one file** with a full history of documented **snapshots** (*commit*). Git is the program that stores and organizes those snapshots on your machine.

## 1. How Git implements version control

Git splits your work into three areas on your machine:

- **Working directory** — the files you edit (like any normal folder)
- **Staging area** — the file changes you marked as ready for the next snapshot
- **Repository** — everything Git has saved so far, files and their changes, stored in the hidden `.git` folder

## 2. Let's start with our first `git` commands

> UC3 is using a old version of git, do `git config --global init.defaultBranch main`

### i. `git init` — Initialize repository

Creates a new Git repository in the current directory. Git can now track changes here.

```bash
# Create a dir
mkdir stations_bw
# Move to the dir
cd stations_bw
# Add a file
touch protocol_staufen.md
git init
```

Before your first commit, tell Git **who you are** (only once):

```bash
git config --global user.email "your.name@futureforests.uni-freiburg.de"
```

---

### ii. `git status` — Check what is happening

Shows which files are new, modified, staged, or untracked.

```bash
git status
```

Example output when you created a file but haven't saved it in Git yet:

```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        protocol_staufen.md

nothing added to commit but untracked files present
```

> **Run this often**, especially before and after `git add` and `git commit` to understand what you are doing. Git print and error messages are usually very useful.

---

### iii. `git add` — Stage changes

Marks files (or changes) to include in the **next commit**.

```bash
git add protocol_staufen.md
```

---

### iv. `git commit` — Save a snapshot

Records the staged changes as a permanent snapshot in the repository history.

```bash
git commit -m "Add Staufen protocol file"
```

> The flag `-m` is to leave a message, a short description of *why* you saved this commit. **This is a very important part of a commit**. To write a good commit message, put yourself in the shoes of a colleague who will need to understand what you did in this commit in a single sentence.

---

### v. `git rm` — Remove files (Git-aware)

Deletes a file **and** records the deletion in Git (so the removal is part of history).

```bash
git rm old_protocol_draft.md
```

> If you delete a file manually (e.g. in the file explorer), Git still sees it as "deleted" — you then stage that with `git add old_protocol_draft.md` or `git add .`.

---

### vi. `git log` — View history

Lists previous commits, newest first.

```bash
git log --oneline
```

## 3. Typical workflow (local)

When you work alone on your machine, the cycle is:

```
edit files  →  git add  →  git commit -m "describe your commit"
```

... and don't forget to use `git status` between each action to understand what you are doing.

## Exercise A - Track a field protocol

Your group maintains a sampling protocol for station **FF-MET-042**. Set up a Git repository and save the starter protocol below in `protocol_staufen.md` as your first commit. Then add the rain-event rule (`Rain event: do not sample if it is raining`) in a second commit, and use `git log` to see how Git recorded each change.

Starter content:

```md
# FF-MET-042 sampling protocol

- Wind conditions: do not sample if wind > 12 m/s
- Sensor check: record battery level before each visit
```

**Solution:**

```bash
mkdir stations_bw
cd stations_bw
git init

touch protocol_staufen.md

# Add starter content

git status
git add protocol_staufen.md
git commit -m "Initial protocol"

# Add rain-event rule

git add protocol_staufen.md
git commit -m "Add rain-event rule"

git log --oneline
```

## 4. Branching - work in parallel without breaking `main`

Until now, everything happened on one line of history (our **`main`** branch). Branches let you create a **parallel copy of the project** to experiment, then merge back when ready.

Why do we need branches? They let you work on a draft **without changing what is stable, what everyone else relies on**.

**Situation example:**

- `main` *(A)* holds the approved field protocol the whole group follows
- You want to draft winter sampling rules, you create branch `winter`, experiment there. You branch off the approved protocol to start your draft *(B)*.
- A colleague fixes a unit error on `main`, `main` moves forward without you *(C)*
- You want to catch up with `main` before merging. You merge `main` with your branch *(D)*
- Your winter rules join the approved protocol, you merge your branch with `main` *(E)*

```
main:      A ────────────── C ─────────────── E
            \                       \        /
winter:      B ───────────────────── D ──────
```

Result: at *(E)*, **`main`** combines both lines of work — the colleague's fix and your winter rules, into one shared history.

---

### i. `git branch` — List branches

```bash
git branch              # list local branches (* = current)
```

---

### ii. `git checkout` — Create and move to branch

Creates and moves you to another branch, or just move you to an existing one.

```bash
git checkout -b winter    # create branch and switch (-b = branch)
git checkout winter       # move to existing branch
```

---

### iii. `git merge` — Combine branches

Brings commits from another branch into your **current** branch.

```bash
git checkout main
git merge winter
```

If the merge succeeds, Git creates a merge commit. However, you may encounter a merge conflict when the same lines have been edited differently in the two branches. You then need to **resolve the merge conflict** before completing the merge (we will look into that later).

## Exercise B — Branching: add a new feature to your repo

The approved protocol on **`main`** is what everyone follows in the field. You want to add new **winter sampling rules** with the following rule:

```md
- Frost: do not touch metal masts with bare hands when air temperature < 0 °C
```

Using the repo from Exercise A, add a frost safety rule on branch `winter`. Then merge it into `main`.

**Solution:**

```bash
cd stations_bw

git checkout -b winter

# Add frost rule 

git add protocol_staufen.md
git commit -m "Add frost safety rule"

git checkout main
git merge winter

git log --oneline
```

## Exercise C (bonus)

You start drafting the **ice** rule on branch **`winter-log`**, then switch priorities: the **wind** limit should be updated on **`main`** first.

On branch **`winter-log`**, add:

```md
- Ice: record ice thickness on soil pins when air temperature < 0 °C
```

On branch **`wind-limit`**, replace the existing wind line with:

```md
- Wind conditions: do not sample if wind > 10 m/s
```

### ii. What to do

1. Move to your `stations_bw` repo and check out **`main`**
2. Create branch **`winter-log`** and switch to it
3. Add the ice rule to `protocol_staufen.md`, stage the file, and commit
4. Switch back to **`main`**
5. Create branch **`wind-limit`** and switch to it
6. Edit the wind line to **10 m/s**, stage, and commit
7. Switch to **`main`** and merge **`wind-limit`**
8. Switch to **`winter-log`** and merge **`main`** so your ice draft includes the new wind limit
9. Switch to **`main`** and merge **`winter-log`**

**Solution:**

```bash
cd stations_bw

git checkout main
git checkout -b winter-log

# Add ice thickness line to protocol_staufen.md

git add protocol_staufen.md
git commit -m "Add ice thickness logging rule"

# Priority change: wind limit goes to main first
git checkout main
git checkout -b wind-limit

# Change wind line to 10 m/s in protocol_staufen.md

git add protocol_staufen.md
git commit -m "Tighten wind sampling limit to 10 m/s"

git checkout main
git merge wind-limit

# winter-log was started earlier — update it before merging back
git checkout winter-log
git merge main

git checkout main
git merge winter-log
```

# Part 2 — GitHub and Git collaboration 

Part 1 was about saving history on **your** machine. In research groups, the "trunk" of a project usually lives on a **remote** server where we can collaborate. At Future Forests, we are using **GitHub** (`https://github.com/future-forests/`, feel free to add this to your browser favourites).

GitHub adds an online server and web interface on top of Git: you can browse files, open bug/issue reports, read history, review changes, and discuss code before merging, without emailing zip files.

## 1. Remote repositories on GitHub

### i. `git clone` — Copy a remote repository

Downloads an existing GitHub repository (including full history), or **remote**, to your machine. **Do this once** when you join a project.

```bash
git clone https://github.com/future-forests/coding-course.git
cd coding-course
```

A **remote** is the copy of the repo hosted on GitHub. By convention it is called **`origin`**. To check the origin, you can do:

```bash
git remote -v
# origin  https://github.com/future-forests/coding-course.git (fetch)
# origin  https://github.com/future-forests/coding-course.git (push)
```

---

### ii. `git pull` — Get changes from GitHub

Downloads commits from the remote **and merges them** into your current branch.

```bash
git checkout main
git pull
```

> **Rule of thumb:** `git pull` on `main` **before** you create a new branch to keep your repo updated with the most recent changes.

---

### iii. `git push` — Send commits to GitHub

Uploads your local commits to the remote branch on GitHub.

```bash
git push
```

> **Rule of thumb:** Always do a `git pull` **before** a `git push`.

## 2. Resolve a merge conflict

When a conflict occurs, VS Code (or GitHub) will show the conflicts in the file as follows:

```
<<<<<<< HEAD
- Wind conditions: do not sample if wind > 12 m/s
=======
- Wind conditions: do not sample if wind > 10 m/s
>>>>>>> winter
```

HEAD is your current branch, the bottom block is the branch you're merging in. You can find different options:

- **Accept Current Change:** keep the version from your current branch (`HEAD`) — here, the 12 m/s threshold on `main`
- **Accept Incoming Change:** keep the version from the branch you are merging in — here, the 10 m/s threshold from `winter`
- **Accept Both Changes:** keep both lines one after the other

Repeat for every conflicted file, then `git add` and `commit` in the terminal to finish the merge:

```bash
git add protocol_staufen.md
git commit -m "Resolve merge conflict in wind rule"
```

## Exercise D — Resolve a merge conflict

> This exercise cannot be done outside of the class on Oct. 1

Last January, the Titisee logger **stopped recording for 9 days**: at −15 °C its batteries drained much faster than expected. You are preparing the winter protocol on a branch called `winter-batteries` and add a battery replacement rule to the sensor check line:

```
- Sensor check: record battery level before each visit; replace batteries if below 50%
```

Meanwhile, the **data manager** found that the logger clock had drifted by 8 minutes, so the Titisee data could not be aligned with the DWD weather data. She updates the **same line** on her own branch `clock-check`, already pushed to GitHub:

```
- Sensor check: record battery level and logger clock time before each visit
```

When you bring `clock-check` into your branch, Git flags a **merge conflict**. Here, **nobody is wrong**: the protocol needs **both** changes. Your job is to combine them into a single line.

This mimics what happens in real projects: a colleague works on the same file in parallel, and you need their changes before you can finish yours.

I give you the first steps:

```bash
git clone git@github.com:future-forests/met-protocol.git
cd met-protocol
git checkout -b winter-batteries

# edit protocol_titisee.md: add the battery rule to the sensor line (see above)

git add protocol_titisee.md
git commit -m "Replace batteries below 50% before winter"
```

Now bring the data manager's `clock-check` branch into your branch (how? move to `clock-check` to get a local copy, move back to your branch and merge). Resolve conflicts and commit to combine both changes.

**Solution:**

```bash
git checkout clock-check        # creates a local copy of the branch from GitHub
git checkout winter-batteries
git merge clock-check
# CONFLICT in protocol_titisee.md

# 3 — in VS Code: "Accept Both Changes", then edit the two lines into one:
#   - Sensor check: record battery level and logger clock time before each visit; replace batteries if below 50%
#   Check that no <<<<<<<, ======= or >>>>>>> markers are left in the file

git add protocol_titisee.md
git commit -m "Merge clock-check: combine clock check and battery rule"
```

## 3. The feature branch workflow

A **workflow** is the set of rules a team agrees to follow when collaborating on a project. It turns Git from a personal time machine into a way of working together without overwriting each other.

Most research software teams (like climate modelling groups) follow the **feature branch workflow**. You already practiced the core idea in Exercise B and C. Here are the main rules:

1. `main` stays stable. It is the approved protocol.
2. One branch per task, named for what it does (e.g. `winter` for a new feature, `fix-temp-formula` to solve a bug). One branch per idea. If you're doing two unrelated things, that's two branches.
3. Never commit directly to `main`. Even for a one-line fix.
4. Open a Pull Request (PR) when your change is ready. Be sure to merge main (the last changes that have been made) beforehand. There is where you might have to solve **merge conflicts**. A colleague reads it, comments, approves. You can merge your branch to `main`
5. Your work is now part of main; everyone else picks it up with git pull the next time they start a branch.

You can find an extended version of this workflow on [this online documentation](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

## Exercise E — Update the class protocol on GitHub (Bonus)

The shared repository https://github.com/future-forests/met-protocol contains `protocol_staufen.md` with **20 field rules**. Five of them need to be revised. You are split into **groups of 4**; each group revises **one rule**, and each student in the group changes a **different part** of that rule. Your **printed card** tells you your group, your branch name, the **old rule** and **your new rule**.

Because you all edit the **same line**, only the first Pull Request of your group merges cleanly. The others get a **conflict** on GitHub: keep what is already on `main` **and** add your change.

- Clone the repository, create your branch (name on your card)
- Replace your old rule with your new rule in `protocol_staufen.md`, commit, push
- Open a Pull Request to `main`, add AdrienDams as reviewer
- If GitHub shows a conflict, click **Resolve conflicts** and combine both versions into one line
- Merge yourself

**Solution — group A (rule 1, rain), student 2:**

```bash
git clone git@github.com:future-forests/met-protocol.git
cd met-protocol
git checkout -b rain/wait-30min

# edit protocol_staufen.md, rule 1 (text from your card):
#   1. Rain event: do not sample if it is raining; wait 30 min after the rain stops.
git add protocol_staufen.md
git commit -m "Rain rule: wait 30 min after rain"
git push -u origin rain/wait-30min

# on GitHub: Pull requests → New pull request → rain/wait-30min → main → add reviewer → Create
```

Student 1 (`rain/drizzle`) merged first, so `main` now says *"do not sample during active rain or drizzle"* and GitHub shows **"This branch has conflicts that must be resolved"** on your PR. Click **Resolve conflicts** and replace the marked block with one line:

```
1. Rain event: do not sample during active rain or drizzle; wait 30 min after the rain stops.
```

Check that no `<<<<<<<`, `=======`, `>>>>>>>` markers are left, then **Mark as resolved** → **Commit merge** → **Merge pull request**. (You can also resolve locally as in Exercise D: `git pull` on `main`, `git merge main` on your branch, fix in VS Code, commit, `git push`.)

Students 3 and 4 do the same, each adding their piece to the line. In the end:

```bash
git checkout main
git pull
cat protocol_staufen.md
# 1. Rain event: do not sample during active rain or drizzle; wait 30 min after the rain stops; cover open connectors with the rain hood; note the rain event on the visit sheet.
```
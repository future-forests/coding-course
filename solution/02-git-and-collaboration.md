## Quick reference card

| Command | Full name / meaning |
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
| `git clone` | Copy a remote repository, download a gitlab project |
| `git pull` | Fetch and merge remote changes, get your colleagues' latest work |
| `git push` | Upload local commits, share your checkpoints with the team |

# Class 2 — Version Control and Collaboration (Git Basics + GitLab)

You will probably be involved in research projects that can last months or year. As your research develops, you will write and modify analysis scripts, process new data, test different approaches, and collaborate with others who may need to reproduce, review, or build on your work. Sooner or later you need to answer:

- *Which version of the code produced this figure?*
- *What exactly changed since last week?*
- *Can I try a new analysis without breaking what already works?*

That is what **version control** is for: a system that **tracks every change** to your project over time, lets you **go back**, **compare** versions, and **work in parallel** without overwriting each other.

**Git** is the tool we use to do version control. Instead of saving `protocol_v2_final.docx`, version control keeps **one file** with a full history of documented snapshots. Git is the program that stores and organizes those snapshots on your machine.

## How Git implements version control

Git splits your work into three areas on your machine:

- **Working directory** — the files you edit (like any normal folder)
- **Staging area** — the file changes you marked as ready for the next snapshot
- **Repository** — everything Git has saved so far, files and their changes, stored in the hidden `.git` folder

## Let's start with our first `git` commands

### `git init` — Initialize repository

Creates a new Git repository in the current directory. Git can now track changes here.

```bash
cd my_project
git init
```

Before your first commit, tell Git **who you are** (only once):

```bash
git config --global user.email "your.name@kit.edu"
```

---

### `git status` — Check what is happening

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

> **Run this often**, especially before `git add` and `git commit` to understand what you are doing

---

### `git add` — Stage changes

Marks files (or changes) to include in the **next commit**.

```bash
git add protocol_staufen.md    # stage one file
git add -u                     # stage every change of tracked files
```

---

### `git commit` — Save a snapshot

Records the staged changes as a permanent snapshot in the repository history.

```bash
git commit -m "Add rain-event sampling rule"
```

> The flag `-m` is to leave a message, a short description of *why* you saved this commit. **This is the most important part of a commit**, you will learn how to make good commit messages with time.

---

### `git rm` — Remove files (Git-aware)

Deletes a file **and** records the deletion in Git (so the removal is part of history).

```bash
git rm old_protocol_draft.md
```

> If you delete a file manually (e.g. in the file explorer), Git still sees it as "deleted" — you then stage that with `git add old_protocol_draft.md` or `git add .`.

---

### `git log` — View history

Lists previous commits, newest first.

```bash
git log --oneline
```

---

### `git diff` — See what changed

Shows line-by-line differences, unstaged changes by default.

```bash
git diff                      # changes not yet staged (before git add)
git diff --staged             # changes already staged (after git add, before git commit)
```

> Tip: it is easier to use **VS Code** to visually review changes of a specific file, right click on one your file in the tab bar → Open Changes.

## Typical workflow (local)

When you work alone on your machine, the cycle is:

```
edit files  →  git add  →  git commit -m "describe your commit"
```

... and don't forget to use `git status` between each action to understand what you are doing.

## Exercise 1 — Typical workflow: track a field protocol

### Scenario

Your group maintains a sampling protocol for station **FF-MET-042**. Set up a Git repository and save the starter protocol below in `protocol_staufen.md` as your first commit. Then add the rain-event rule in a second commit, and use `git log` to see how Git recorded each change.

Starter content:

```md
# FF-MET-042 sampling protocol

- Wind conditions: do not sample if wind > 12 m/s
- Sensor check: record battery level before each visit
```

**Solution:**

```bash
mkdir ff_met_protocol
cd ff_met_protocol
git init

touch protocol_staufen.md

# Add starter content

git status
git add protocol_staufen.md
git commit -m "Initial protocol"

# Add rain-event rule

git diff
git add protocol_staufen.md
git commit -m "Add rain-event rule"

git log --oneline
```

## Branching — work in parallel without breaking `main`

Until now, everything happened on one line of history (usually called **`main`**). Branches let you create a **parallel copy of the project** to experiment, then merge back when ready.

Why do we need branches? They let you work on a draft **without changing what everyone else relies on**. On `main` sits the approved protocol your group follows in the field, you do not want half-finished rules there. On a branch, you can add, rewrite, or delete freely. When the draft is ready, you merge it in.

This matters as soon as **two people work at the same time**. While you draft winter rules on your branch, a colleague can fix a typo on `main`. Git keeps both histories separate until you choose to combine them — no overwritten files, no `protocol_final_v3.docx` by email.

Example:

| Situation | Branch strategy |
| --------- | --------------- |
| `main` *(A)* holds the approved field protocol the whole group follows | Keep `main` stable — only reviewed rules |
| You want to draft winter sampling rules *(B)* | Create branch `feature/winter`, experiment there |
| A colleague fixes a unit error on `main` *(C)* | You stay on your branch; they push to `main`; you pull on `main` later *(D)*, then merge your branch *(E)* |

```
main:              A ────────────── C ─────────────── E
                    \                   \           /
feature/winter:      B ───────────────── D ────────
```

- **A → B** — you branch off the approved protocol to start your draft.
- **C** — meanwhile, `main` moves forward without you.
- **D** — you catch up with `main` before merging.
- **E** — your winter rules join the approved protocol.

---

### `git branch` — List branches

```bash
git branch              # list local branches (* = current)
```

---

### `git checkout` — Create and move to branch

Creates and moves you to another branch, or just move you to an existing one.

```bash
git checkout -b feature/winter    # create branch and switch (-b = branch)
git checkout feature/winter       # move to existing branch
```

---

### `git merge` — Combine branches

Brings commits from another branch into your **current** branch.

```bash
git checkout main
git merge winter
```

If the merge succeeds, Git creates a merge commit. However, you may encounter a merge conflict when the same lines have been edited differently in the two branches. You then need to **resolve the merge conflict** before completing the merge (we will look into that later).

## Exercise 2 — Branching: add a new feature to your repo

### Scenario

The approved protocol on **`main`** is what everyone follows in the field. You want to add new **winter sampling rules** with the following rule:

```md
- Frost: do not touch metal masts with bare hands when air temperature < 0 °C
```

Using the repo from Exercise 1, add a frost safety rule on branch `feature/winter`. Then merge it into `main`.

**Solution:**

```bash
cd ff_met_protocol

git checkout -b feature/winter

# Add frost rule 

git add protocol_staufen.md
git commit -m "Add frost safety rule"

git checkout main
git merge feature/winter
grep -i frost protocol_staufen.md

git log --oneline
```

# Part 2 — GitLab and Git collaboration 

Part 1 was about saving history on **your** machine. In research groups, the "trunk" of a project usually lives on a **remote** server where we can collaborate. At Future Forests, we are using a **GitLab** server (`gitlab.uni-freiburg.de/future-forests/`, feel free to add this to your browser favourites).

GitLab adds a web interface on top of Git: you can browse files, open bug/issue reports, read history, review changes, and discuss code before merging, without emailing zip files.

## Remote repositories on GitLab

### `git clone` — Copy a remote repository

Downloads an existing GitLab project (including full history), or **remote**, to your machine. **Do this once** when you join a project.

```bash
git clone git@gitlab.kit.edu:fufo/fufo_coding_course.git  # TODO: permission issue?
cd fufo_coding_course
```

A **remote** is the copy of the repo hosted on GitLab. By convention it is called **`origin`**. To check the origin, you can do:

```bash
git remote -v
# origin  TOCHANGEHERE (fetch)
# origin  TOCHANGEHERE (push)
```

---

### `git pull` — Get changes from GitLab

Downloads commits from the remote **and merges them** into your current branch.

```bash
git checkout main
git pull
```

> **Rule of thumb:** `git pull` on `main` **before** you create a new branch to keep your repo updated with the most recent changes.

---

### `git push` — Send commits to GitLab

Uploads your local commits to the remote branch on GitLab.

```bash
git push             # CHECKHERE
```

## Resolve a merge conflict

When a conflict occurs, VS Code (or GitLab) will show the conflicts in the file as follows (read this part in the editor):

```
<<<<<<< HEAD
- Wind conditions: do not sample if wind > 12 m/s
=======
- Wind conditions: do not sample if wind > 10 m/s
>>>>>>> feature/winter
```

HEAD is your current branch, the bottom block is the branch you're merging in. You can find different options:

- **Accept Current Change:** keep the version from your current branch (`HEAD`) — here, the 12 m/s threshold on `main`
- **Accept Incoming Change:** keep the version from the branch you are merging in — here, the 10 m/s threshold from `feature/winter`
- **Accept Both Changes:** keep both lines one after the other — usually wrong for a single rule; edit manually afterwards
- **Compare Changes:** open a side-by-side view of the two versions to decide which threshold is correct

Repeat for every conflicted file, then `git add` and `commit` in the terminal to finish the merge:

```bash
git add protocol_staufen.md
git commit -m "Resolve merge conflict in wind rule"
```

## Exercise 3 — Resolve a merge conflict (with instructor update)

### Scenario

You are drafting a new rule on branch `feature/safety-vest`, which recommends a new wind speed limit of 10 m/s. While doing that, your supervisor updated the shared protocol to the new sensor limit (8 m/s). When you bring `main` into your branch, Git flags a **merge conflict** on the same line.

This mimics what happens in real projects: `main` moves forward while your branch is still open.

### Task

From the repo in Exercise 2, create branch `feature/safety-vest`, add the vest rule below, and change the wind line to **10 m/s** (your field notes suggest the old limit was too high). Commit, then merge the latest `main` into your branch and **resolve the conflict** before finishing the merge.

New rule to add:

```md
- Safety: wear high-visibility vest and safety boots on site at all times
```

### What Adrien should do during the class

**Wait until most students have committed on `feature/safety-vest`**, then update `main` on the shared repo (or ask students to pull your commit):

```md
- Wind conditions: do not sample if wind > 8 m/s
```

Commit message: `"Update wind threshold after group meeting"`

Tell students: *“Main has changed — run `git checkout main`, `git pull`, then go back to your branch and merge `main`.”*

### What students should see

Git stops the merge and marks the conflict:

```
<<<<<<< HEAD
- Wind conditions: do not sample if wind > 8 m/s
=======
- Wind conditions: do not sample if wind > 10 m/s
>>>>>>> main
```

Discuss as a class which value should stay (likely **8 m/s** — the sensor value), resolve in VS Code, then complete the merge.

**Solution:**

```bash
cd ff_met_protocol

git checkout main
git pull   # or: instructor pushes first; students pull the new wind rule

git checkout -b feature/safety-vest

# Edit protocol_staufen.md:
#   - change wind line to 8 m/s
#   - add the safety vest rule

git add protocol_staufen.md
git commit -m "Add safety vest rule and propose 8 m/s wind limit"

# main moved while you were working — bring it in
git merge main
# CONFLICT in protocol_staufen.md — resolve in VS Code (keep 12 m/s, keep vest rule)

git add protocol_staufen.md
git commit -m "Merge main and resolve wind threshold conflict"
```

End of class?

## The feature branch workflow

A **workflow** is the set of rules a team agrees to follow when sharing a project. It turns Git from a personal time machine into a way of working together without overwriting each other.

Most research software teams (like climate modelling groups) follow the **feature branch workflow**. You already practiced the core idea in Exercise 2 and 3:

1. `main` stays stable. It is the approved protocol.
2. One branch per task, named for what it does (e.g. `feature/winter` for a new feature, `fix/temp-formula` to solve a bug). One branch per idea. If you're doing two unrelated things, that's two branches.
3. Never commit directly to `main`. Even for a one-line fix.
4. Open a Merge Request (MR) when your change is ready. Be sure to merge main (the last changes that have been made) beforehand. There is where you might have to solve **merge conflicts**. A colleague reads it, comments, approves. You can merge your branch to `main`
5. Your work is now part of main; everyone else picks it up with git pull the next time they start a branch. 

## Exercise 4 — Build the class protocol on GitLab (20 students)

### Scenario

The instructor hosts a shared repository on **GitLab** with a starter `protocol_staufen.md`. The class (20 students) each adds **one assigned sampling rule**, for the instructor sheet.

Following the **feature branch workflow**, nobody pushes directly to `main`. Each student opens a **Merge Request** with their single new bullet point.

### Task

Clone the class repository on GitLab, add **your assigned rule** to `protocol_staufen.md` on your own branch, and open a Merge Request so it can be reviewed before it joins `main`. Do not edit `main` directly — by the end of the session, all 20 rules should be in one shared protocol.

**Example — student assigned rule #1:**

```bash
# 1 — clone (once)
git clone git@gitlab.kit.edu:fufo/ff-met-protocol.git
cd ff-met-protocol

# 2 — start from up-to-date main
git checkout main
git pull

# 3 — new branch (rule #1: rain events)
git checkout -b protocol/rain-events

# 4 — edit, commit, push (add only your assigned line)
git add protocol_staufen.md
git commit -m "Add protocol rule: rain events"
git push -u origin protocol/rain-events

# 5 — on GitLab (web browser):
#     Project → Merge requests → New merge request
#     Source: protocol/rain-events  →  Target: main
#     Add description, assign reviewer, Create merge request
#     After approval: Merge

# 6 — sync local main after all merges
git checkout main
git pull
cat protocol_staufen.md
```
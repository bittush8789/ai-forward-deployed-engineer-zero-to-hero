# Module 4.3: Advanced Git

Welcome to **Module 4.3**. The basics allow you to save code. Advanced Git allows you to manipulate time, rewrite history, and fix disastrous mistakes. FDEs frequently use these commands to keep commit histories clean before merging code into an enterprise codebase.

---

## 1. Detailed Theory

### Rewriting History (Rebase vs Merge)
- **Merge**: Takes the changes from the `main` branch and creates a new "Merge Commit" on your feature branch. It preserves exact chronological history but creates messy, non-linear commit graphs.
- **Rebase**: Takes your feature branch commits, temporarily sets them aside, fast-forwards your branch to the tip of `main`, and then "replays" your commits on top. It creates a perfectly linear, beautiful commit history (but rewrites commit hashes).

### Fixing Mistakes
- **`git commit --amend`**: Modifies the very last commit (e.g., you typo'd the commit message, or forgot a file).
- **`git revert <commit-hash>`**: Creates a *new* commit that undoes the changes of a previous commit. (Safe for public branches).
- **`git reset`**: Moves the branch pointer backward in time. 
  - `--soft`: Keeps your files as they are (puts changes in staging).
  - `--hard`: **DANGEROUS**. Deletes the commits AND deletes the file changes permanently.

### Utility Commands
- **`git stash`**: Temporarily shelves your uncommitted changes so you can switch branches without committing half-finished work. (`git stash pop` brings them back).
- **`git cherry-pick <commit-hash>`**: Grabs one specific commit from another branch and copies it onto your current branch.
- **Tags**: Immutable pointers to specific commits (e.g., `v1.0.0`). Used for marking production releases.

---

## 2. Architecture Diagram: Rebase vs Merge

```text
INITIAL STATE:
      A---B---C (main)
           \
            D---E (feature)

IF YOU MERGE MAIN INTO FEATURE:
      A---B---C (main)
           \   \
            D---E---F (feature)  <-- F is a merge commit

IF YOU REBASE FEATURE ONTO MAIN:
      A---B---C (main)
               \
                D'---E' (feature) <-- Linear history! (Hashes changed)
```

---

## 3. Production Use Cases

1. **Interactive Rebase for Clean PRs**: You made 15 tiny commits while developing a LangChain agent ("fix typo", "oops", "forgot import"). Before opening a Pull Request, you use `git rebase -i` to "squash" those 15 commits into 1 single, clean commit: "Implement LangChain Agent".
2. **Cherry Picking Hotfixes**: A severe bug is fixed on the `development` branch via commit `abc1234`. The release team needs that exact fix on the `production` branch immediately without taking all the other unstable features in `development`. They checkout `production` and run `git cherry-pick abc1234`.
3. **Stashing during an emergency**: You are halfway through writing a complex SQL migration. Your boss says production is down. You run `git stash`, switch to `main`, deploy the fix, switch back, and run `git stash pop` to resume exactly where you left off.

---

## 4. Coding Examples

### The Stash
```bash
$ git status
# Modified: heavy_math_logic.py

$ git stash
# Saved working directory and index state WIP

$ git checkout main
# (Do some work, push fixes)

$ git checkout my-feature
$ git stash pop
# Your modifications to heavy_math_logic.py are back!
```

### Amending a Commit
```bash
$ git commit -m "Added Redis cache"
# Oops, I forgot to add the redis configuration file!

$ git add redis.conf
# Adds it to the existing commit, lets you edit the message
$ git commit --amend -m "Added Redis cache and config"
```

### Undoing a Bad Deploy (Revert)
```bash
# You pushed a commit that broke the API.
# Find the hash using `git log` (e.g., 9f8a7b6)

$ git revert 9f8a7b6
# Git creates a NEW commit (e.g., 2c3d4e5) with the message "Revert 'Added Redis cache'"
# The code is fixed, and the history shows exactly what happened.
```

---

## 5. Hands-on Labs

**Lab: Time Travel with Reset**
**Objective**: Understand the danger of `git reset --hard`.
**Instructions**:
1. In your test repo, create a file `important.txt` and commit it.
2. Run `git log --oneline` and note the commit hash.
3. Create another file `mistake.txt` and commit it.
4. Run `git log --oneline`. You see both commits.
5. You want to undo the mistake completely. Run `git reset --hard HEAD~1` (Moves back 1 commit).
6. Run `ls`. Notice `mistake.txt` is physically gone from your hard drive.
7. Run `git log --oneline`. The commit is gone. You have altered history!

---

## 6. Assignments

**Assignment: The Squash**
*Note: This requires an understanding of the terminal text editor (Vim or Nano).*
1. Create a new branch `rebase-test`.
2. Create `file1.txt`, commit with message "WIP 1".
3. Create `file2.txt`, commit with message "WIP 2".
4. Create `file3.txt`, commit with message "WIP 3".
5. Run `git rebase -i HEAD~3`.
6. Your editor will open. Leave the word `pick` next to "WIP 1". Change `pick` to `squash` (or `s`) next to WIP 2 and WIP 3.
7. Save and close. Another editor opens to combine the commit messages. Delete the WIP messages and write "Add all 3 files".
8. Save and close. Run `git log`. You now have one perfectly clean commit!

---

## 7. Interview Questions

1. **Why is it dangerous to `git rebase` a public branch?**
   *Answer Hint: Rebasing rewrites history (changes commit hashes). If you rebase a branch that other developers have already pulled to their laptops, their Git history will completely diverge from the server's history, causing massive, unresolvable merge conflicts for the entire team.*
2. **What is the difference between `git revert` and `git reset`?**
   *Answer Hint: `revert` is safe; it creates a new commit that undoes changes, leaving the history intact. `reset` is destructive; it rewrites history by moving the branch pointer backward, effectively erasing commits.*
3. **What is a "Fast-Forward" merge?**
   *Answer Hint: When the target branch (e.g., main) has no new commits since you branched off it. Git doesn't need to create a new merge commit; it simply moves the main pointer "forward" to match your feature branch.*

---

## 8. Best Practices (FDE Standards)

- **Rebase local, Merge remote**: Use `git rebase main` on your *local* feature branch frequently to keep it up to date with your team's changes cleanly. But when integrating your feature into the shared repository, always use Pull Requests which execute a `merge`, preserving the historical context of the feature integration.

---

## 9. Common Mistakes

- **Panicking during a Rebase Conflict**: During a rebase, if there is a conflict, Git pauses. Developers panic and try to `git commit`. 
  *Fix: Resolve the conflict in the file, run `git add <file>`, and then run `git rebase --continue`. If you are completely lost, run `git rebase --abort` to safely cancel the entire operation.*

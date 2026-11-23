# Your first Git workflow

Slide 26 covers staging, commits, branches, merging, pushing and cloning. The commands below reproduce the exercise using disposable repositories. Start in this exercise folder in Bash. The first line records where the supplied installer is stored.

```bash
exercise_dir="$PWD"
lab="$(mktemp -d)"
cd "$lab"

# 1–3. Configure the practice repository and make the first commit.
git --version
git init -b main my-first-repo
cd my-first-repo
git config user.name "Exercise Author"
git config user.email "exercise@example.invalid"
touch readme.txt
git status --short
git add readme.txt
git diff --cached --stat
git commit -m "Add readme file"

# 4–5. Edit the file, inspect the unstaged change, then commit.
printf '%s\n' 'Git practice repository' >> readme.txt
git status --short
git diff
git add readme.txt
git commit -m "Describe the practice repository"
git log --oneline

# 6–7. Create branches and commit an installer on feature-script.
git branch feature-script
git switch feature-script
git switch -c dev
git switch feature-script
git branch
cp "$exercise_dir/bash-installer/install.sh" .
chmod +x install.sh
git add install.sh
git update-index --chmod=+x install.sh
git commit -m "Add install script"

# 8. Verify the file appears on main after a fast-forward.
git switch main
test ! -e install.sh
git merge --ff-only feature-script
test -f install.sh
git branch -d feature-script
git log --oneline

# 9–10. Use a local bare remote for the reproducible check.
# For the GitHub version, create an empty repo and set remote to its clone URL.
git init --bare --initial-branch=main "$lab/remote.git"
remote="$lab/remote.git"
git remote add origin "$remote"
git push -u origin main
cd "$lab"
mv my-first-repo original
git clone "$remote" my-first-repo
git -C my-first-repo log --oneline
bash my-first-repo/install.sh --dry-run

# 11. Repeat the full workflow for the installer project.
git init -b main bash-installer
cd bash-installer
git config user.name "Exercise Author"
git config user.email "exercise@example.invalid"
cp "$exercise_dir/bash-installer/README.md" .
git add README.md
git commit -m "Document tree installer"
git switch -c feature-install
cp "$exercise_dir/bash-installer/install.sh" .
git add install.sh
git update-index --chmod=+x install.sh
git commit -m "Add tree package setup"
git switch main
git merge --ff-only feature-install
git branch -d feature-install
git init --bare --initial-branch=main "$lab/installer-remote.git"
git remote add origin "$lab/installer-remote.git"
git push -u origin main
git log --oneline
```

After editing the README, status shows an unstaged modification. `git diff` shows its changed lines and `git log --oneline` shows one line per commit. Expect two commits after the first README edit, three after the first merge, and two in the final installer project. The installer appears on `main` when the fast-forward moves `main` to the feature commit.

On GitHub, use the URL of a second empty repository for the installer remote. The clone check renames the original so you can verify the fresh checkout and still recover it. For the prompt's deletion step, the command is `rm -r my-first-repo` from its parent after confirming it is the disposable copy and the remote has its history.

## Reflection

- Version control records changes, supports collaboration, and lets you recover earlier versions.
- Staging selects the content that goes into the next commit. A commit records that snapshot in history.
- Commit a small, coherent change once you can explain and check it. Descriptive messages help reviewers and future debugging.
- `git init` creates a repository. `git clone` copies an existing repository and its history.
- Branches isolate work such as a bug fix or experiment until it is ready to merge.

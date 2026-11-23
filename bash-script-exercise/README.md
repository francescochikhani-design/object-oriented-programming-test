# Set up a Python development environment

Slide 18 asks for a Bash script that detects the OS, checks Python and pip, and installs Jupyter. This solution supports macOS with Homebrew and Debian/Ubuntu with apt. Jupyter runs in a dedicated virtual environment. The script logs command exit statuses to ~/env_install.log and reports failed commands.

For the shell setup, use `ps -p $$` to identify the running shell and `printf '%s\n' "$SHELL"` to see your login shell. Follow the Oh My Bash or Oh My Zsh setup instructions, choose a theme, and enable Git in its plugin list. Run `source ~/.bashrc` or `source ~/.zshrc` so the theme and aliases take effect in your current shell. Check with `type gst`.

```bash
bash -n env_install.sh
bash env_install.sh --dry-run
bash env_install.sh
"$HOME/.local/share/oop-jupyter/bin/jupyter" notebook --version
bash env_install.sh --uninstall
```

`--dry-run` previews commands. `--verbose` prints commands as they run and `--quiet` sends command output to the log. Uninstall removes the Notebook package from the exercise environment. Launch the notebook by replacing `notebook --version` with `notebook` in the check above.

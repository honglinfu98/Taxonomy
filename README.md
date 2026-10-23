# Taxonomy

## Setup

```bash
chmod +x setup_repo.sh
./setup_repo.sh
. venv/bin/activate
cp .env.example .env   # fill in HPC_* and SMTP_*
```

`setup_repo.sh` creates a local `venv/`, installs `requirements.txt`, and drops a
`.pth` file into the venv so `import taxonomy` works from anywhere once the venv
is active. There is no `pyproject.toml`; the package lives flat at the repo root.

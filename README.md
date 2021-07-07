# asahiMigration
Migration tool for gulag/ripple servers to switch to Asahi.

## Setup

Clone the repo and install the requirements:

```bash
git clone https://github.com/tsunyoku/asahiMigration.git && cd asahiMigration
python3.9 -m pip install -r requirements.txt
```

Copy the config file and edit it:

```bash
cp ext/config.sample.py config.py
```

Run the migrator:

```bash
python3.9 main.py
```
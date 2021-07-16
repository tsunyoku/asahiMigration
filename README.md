# asahiMigration
Migration tool for gulag/ripple servers to switch to Asahi.

## Setup

NOTE: This tool will assume you are using MariaDB and not MySQL. If you are using MySQL and not MariaDB, please edit main.py so it uses mysql instead of mariadb!

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
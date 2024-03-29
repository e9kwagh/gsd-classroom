# Qjango - A Qux Django Template

## Getting Started

```
account="quxdev"
repo="qjango"

git clone https://github.com/${account}/${repo}.git
cd ${repo}
```

``` shell
# Update submodules
git submodule update --init

# Create virtual environment
python3 -m venv venv

if [[ $OSTYPE != darwin* ]]; then
    sed -i '' 's/PS1=\"(venv)/PS1=\"(venv:${repo})/g' venv/bin/activate
else
    sed -i 's/PS1=\"(venv)/PS1=\"(venv:${repo})/g' venv/bin/activate
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install packages
pip install --upgrade pip
```

You get this error if pip is not running at least version 24.0 

```shell
$ pip install -r requirements/prod.txt 
Usage: pip [options]

ERROR: Invalid requirement: pygraphviz==1.11 --config-settings="--global-option=build_ext" --config-settings="--global-option=-I$(brew --prefix graphviz)/include/" --config-settings="--global-option=-L$(brew --prefix graphviz)/lib/"; sys_platform == "darwin"
pip: error: no such option: --config-settings
```

Upgrading pip will solve the problem.

```shell
pip install -r requirements/prod.txt

# Migrate models to db.sqlite3
python manage.py migrate

# Configure project/.env
dotenv="project/.env"
if [ ! -f dotenv ]; then
    touch ${dotenv}
    secret=$(python manage.py generate_secret_key)
    echo "DJANGO_SECRET_KEY=\"${secret}\"" >> ${dotenv}
    echo "DJANGO_DEBUG=true" >> ${dotenv}
    echo "BOOTSTRAP=bs5" >> ${dotenv}
fi

# Runserver and test
python manage.py runserver
```

## ENVIRONMENT

### Django

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_SITE_ID`
- `BOOTSTRAP=bs5`

### Database

- `DB_TYPE` = `[sqlite3|mysql]`
- `DB_NAME`
- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

### wsgi.py

!! There is no reason to set these by default.

- `DJANGO_SETTINGS_MODULE`
- `DJANGO_PYTHON_PATH`

## Templates

### `_blank.html`

1. `qux_page_title_extra`: additional classes in heading
2. `qux_page_title`: page title
3. `qux_page_content`: page content

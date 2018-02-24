import os
from fabric.contrib.files import upload_template, exists
from fabric.api import env, run, cd, prefix, sudo, shell_env
from contextlib import contextmanager

env.hosts = ['dev']
env.use_ssh_config = True


@contextmanager
def venv_in_project_dir():
    with cd(env.base_dir):
        with prefix('source {venv_dir}/bin/activate'.format(**env)):
            yield


def set_env():
    env.project_name = 'transcendence'
    env.base_dir = '/opt/{project_name}'.format(**env)
    env.venv_dir = os.path.join('/opt', '.venv', '{project_name}'.format(**env))
    env.repo = os.getenv('GIT_REPO')
    env.db_uri = os.getenv('DJANGO_DB_URI')
    env.password = os.getenv('DB_PASSWORD')
    env.secret_key = os.getenv('DJANGO_SECRET_KEY')
    env.raven_secret = os.getenv('DJANGO_RAVEN_SECRET')
    env.domain = os.getenv('DOMAIN')


def setup():
    run('mkdir -p {base_dir}'.format(**env))
    with cd(env.base_dir):
        run('git clone {repo} .'.format(**env))
    with venv_in_project_dir():
        run('pip install --upgrade pip')
        run('pip install -r requirements.txt')
        with shell_env(
            DJANGO_DB_URI=env.db_uri,
            DJANGO_SECRET_KEY=env.secret_key
        ):
            run('python manage.py migrate --noinput')
            run('python manage.py collectstatic --noinput')
            run_command = (
                "from django.contrib.auth.models import User;"
                "User.objects.create_superuser('admin', 'admin@example.com', '{password}');".format(**env)
            )
            run('python manage.py shell -c "{}"'.format(run_command))
    run('chown -R www-data: {base_dir}'.format(**env))


def create_virtualenv():
    run('python3 -m venv {venv_dir}'.format(**env))


def install_system_libs():
    run('apt update')
    run('apt -y install sudo git python3-venv python3-pip nginx postgresql')


def service_setup():
    destination = '/etc/systemd/system/{project_name}.service'.format(**env)
    context = {
        'project_name': env.project_name,
        'venv_dir': env.venv_dir,
        'base_dir': env.base_dir,
        'db_uri': env.db_uri,
        'secret_key': env.secret_key,
        'raven_secret': env.raven_secret
    }
    upload_template(
        'systemd.service',
        destination,
        context=context,
        use_jinja=True,
        template_dir='server'
    )
    run('systemctl enable --now {project_name}.service'.format(**env))


def nginx_setup():
    destination = '/etc/nginx/sites-available/{project_name}.conf'.format(**env)
    context = {
        'domain': env.domain,
        'base_dir': env.base_dir,
        'project_name': env.project_name
    }
    upload_template(
        'nginx.conf',
        destination,
        context=context,
        use_jinja=True,
        template_dir='server'
    )
    run('ln -s /etc/nginx/sites-available/{project_name}.conf /etc/nginx/sites-enabled/'.format(**env))
    run('rm -f /etc/nginx/sites-enabled/default')
    run('systemctl restart nginx.service')


def postgres_setup():
    sudo('psql -c "create user {project_name} with encrypted password E\'{password}\'"'.format(**env), user='postgres')
    sudo('psql -c "create database {project_name} with owner {project_name}"'.format(**env), user='postgres')


def remove():
    set_env()
    run('systemctl stop {project_name}.service'.format(**env))
    run('systemctl disable {project_name}.service'.format(**env))
    run('rm /etc/systemd/system/{project_name}.service'.format(**env))
    run('systemctl daemon-reload')
    run('rm -f /etc/nginx/sites-enabled/{project_name}.conf'.format(**env))
    run('rm -rf {base_dir}'.format(**env))
    run('rm -rf {venv_dir}'.format(**env))
    sudo('dropdb {project_name}'.format(**env), user='postgres')
    sudo('dropuser {project_name}'.format(**env), user='postgres')
    run('apt -y autoremove nginx postgresql-9.6')


def fresh_install():
    set_env()
    install_system_libs()
    create_virtualenv()
    postgres_setup()
    setup()
    service_setup()
    nginx_setup()


def bootstrap():
    set_env()
    if exists('{base_dir}'.format(**env)):
        setup()
    else:
        fresh_install()

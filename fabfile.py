import os
from fabric.contrib.files import upload_template, exists
from fabric.api import env, run, cd, sudo, shell_env
from fabric.context_managers import settings

env.hosts = ['dev']
env.use_ssh_config = True


def set_env():
    env.PROJECT_NAME = os.getenv('PROJECT_NAME')
    env.BASE_DIR = '/opt/{PROJECT_NAME}'.format(**env)
    env.VENV_DIR = os.path.join('/opt', '.venv', '{PROJECT_NAME}'.format(**env))
    env.PYTHON = os.path.join(env.VENV_DIR, 'bin', 'python')
    env.REPO = os.getenv('GIT_REPO')
    env.DB_URI = os.getenv('DJANGO_DB_URI')
    env.PASSWORD = os.getenv('DB_PASSWORD')
    env.SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    env.RAVEN_SECRET = os.getenv('DJANGO_RAVEN_SECRET')
    env.DOMAIN = os.getenv('DOMAIN')


def install_system_libs():
    run('apt update')
    run('apt -y install sudo git python3-venv python3-pip nginx postgresql-9.6')


def create_or_update_dir_with_project():
    run('mkdir -p {BASE_DIR}'.format(**env))
    with cd(env.BASE_DIR):  # noqa
        run('git clone {REPO} .'.format(**env))
    run('chown -R www-data: {BASE_DIR}'.format(**env))


def create_virtualenv():
    run('python3 -m venv {VENV_DIR}'.format(**env))
    run('{PYTHON} -m pip install --upgrade pip'.format(**env))


def install_requirements():
    with cd(env.BASE_DIR):
        run('{PYTHON} -m pip install -r requirements.txt'.format(**env))


def create_project_database():
    sudo('psql -c "create user {PROJECT_NAME} with encrypted PASSWORD E\'{PASSWORD}\'"'.format(**env), user='postgres')
    sudo('psql -c "create database {PROJECT_NAME} with owner {PROJECT_NAME}"'.format(**env), user='postgres')


def migrate_and_collect_static(is_new=False):
    with cd(env.BASE_DIR), shell_env(
            DJANGO_DB_URI=env.DB_URI,
            DJANGO_SECRET_KEY=env.SECRET_KEY
    ):
        run('{PYTHON} manage.py migrate --noinput'.format(**env))
        run('{PYTHON} manage.py collectstatic --noinput'.format(**env))
        if is_new:
            with settings(prompts={
                "Password: ": env.PASSWORD,
                "Password (again): ": env.PASSWORD
            }):
                run('{PYTHON} manage.py createsuperuser --username admin --email admin@admin.com')


def install_systemd_project_service():
    destination = '/etc/systemd/system/{PROJECT_NAME}.service'.format(**env)
    context = {
        'PROJECT_NAME': env.PROJECT_NAME,
        'VENV_DIR': env.VENV_DIR,
        'BASE_DIR': env.BASE_DIR,
        'DB_URI': env.DB_URI,
        'SECRET_KEY': env.SECRET_KEY,
        'RAVEN_SECRET': env.RAVEN_SECRET
    }
    upload_template(
        'systemd.service',
        destination,
        context=context,
        use_jinja=True,
        template_dir='server_templates'
    )
    run('systemctl enable --now {PROJECT_NAME}.service'.format(**env))


def install_nginx_project_conf():
    destination = '/etc/nginx/sites-available/{PROJECT_NAME}.conf'.format(**env)
    context = {
        'DOMAIN': env.DOMAIN,
        'BASE_DIR': env.BASE_DIR,
        'PROJECT_NAME': env.PROJECT_NAME
    }
    upload_template(
        'nginx.conf',
        destination,
        context=context,
        use_jinja=True,
        template_dir='server_templates'
    )
    run('ln -s /etc/nginx/sites-available/{PROJECT_NAME}.conf /etc/nginx/sites-enabled/'.format(**env))
    run('systemctl restart nginx.service')


def fresh_install():
    install_system_libs()
    create_or_update_dir_with_project()
    create_virtualenv()
    install_requirements()
    create_project_database()
    migrate_and_collect_static(is_new=True)
    install_systemd_project_service()
    install_nginx_project_conf()


def bootstrap():
    set_env()
    if exists(env.BASE_DIR):
        create_or_update_dir_with_project()
        migrate_and_collect_static()
        run('systemctl restart {PROJECT_NAME}.service'.format(**env))
    else:
        fresh_install()

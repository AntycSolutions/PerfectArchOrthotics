from fabric import api, context_managers
from fabric.api import env


dev_host = (
    'perfectarch.antyc.ca',
)

prod_hosts = (
    'perfectarch.ca',
)

all_hosts = prod_hosts + dev_host


env.user = 'airith'


@api.hosts(all_hosts)
def update_all():
    update_server()


@api.hosts(dev_host)
def update_dev():
    update_server()


@api.hosts(prod_hosts)
def update_prod():
    update_server()


def update_server():
    if env.host == 'perfectarch.ca':
        raise Exception('Unhandled')

    with context_managers.cd(
        'public_html/{}/PerfectArchOrthotics'.format(
            env.host
        )
    ):
        api.run('git pull -q')

        with api.prefix('source ../venv_perfect_arch/bin/activate'):
            # without -q we get unicode issues
            api.run('pip install -q -r requirements.txt')
            api.run('python manage.py migrate -v 0')
            api.run('python manage.py collectstatic -v 0 --noinput')

    api.sudo('service apache2 restart')

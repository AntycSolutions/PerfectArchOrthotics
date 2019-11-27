from fabric import api, context_managers
from fabric.api import env


dev_host = (
    'perfectarch.antyc.ca',
)

prod_hosts = (
    'perfectarch.ca',
)

all_hosts = prod_hosts + dev_host


@api.hosts(all_hosts)
def update_all(branch=''):
    update_server(branch=branch)


@api.hosts(dev_host)
def update_dev(branch=''):
    update_server(branch=branch)


@api.hosts(prod_hosts)
def update_prod(branch=''):
    update_server(branch=branch)


def update_server(branch=''):
    if env.host == 'perfectarch.ca':
        env.user = 'perfectarch'
        path = '{}/PerfectArchOrthotics'
    elif env.host == 'perfectarch.antyc.ca':
        env.user = 'airith'
        path = 'public_html/{}/PerfectArchOrthotics'
    else:
        raise Exception('Unhandled')

    with context_managers.cd(path.format(env.host)):
        api.run('git pull -q')
        if branch:
            api.run('git checkout {}'.format(branch))

        with api.prefix('source ../venv_perfect_arch/bin/activate'):
            # without -q we get unicode issues
            api.run('pip install -q -r requirements.txt')
            api.run('python manage.py migrate -v 0')
            api.run('python manage.py collectstatic -v 0 --noinput')

    api.sudo('service apache2 reload')

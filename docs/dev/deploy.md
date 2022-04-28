# Deployment

The deployment process is controlled by [Ansible](https://www.ansible.com/). The ansible configurations are in the `deploy` and `provision` folders in the source tree. The `deploy` folder currently contains a `staging.yml` playbook. Portal deployments are configured on a per-country basis, with each country having its own ansible variable file stored in the `vars` directory and named `{country}_vars.yml`. The `vars` file is specified on the commandline to determine which instance gets deployed (see below).

The `provision` directory contains ansible configurations which determine the deployment tasks. There are a number of sub-directories as follows:

- `files`: contains templates that get populated with variables and installed on the host machine.
- `handlers`: operating system tasks, eg restaring nginx.
- `tasks`: ansible installation tasks, eg checking out the repo, installing OS dependencies etc.

Vars files are encrypted using `ansible-vault` and are committed to the github repository. The deployment process injects the variables found in the `{country}_vars.yml` file into a `.env` file. This `.env` file is then copied into the root directory of the country deployment folder. A separate `.env` file for frontend variables is copied into the `frontend` folder. When the application starts, the `.env` files are read and the portal instance configures itself using the variables found there.

To deploy a portal instance to production or staging, create a `.vault-pass` file in the root directory of the source tree. Your `.vault-pass` file shoud have the format `{ country } { your_country_password }`, eg `paraguay paraguay_password`. This file **SHOULD NOT** be checked into the repo. The `.vault-pass` file allows ansible to decrypt the `{country}_vars.yml` file during deployment. The contents of the `{country}_vars.yml` file can be viewed by running the following command.

`ansible-vault view deploy/vars/{country}_vars.yml --vault-password-file=.vault-pass` where `{country}` is the particular country the portal instance is being deployed for. See [here](https://docs.ansible.com/ansible/latest/user_guide/vault.html) for more information on `ansible-vault`.

**_Please get in touch for the ansible vault password for your country_**.

Ansible requires a `hosts.ini` file containing the IP address of the production/staging instance to be in the root of the application directory. Again, this file **SHOULD NOT** be committed to the repo. The `hosts.ini` file should look like this...

    [production]
    xxx.xxx.xxx.xxx

    [staging]
    xxx.xxx.xxx.xxx

    [staging:vars]
    ansible_python_interpreter=/usr/bin/python3

The ssh key for the staging / production instance should be loaded in a running ssh-agent. Then, to perform the actual production deployment run:

```bash
ansible-playbook -i hosts.ini -e @deploy/vars/{country}_vars.yml \
deploy/staging.yml --vault-password-file=.vault-pass
```

Anisble will connect to the production instance via ssh and run the provisioning and deployment configurations at `./provision/tasks`. See `./deploy/staging.yml` for an example of the tasks executed for each portal instance.

# Roles Notes

> **NOTE** - These notes assume you are:
>
> - You are using a Python virtual environment.
> - You have installed Ansible and Ansible Lint in the environment.
> - An inventory file (`inventory.ini`) exists in your project directory containing a node with a local connection (e.g., `managed_node1 ansible_connection=local`).
> - An Ansible configuration file (i.e., `ansible.cfg`), set to use your inventory (e.g., `inventory=inventory.ini`), exists in your project directory.

-----

## Create a Role

Activate your Python virtual environment and create a role:

```bash
cd ~/a4p
source bin/activate
mkdir --parents roles
cd roles
ansible-galaxy init demo_role
# Remove the tests subdirectory if you are not publishing
# the role or using Travis CI
rm -rf demo_role/tests
```

Get the version number of Ansible you are using:

```bash
ansible --version
```

> **NOTE** - If you are using the AWX project, the Red Hat Ansible Automation Platform (AAP) or Ansible Tower, get the version number of Ansible used by the execution environment instead.

Using an editor of your choice, open `demo_role/meta/main.yml` and modify the following items:

- author: Enter your name
- description: Enter a description of the role
- company: Enter the name of your company. This line is optional and you may delete it.
- license: Enter the type of license (GPL-2.0-or-later, MIT, etc)
- min_ansible_version: Enter the Ansible version number you are using in quotes (e.g., "2.9", "2.16", etc.)


Using an editor of your choice, open `demo_role/tasks/main.yml` and add the following code:

```yaml
---
# tasks file for demo_role
- name: Show a greeting
  ansible.builtin.debug:
    msg: "Hello from the role!"
...
# code: language=ansible
# vi: set noai nu ts=2 sw=2 sts=2 sta et:
```

Create a playbook:

```bash
cd ~/a4p
touch use_roles.yml
```

Using an editor of your choice, open `use_roles.yml` and add the following code:

```yaml
---
# Use a role in a playbook
# Usage: ansible-playbook use_roles.yml
- name: Use roles
  hosts: managed_node1
  gather_facts: false
  tasks:
    - name: Run demo_role/tasks/main.yml
      ansible.builtin.include_role:
        name: demo_role
...
# code: language=ansible
# vi: set noai nu ts=2 sw=2 sts=2 sta et:
```

Check the playbook and the role for any issues:

```bash
ansible-lint
```

Run the playbook:

```bash
ansible-playbook use_roles.yml
```

-----

## Use a Callback Plugin with a Role

Add a callback plugin directory:

```bash
cd ~/a4p
mkdir -p roles/demo_role/callback_plugins
```

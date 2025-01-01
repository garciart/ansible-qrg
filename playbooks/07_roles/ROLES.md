# Working with Roles

-----

## Create a Role

Activate your Python virtual environment and create a role:

```bash
source .venv/bin/activate
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

> **NOTE** - If you are using the AWX project, the Red Hat Ansible Automation Platform (AAP), or Ansible Tower, get the version number of Ansible used by the execution environment instead.

Using an editor of your choice, open `demo_role/meta/main.yml` and modify the following items:

- ***author:*** Enter your name
- ***description:*** Enter a description of the role
- ***company:*** Enter the name of your company. This line is optional and you may delete it.
- ***license:*** Enter the type of license (GPL-2.0-or-later, MIT, etc)
- ***min_ansible_version:*** Enter the Ansible version number you are using in quotes (e.g., "2.9", "2.16", etc.)

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

Create a playbook named `use_roles.yml` in the parent directory of the role (i.e., not in the role itself) and, using an editor of your choice, add the following code:

```yaml
---
# Use a role in a playbook
# Usage: ansible-playbook use_roles.yml
- name: Use roles
  hosts: all
  gather_facts: false
  roles:
    - demo_role
...
# code: language=ansible
# vi: set noai nu ts=2 sw=2 sts=2 sta et:
```

> **NOTE** - There are several ways to activate a role

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

Ansible uses [callback plugins](https://docs.ansible.com/ansible/latest/plugins/callback.html) to format output, specifically the [`default.py`](https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/callback/default.py) callback if you do not override `callbacks_enabled=` in `ansible.cfg` with a built-in callback, like `minimal` or `oneline`, or a custom callback.

All callback plugins inherit from the `CallbackBase` class, and you can override all of the public methods and variables in [`__init__.py`](https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/callback/__init__.py)

Add a callback plugin directory:

```bash
mkdir -p roles/demo_role/callback_plugins
cd roles/demo_role/callback_plugins

```

`__init__.py` methods:

```python
def __init__(self, display=None, options=None) -> None:
def v2_playbook_on_start(self, playbook):
def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None, unsafe=None):
def v2_playbook_on_play_start(self, play):
def v2_playbook_on_no_hosts_matched(self):
def v2_playbook_on_task_start(self, task, is_conditional):
def v2_playbook_on_notify(self, handler, host):
def v2_playbook_on_handler_task_start(self, task):
def v2_playbook_on_cleanup_task_start(self, task):
def v2_runner_on_start(self, host, task):
def v2_runner_on_async_poll(self, result: TaskResult) -> None:
def v2_runner_on_async_ok(self, result):
def v2_runner_on_async_failed(self, result):
def v2_on_file_diff(self, result):
def v2_runner_on_ok(self, result):
def v2_runner_on_unreachable(self, result):
def v2_runner_on_failed(self, result, ignore_errors=False):
def v2_runner_on_skipped(self, result):
def v2_playbook_on_include(self, included_file):
def v2_playbook_on_no_hosts_remaining(self):
def v2_runner_item_on_ok(self, result):
def v2_runner_item_on_failed(self, result):
def v2_runner_item_on_skipped(self, result):
def v2_runner_retry(self, result):
def v2_playbook_on_stats(self, stats):
```

`default.py` methods:

```python
def __init__(self):
def v2_playbook_on_start(self, playbook):
def v2_playbook_on_play_start(self, play):
def v2_playbook_on_no_hosts_matched(self):
def v2_playbook_on_task_start(self, task, is_conditional):
def v2_playbook_on_notify(self, handler, host):
def v2_playbook_on_handler_task_start(self, task):
def v2_playbook_on_cleanup_task_start(self, task):
def _task_start(self, task, prefix=None):
def _print_task_banner(self, task):
def v2_runner_on_start(self, host, task):
def v2_runner_on_async_poll(self, result: TaskResult) -> None:
def v2_runner_on_async_ok(self, result):
def v2_runner_on_async_failed(self, result):
def v2_on_file_diff(self, result):
def v2_runner_on_ok(self, result):
def v2_runner_on_unreachable(self, result):
def v2_runner_on_failed(self, result, ignore_errors=False):
def v2_runner_on_skipped(self, result):
def v2_playbook_on_include(self, included_file):
def v2_playbook_on_no_hosts_remaining(self):
def v2_runner_item_on_ok(self, result):
def v2_runner_item_on_failed(self, result):
def v2_runner_item_on_skipped(self, result):
def v2_runner_retry(self, result):
def v2_playbook_on_stats(self, stats):
```

"""_summary_
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from ansible.plugins.callback import CallbackBase

if TYPE_CHECKING:
    from ansible.playbook.play import Play
    from ansible.playbook.task import Task

class CallbackModule(CallbackBase):
    """
    This is a custom aggregate callback interface that adds information
    to stdout when new callback events are received.
    """

    def __init__(self):
        super(CallbackModule, self).__init__()
        self._task_count = 1

    def v2_playbook_on_play_start(self, play):
        # type: (Play) -> None
        """Add additional behaviors when starting a play.
        
        Customization Notes - In this method:
        - You can access Play class methods and attributes like play.get_tasks() and play.hosts
        - You can access extra-vars using play.get_variable_manager().extra_vars
        - You can access play-level vars using play.get_vars()
        - You can access roles using play.get_roles()
        - You can access role vars by getting the role object and using role[0].get_default_vars()
        - The ansible.playbook.Play class is defined in lib/ansible/playbook/play.py
        - The ansible.playbook.role.Role class is defined in lib/ansible/playbook/role/__init__.py
        
        :param Play play: The running play instance
        :return: None
        """
        self._display.display('And we\'re off!', color='bright green')
        self._display.display(f'The hosts are: {play.hosts}', color='bright green')

    def v2_playbook_on_task_start(self, task: Task, is_conditional: bool) -> None:
        """Add additional behaviors when starting a normal task.
        
        Customization Notes - In this method:
        - You can access Task class methods and attributes like task.get_name() and task.action
        - You can access task-level vars using task.get_vars()
        - You can access extra_vars using task.get_variable_manager().extra_vars
        - The ansible.playbook.task.Task class is defined in lib/ansible/playbook/task.py

        :param Task task: The running task instance
        :param bool is_conditional: Not currently used by Ansible
        :return: None
        """
        self._display.display(f'This is task {self._task_count}.', color='bright yellow')
        self._display.display(f'Action: {task.action}.', color='bright yellow')
        self._task_count += 1

"""This is an annotated and customized version of Ansible's default stdout callback plugin.

If you do not tell Ansible to use another callback (e.g., minimal, oneline, etc.),
Ansible will use the default callback to display output to the screen.

You can customize output by changing the code in this callback
or by changing settings in ansible.cfg.
See https://docs.ansible.com/ansible/latest/collections/ansible/builtin/default_callback.html
for a list of applicable ansible.cfg settings.

Order of operations:
.
├── __init__
├── v2_playbook_on_start
│   ├── v2_playbook_on_play_start
│   │   ├── v2_playbook_on_no_hosts_matched (ends current play)
│   │   ├── v2_playbook_on_task_start
│   │   │   or v2_playbook_on_notify and v2_playbook_on_handler_task_start
│   │   │   or v2_playbook_on_cleanup_task_start
│   │   │   └── _task_start
│   │   │       └── _print_task_banner
│   │   │           └── v2_runner_on_start
│   │   |               ├── v2_runner_on_async_poll (if running in asynchronous mode)
│   │   |               |   ├── v2_runner_on_async_ok
│   │   |               |   └── v2_runner_on_async_failed
│   │   |               ├── v2_on_file_diff (if --diff arg is used)
│   │   │               └── v2_runner_on_ok
│   │   │                   or v2_runner_on_unreachable
│   │   │                   or v2_runner_on_failed
│   │   │                   or v2_runner_on_skipped
│   │   |                   ├── v2_playbook_on_include (if a file is included)
│   │   |                   ├── v2_playbook_on_no_hosts_remaining (if any_errors_fatal is true
│   │   |                   |   or max_fail_percentage is met)
│   │   |                   ├── v2_runner_item_on_ok
│   │   |                   |   or v2_runner_item_on_failed
│   │   |                   |   or v2_runner_item_on_skipped (if running a loop)
│   │   |                   └── v2_runner_retry (if retries is set)
│   │   └── (Repeat v2_playbook_on_task_start until all tasks in the play are completed)
│   └── (Repeat v2_playbook_on_play_start until all plays in the playbook are completed)
└── v2_playbook_on_stats
"""
# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

# ADDED imports used for type hints, input validation, and debugging
import inspect  # ADDED
import sys
from typing import Union  # noqa: F401 ADDED

from ansible import constants as C
from ansible import context
from ansible.executor.stats import AggregateStats  # ADDED
from ansible.executor.task_result import TaskResult  # ADDED
from ansible.inventory.host import Host  # ADDED
from ansible.playbook import Playbook  # ADDED
from ansible.playbook.handler import Handler  # ADDED
from ansible.playbook.included_file import IncludedFile  # ADDED
from ansible.playbook.play import Play  # ADDED
from ansible.playbook.task import Task  # ADDED
from ansible.playbook.task_include import TaskInclude
from ansible.plugins.callback import CallbackBase
from ansible.utils.color import colorize, hostcolor
from ansible.utils.fqcn import add_internal_fqcns

# Pylint overrides
# pylint: disable=locally-disabled, protected-access, consider-using-f-string

DOCUMENTATION = '''
    name: defaultunicode
    type: stdout
    short_description: default Ansible screen output
    version_added: historical
    description:
      - This is the default output callback for ansible-playbook.
    extends_documentation_fragment:
      - default_callback
      - result_format_callback
    requirements:
      - set as stdout in configuration
'''


class CallbackModule(CallbackBase):
    """
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'custom_default'

    # Added to prevent Pylint E1101-no-member error during development
    # Module 'ansible.constants' has no 'COLOR_<type>' member
    C.COLOR_CHANGED = 'yellow'
    C.COLOR_DEBUG = 'dark gray'
    C.COLOR_ERROR = 'red'
    C.COLOR_OK = 'green'
    C.COLOR_SKIP = 'cyan'
    C.COLOR_UNREACHABLE = 'bright red'
    C.COLOR_VERBOSE = 'blue'
    C.COLOR_WARN = 'purple'
    C.DISPLAY_ARGS_TO_STDOUT = 'false'

    # Additional constants

    DEV_MODE = True
    ARG_NOT_DEFINED = ' is not defined.'
    TRACE_COLOR = 'bright cyan'

    PYTHON_VERSION = float('{0}.{1:02d}'.format(sys.version_info.major, sys.version_info.minor))

    # Python 2 'str' type = Python 3 'bytes' type
    # Python 2 'unicode' type = Python 3 'str' type
    # noqa: Python 3 no longer recognizes unicode as a type, and it is undefined
    # pylint: disable-next=undefined-variable
    UNICODE_TYPE = str if PYTHON_VERSION >= 3 else unicode  # noqa:F821 # type:ignore

    def __init__(self):
        # type: () -> None
        """Create the class instance and initialize variables.

        :return: None
        """
        self._play = None
        self._last_task_banner = None
        self._last_task_name = None
        self._task_type_cache = {}
        super(CallbackModule, self).__init__()

        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

    def v2_playbook_on_start(self, playbook):
        # type: (Playbook) -> None
        """Inform the user the playbook has started and show additional information
        based on verbosity level, CLI args, and ansible.cfg settings, like check_mode_markers.

        Customization Notes - In this method:
        - You can access Playbook class methods and attributes like playbook.get_plays()
          and playbook._file_name
        - The ansible.playbook.Playbook class is defined in lib/ansible/playbook/__init__.py

        :param Playbook playbook: The running playbook instance
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('playbook', playbook, Playbook)

            # try:
            #     # Get and show the plays in the playbook
            #     _plays = playbook.get_plays()
            #     self._peek_inside('_plays', _plays)
            #
            #     # Get the name of the playbook
            #     self._peek_inside('playbook._file_name', playbook._file_name)
            # except KeyError as e:
            #     self._display.display(self.UNICODE_TYPE(e) + self.ARG_NOT_DEFINED)

        if self._display.verbosity > 1:
            from os.path import basename
            self._display.banner("PLAYBOOK: %s" %
                                 basename(playbook._file_name))

        # show CLI arguments
        if self._display.verbosity > 3:
            if context.CLIARGS.get('args'):
                self._display.display('Positional arguments: %s' % ' '.join(
                    context.CLIARGS['args']), color=C.COLOR_VERBOSE, screen_only=True)

            for argument in (a for a in context.CLIARGS if a != 'args'):
                val = context.CLIARGS[argument]
                if val:
                    self._display.display('%s: %s' % (
                        argument, val), color=C.COLOR_VERBOSE, screen_only=True)

        if context.CLIARGS['check'] and self.get_option('check_mode_markers'):
            self._display.banner("DRY RUN")

    def v2_playbook_on_play_start(self, play):
        # type: (Play) -> None
        """Inform the user a play has started and show additional information
        based on CLI args and ansible.cfg settings, like check_mode_markers.

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
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('play', play, Play)

            # try:
            #     # Get the tasks in the play
            #     _tasks = play.get_tasks()
            #     self._peek_inside('_tasks', _tasks)

            #     # Get the hosts targeted by the play
            #     self._peek_inside('play.hosts', play.hosts)

            #     # Get play-level vars
            #     _vars = play.get_vars()
            #     self._peek_inside('_vars', _vars)
            #     self._peek_inside("_vars['play_var']", _vars['play_var'])

            #     # Get extra vars from the command line
            #     _extra_vars = play.get_variable_manager().extra_vars
            #     self._peek_inside('_extra_vars', _extra_vars)

            #     # Get a list of the names of the roles included in the play
            #     _roles = play.get_roles()
            #     self._peek_inside('_roles', _roles)
            #     self._peek_inside('_roles[0]', _roles[0])

            #     # Get the default vars of a role
            #     _default_vars = _roles[0].get_default_vars()
            #     self._peek_inside('_default_vars', _default_vars)
            #     self._peek_inside("_default_vars['default_role_var']",
            #                       _default_vars['default_role_var'])
            # except KeyError as e:
            #     self._display.display(self.UNICODE_TYPE(e) + self.ARG_NOT_DEFINED)

        name = play.get_name().strip()
        if play.check_mode and self.get_option('check_mode_markers'):
            checkmsg = " [CHECK MODE]"
        else:
            checkmsg = ""
        if not name:
            msg = u"PLAY%s" % checkmsg
        else:
            msg = u"PLAY [%s]%s" % (name, checkmsg)

        self._play = play

        self._display.banner(msg)

    def v2_playbook_on_no_hosts_matched(self):
        # type: () -> None
        """Inform the user that Ansible is skipping the play because
        none of the target nodes are in the inventory.

        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

        self._display.display("skipping: no hosts matched", color=C.COLOR_SKIP)

    def v2_playbook_on_task_start(self, task, is_conditional):
        # type: (Task, bool) -> None
        """Wrapper for showing output when starting a normal task.
        Adds a 'TASK' prefix to the task banner.

        Customization Notes - In this method:
        - You can access Task class methods and attributes like task.get_name() and task.action
        - You can access task-level vars using task.get_vars()
        - You can access extra_vars using task.get_variable_manager().extra_vars
        - The ansible.playbook.task.Task class is defined in lib/ansible/playbook/task.py

        :param Task task: The running task instance
        :param bool is_conditional: Not currently used by Ansible
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('task', task, Task)

            # try:
            #     # Get task actions and arguments
            #     self._peek_inside('task.action', task.action)
            #     self._peek_inside('task.args', task.args)
            #     self._peek_inside("task.args['msg']", task.args['msg'])

            #     # Get task-level vars
            #     _vars = task.get_vars()
            #     self._peek_inside('_vars', _vars)

            #     # Get extra vars from the command line
            #     _extra_vars = task.get_variable_manager().extra_vars
            #     self._peek_inside('_extra_vars', _extra_vars)
            # except KeyError as e:
            #     self._display.display(self.UNICODE_TYPE(e) + self.ARG_NOT_DEFINED)

        self._task_start(task, prefix='TASK')

    def v2_playbook_on_notify(self, handler, host):
        # type: (Handler, Host) -> None
        """Inform the user a handler was notified if the verbosity level is met.

        Customization Notes - In this method:
        - You can access Handler class methods and attributes like handler.is_host_notified()
          and handler.notified_hosts
        - You can access Host class methods and attributes like host.get_name() and host.address
        - The ansible.playbook.handler.Handler class is defined in lib/ansible/playbook/handler.py
        - The ansible.playbook.host.Host class is defined in lib/ansible/inventory/host.py

        :param Handler handler: The handler task instance
        :param Host host: The target host instance
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('handler', handler, Handler)
            self._validate_input('host', host, Host)

        if self._display.verbosity > 1:
            self._display.display("NOTIFIED HANDLER %s for %s" % (
                handler.get_name(), host), color=C.COLOR_VERBOSE, screen_only=True)

    def v2_playbook_on_handler_task_start(self, task):
        # type: (Task) -> None
        """Wrapper for showing output when calling a handler.
        Adds a 'RUNNING HANDLER' prefix to the task banner.

        Customization Notes - In this method:
        - You can access Task class methods and attributes like task.get_name() and task.action
        - You can access task-level vars using task.get_vars()
        - You can access extra_vars using task.get_variable_manager().extra_vars
        - The ansible.playbook.task.Task class is defined in lib/ansible/playbook/task.py

        :param Task task: The running task instance
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('task', task, Task)

        self._task_start(task, prefix='RUNNING HANDLER')

    def v2_playbook_on_cleanup_task_start(self, task):
        # type: (Task) -> None
        """Not currently used by Ansible.

        Customization Notes - In this method:
        - You can access Task class methods and attributes like task.get_name() and task.action
        - You can access task-level vars using task.get_vars()
        - You can access extra_vars using task.get_variable_manager().extra_vars
        - The ansible.playbook.task.Task class is defined in lib/ansible/playbook/task.py

        :param Task task: The running task as an object
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('task', task, Task)

        self._task_start(task, prefix='CLEANUP TASK')

    def _task_start(self, task, prefix=None):
        # type: (Task, Union[str, None]) -> None
        """Wrapper for showing task output, based on strategy and ansible.cfg settings,
        like display_ok_hosts.

        Customization Notes - In this method:
        - You can access Task class methods and attributes like task.get_name() and task.action
        - You can access task-level vars using task.get_vars()
        - You can access extra_vars using task.get_variable_manager().extra_vars
        - The ansible.playbook.task.Task class is defined in lib/ansible/playbook/task.py

        :param Task task: The running task instance
        :param str/None prefix: The type of task being performed (TASK, CLEANUP TASK,
        RUNNING HANDLER)

        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('task', task, Task)
            self._validate_input('prefix', prefix, self.UNICODE_TYPE)

        # Cache output prefix for task if provided
        # This is needed to properly display 'RUNNING HANDLER' and similar
        # when hiding skipped/ok task results
        if prefix is not None:
            self._task_type_cache[task._uuid] = prefix

        # Preserve task name, as all vars may not be available for templating
        # when we need it later
        if self._play.strategy in add_internal_fqcns(('free', 'host_pinned')):
            # Explicitly set to None for strategy free/host_pinned to account for any cached
            # task title from a previous non-free play
            self._last_task_name = None
        else:
            self._last_task_name = task.get_name().strip()

            # Display the task banner immediately if we're not doing any filtering based on task
            # result
            if self.get_option('display_skipped_hosts') and self.get_option('display_ok_hosts'):
                self._print_task_banner(task)

    def _print_task_banner(self, task):
        # type: (Task) -> None
        """Show task information, like prefix, task name, and arguments, and optional information,
        based on verbosity level, CLI args, and ansible.cfg settings, like check_mode_markers.

        Customization Notes - In this method:
        - You can access Task class methods and attributes like task.get_name() and task.action
        - You can access task-level vars using task.get_vars()
        - You can access extra_vars using task.get_variable_manager().extra_vars
        - The ansible.playbook.task.Task class is defined in lib/ansible/playbook/task.py

        :param Task task: The running task instance
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)
            # Validate inputs
            self._validate_input('task', task, Task)

        # args can be specified as no_log in several places: in the task or in
        # the argument spec.  We can check whether the task is no_log but the
        # argument spec can't be because that is only run on the target
        # machine, and we haven't run it there yet at this time.
        #
        # So we give people a config option to affect display of the args so
        # that they can secure this if they feel that their stdout is insecure
        # (shoulder surfing, logging stdout straight to a file, etc).
        args = ''
        if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
            args = u', '.join(u'%s=%s' % a for a in task.args.items())
            args = u' %s' % args

        prefix = self._task_type_cache.get(task._uuid, 'TASK')

        # Use cached task name
        task_name = self._last_task_name
        if task_name is None:
            task_name = task.get_name().strip()

        if task.check_mode and self.get_option('check_mode_markers'):
            checkmsg = " [CHECK MODE]"
        else:
            checkmsg = ""
        self._display.banner(u"%s [%s%s]%s" %
                             (prefix, task_name, args, checkmsg))

        if self._display.verbosity >= 2:
            self._print_task_path(task)

        self._last_task_banner = task._uuid

    def v2_runner_on_start(self, host, task):
        # type: (Host, Task) -> None
        """Inform the user a task has started, based on ansible.cfg settings,
        like show_per_host_start. Disabled by default.

        Customization Notes - In this method:
        - You can access Host class methods and attributes like host.get_name() and host.address
        - You can access Task class methods and attributes like task.get_name() and task.action
        - You can access extra-vars using task.get_variable_manager().extra_vars
        - You can access task-level vars using task.get_vars()
        - The ansible.playbook.host.Host class is defined in lib/ansible/inventory/host.py
        - The ansible.playbook.task.Task class is defined in lib/ansible/playbook/task.py

        :param Host host: The target host instance
        :param Task task: The running task instance
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)
            # Validate inputs
            self._validate_input('task', host, Host)
            self._validate_input('task', task, Task)

        if self.get_option('show_per_host_start'):
            self._display.display(" [started %s on %s]" %
                                  (task, host), color=C.COLOR_OK)

    def v2_runner_on_async_poll(self, result):
        # type: (TaskResult) -> None
        """Inform the user that Ansible is polling a target host
        if the task is running in asynchronous mode.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, and result.task_name()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        host = result._host.get_name()
        jid = result._result.get('ansible_job_id')
        started = result._result.get('started')
        finished = result._result.get('finished')
        self._display.display(
            'ASYNC POLL on %s: jid=%s started=%s finished=%s' % (
                host, jid, started, finished),
            color=C.COLOR_DEBUG
        )

    def v2_runner_on_async_ok(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on verbosity level and
        ansible.cfg settings, if an asynchronous task passed on a target host.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_changed()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        host = result._host.get_name()
        jid = result._result.get('ansible_job_id')
        self._display.display("ASYNC OK on %s: jid=%s" %
                              (host, jid), color=C.COLOR_DEBUG)

    def v2_runner_on_async_failed(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on verbosity level and
        ansible.cfg settings, if an asynchronous task failed on a target host.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_failed()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        host = result._host.get_name()

        # Attempt to get the async job ID. If the job does not finish before the
        # async timeout value, the ID may be within the unparsed 'async_result' dict.
        jid = result._result.get('ansible_job_id')
        if not jid and 'async_result' in result._result:
            jid = result._result['async_result'].get('ansible_job_id')
        self._display.display("ASYNC FAILED on %s: jid=%s" %
                              (host, jid), color=C.COLOR_DEBUG)

    def v2_on_file_diff(self, result):
        # type: (TaskResult) -> None
        """Show changes made by tasks with supported modules, like ansible.builtin.file,
        if the --diff arg is passed.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, and result.task_name()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        if result._task.loop and 'results' in result._result:
            for res in result._result['results']:
                if 'diff' in res and res['diff'] and res.get('changed', False):
                    diff = self._get_diff(res['diff'])
                    if diff:
                        if self._last_task_banner != result._task._uuid:
                            self._print_task_banner(result._task)
                        self._display.display(diff)
        elif 'diff' in result._result and result._result['diff'] and result._result.get('changed',
                                                                                        False):
            diff = self._get_diff(result._result['diff'])
            if diff:
                if self._last_task_banner != result._task._uuid:
                    self._print_task_banner(result._task)
                self._display.display(diff)

    def v2_runner_on_ok(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on verbosity level and
        ansible.cfg settings, if a task passed.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_changed()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        print('result', result, type(result))
        print('result._host', result._host, type(result._host))
        print('result._task', result._task, type(result._task))
        print('result._result', result._result, type(result._result))
        print('result._task_fields', result._task_fields, type(result._task_fields))
        print(result._result['msg'])

        host_label = self.host_label(result)

        if isinstance(result._task, TaskInclude):
            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)
            return
        elif result._result.get('changed', False):
            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = "changed: [%s]" % (host_label,)
            color = C.COLOR_CHANGED
        else:
            if not self.get_option('display_ok_hosts'):
                return

            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = "ok: [%s]" % (host_label,)
            color = C.COLOR_OK

        self._handle_warnings(result._result)

        if result._task.loop and 'results' in result._result:
            self._process_items(result)
        else:
            self._clean_results(result._result, result._task.action)

            if self._run_is_verbose(result):
                msg += " => %s" % (self._dump_results(result._result),)
            self._display.display(msg, color=color)

    def v2_runner_on_unreachable(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on ansible.cfg settings,
        if a host is unreachable.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_unreachable()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        if self._last_task_banner != result._task._uuid:
            self._print_task_banner(result._task)

        host_label = self.host_label(result)
        msg = "fatal: [%s]: UNREACHABLE! => %s" % (
            host_label, self._dump_results(result._result))
        self._display.display(msg, color=C.COLOR_UNREACHABLE, stderr=self.get_option(
            'display_failed_stderr'))

        if result._task.ignore_unreachable:
            self._display.display("...ignoring", color=C.COLOR_SKIP)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        # type: (TaskResult, bool) -> None
        """Show result, output, and optional information, based on verbosity level, vars, and
        ansible.cfg settings, if a task failed.

        Customization notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_failed()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :param bool ignore_errors: The value of the ignore_errors vars
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

            # Unfortunately, some methods may call v2_runner_on_failed()
            # with ignore_errors explicitly set to None
            # Set to False if that is the case
            ignore_errors = False if ignore_errors is None else ignore_errors
            self._validate_input('ignore_errors', ignore_errors, bool)

        host_label = self.host_label(result)
        self._clean_results(result._result, result._task.action)

        if self._last_task_banner != result._task._uuid:
            self._print_task_banner(result._task)

        self._handle_exception(
            result._result, use_stderr=self.get_option('display_failed_stderr'))
        self._handle_warnings(result._result)

        if result._task.loop and 'results' in result._result:
            self._process_items(result)

        else:
            if self._display.verbosity < 2 and self.get_option('show_task_path_on_failure'):
                self._print_task_path(result._task)
            msg = "fatal: [%s]: FAILED! => %s" % (
                host_label, self._dump_results(result._result))
            self._display.display(msg, color=C.COLOR_ERROR, stderr=self.get_option(
                'display_failed_stderr'))

        if ignore_errors:
            self._display.display("...ignoring", color=C.COLOR_SKIP)

    def v2_runner_on_skipped(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on verbosity level and
        ansible.cfg settings, if a task is skipped.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_skipped()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        if self.get_option('display_skipped_hosts'):

            self._clean_results(result._result, result._task.action)

            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            if result._task.loop is not None and 'results' in result._result:
                self._process_items(result)

            msg = "skipping: [%s]" % result._host.get_name()
            if self._run_is_verbose(result):
                msg += " => %s" % self._dump_results(result._result)
            self._display.display(msg, color=C.COLOR_SKIP)

    def v2_playbook_on_include(self, included_file):
        # type (IncludedFile) -> None
        """Inform the user a file was included in the play.

        Customization Notes - In this method:
        - You can access IncludedFile class methods like included_file.add_host()
        - The ansible.playbook.included_file.IncludedFile class is defined in
          lib/ansible/playbook/included_file.py

        :param IncludedFile included_file: The included task file instance
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('included_file', included_file, IncludedFile)

        msg = 'included: %s for %s' % (included_file._filename, ", ".join(
            [h.name for h in included_file._hosts]))
        label = self._get_item_label(included_file._vars)
        if label:
            msg += " => (item=%s)" % label
        self._display.display(msg, color=C.COLOR_SKIP)

    def v2_runner_item_on_ok(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on verbosity level and
        ansible.cfg settings, if a task passed using an item from a loop.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_changed()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        host_label = self.host_label(result)
        if isinstance(result._task, TaskInclude):
            return
        elif result._result.get('changed', False):
            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = 'changed'
            color = C.COLOR_CHANGED
        else:
            if not self.get_option('display_ok_hosts'):
                return

            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = 'ok'
            color = C.COLOR_OK

        msg = "%s: [%s] => (item=%s)" % (
            msg, host_label, self._get_item_label(result._result))
        self._clean_results(result._result, result._task.action)
        if self._run_is_verbose(result):
            msg += " => %s" % self._dump_results(result._result)
        self._display.display(msg, color=color)

    def v2_runner_item_on_failed(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on ansible.cfg settings,
        if a task failed using an item from a loop.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_failed()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        if self._last_task_banner != result._task._uuid:
            self._print_task_banner(result._task)

        host_label = self.host_label(result)
        self._clean_results(result._result, result._task.action)
        self._handle_exception(
            result._result, use_stderr=self.get_option('display_failed_stderr'))

        msg = "failed: [%s]" % (host_label,)
        self._handle_warnings(result._result)
        self._display.display(
            msg + " (item=%s) => %s" % (self._get_item_label(result._result), self._dump_results(
                result._result)),
            color=C.COLOR_ERROR,
            stderr=self.get_option('display_failed_stderr')
        )

    def v2_runner_item_on_skipped(self, result):
        # type: (TaskResult) -> None
        """Show result, output, and optional information, based on verbosity level and
        ansible.cfg settings, if a task is skipped using an item from a loop.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, result.task_name(), and result.is_skipped()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        if self.get_option('display_skipped_hosts'):
            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            self._clean_results(result._result, result._task.action)
            msg = "skipping: [%s] => (item=%s) " % (result._host.get_name(), self._get_item_label(
                result._result))
            if self._run_is_verbose(result):
                msg += " => %s" % self._dump_results(result._result)
            self._display.display(msg, color=C.COLOR_SKIP)

    def v2_playbook_on_no_hosts_remaining(self):
        # type() -> None
        """Inform the user that Ansible has finished performing a task,
        which failed on one or more hosts, on the remaining hosts in the queue.

        If any_errors_fatal is true or the max_fail_percentage is met,
        Ansible will continue to run the current task on any remaining hosts,
        but it will not perform any further tasks in the play.

        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

        self._display.banner("NO MORE HOSTS LEFT")

    def v2_runner_retry(self, result):
        # type: (TaskResult) -> None
        """Inform the user that Ansible is retrying a task if retries has a value.

        Customization Notes - In this method:
        - You can access and use other TaskResult class attributes and methods like
          result._task, result._task_fields, and result.task_name()
        - The ansible.executor.task_result.TaskResult class is defined in
          lib/ansible/executor/task_result.py

        :param TaskResult result: The result and output of a task
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('result', result, TaskResult)

        task_name = result.task_name or result._task
        host_label = self.host_label(result)
        msg = "FAILED - RETRYING: [%s]: %s (%d retries left)." % (
            host_label, task_name, result._result['retries'] - result._result['attempts'])
        if self._run_is_verbose(result, verbosity=2):
            msg += "Result was: %s" % self._dump_results(result._result)
        self._display.display(msg, color=C.COLOR_DEBUG)

    def v2_playbook_on_stats(self, stats):
        # type: (AggregateStats) -> None
        """Show a summary of the task results per host, broken down ok, changed,
        unreachable, failed, skipped, rescued, and ignored.

        Customization Notes - In this method:
        - You can access AggregateStats class methods and attributes like stats.summarize()
          and stats.processed
        - The ansible.executor.stats.AggregateStats class is defined
          in lib/ansible/executor/stats.py

        :param AggregateStats stats: The playbook results instance
        :return: None
        """
        if self.DEV_MODE:
            self._display.display('>>> ' + sys._getframe().f_code.co_name,
                                  color=self.TRACE_COLOR)

            # Validate inputs
            self._validate_input('stats', stats, AggregateStats)

        self._display.banner("PLAY RECAP")

        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)

            self._display.display(
                u"%s : %s %s %s %s %s %s %s" % (
                    hostcolor(h, t),
                    colorize(u'ok', t['ok'], C.COLOR_OK),
                    colorize(u'changed', t['changed'], C.COLOR_CHANGED),
                    colorize(u'unreachable',
                             t['unreachable'], C.COLOR_UNREACHABLE),
                    colorize(u'failed', t['failures'], C.COLOR_ERROR),
                    colorize(u'skipped', t['skipped'], C.COLOR_SKIP),
                    colorize(u'rescued', t['rescued'], C.COLOR_OK),
                    colorize(u'ignored', t['ignored'], C.COLOR_WARN),
                ),
                screen_only=True
            )

            self._display.display(
                u"%s : %s %s %s %s %s %s %s" % (
                    hostcolor(h, t, False),
                    colorize(u'ok', t['ok'], None),
                    colorize(u'changed', t['changed'], None),
                    colorize(u'unreachable', t['unreachable'], None),
                    colorize(u'failed', t['failures'], None),
                    colorize(u'skipped', t['skipped'], None),
                    colorize(u'rescued', t['rescued'], None),
                    colorize(u'ignored', t['ignored'], None),
                ),
                log_only=True
            )

        self._display.display("", screen_only=True)

        # print custom stats if required
        if stats.custom and self.get_option('show_custom_stats'):
            self._display.banner("CUSTOM STATS: ")
            # per host
            # TODO: come up with 'pretty format'
            for k in sorted(stats.custom.keys()):
                if k == '_run':
                    continue
                self._display.display('\t%s: %s' % (k, self._dump_results(
                    stats.custom[k], indent=1).replace('\n', '')))

            # print per run custom stats
            if '_run' in stats.custom:
                self._display.display("", screen_only=True)
                self._display.display('\tRUN: %s' % self._dump_results(
                    stats.custom['_run'], indent=1).replace('\n', ''))
            self._display.display("", screen_only=True)

        if context.CLIARGS['check'] and self.get_option('check_mode_markers'):
            self._display.banner("DRY RUN")

    def _validate_input(self, _object_name, _object, _expected_type):
        # type: (str, any, type) -> None
        """Check that inputs are the correct type and not empty.

        :param str _object_name: The name of the argument, object, or variable
        :param any _object: The actual argument, object, or variable
        :param type _expected_type: The expected type for the argument, object, or variable
        :return: None
        """
        try:
            # Validate inputs
            if not isinstance(_object_name, self.UNICODE_TYPE):
                raise TypeError('_object_name arg must be a string.')

            if not isinstance(_expected_type, type):
                raise TypeError('_expected_type arg must be a valid Python data type.')

            # Check that the argument is the correct type and not empty
            if not isinstance(_object, _expected_type):
                raise TypeError('{0} is not type <{1}>.'.format(_object_name, _expected_type))

            if isinstance(_object, self.UNICODE_TYPE) and str(_object).strip() == '':
                raise ValueError('{0} cannot be blank.'.format(_object_name))

            if (isinstance(_object, list) and len(_object) == 0) or (
                    isinstance(_object, dict) and len(_object) == 0):
                raise ValueError('{0} cannot be empty.'.format(_object_name))

        except (TypeError, ValueError) as e:
            # Warn the user that an input is invalid
            _calling_method = inspect.currentframe().f_back
            _msg = '{0} ({1}(), line {2}).'.format(e,
                                                   _calling_method.f_code.co_name,
                                                   _calling_method.f_lineno)
            self._display.error('Invalid input or value:')
            self._display.error(_msg)
            sys.exit(1)

    def _peek_inside(self, _object_name, _object):
        # type: (str, any) -> None
        """Display an object's value and type.

        :param str _object_name: The name of the argument, object, or variable
        :param any _object: The actual argument, object, or variable
        :return: None
        """
        self._display.display('>>> {0} is type {1}: {2}.'.format(
            _object_name, type(_object), _object), 'bright green')

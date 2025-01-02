"""This is an aggregate callback plugin that allows you to trace callback execution.

It interfaces with Ansible's callback mechanism and provides a way to trace
function and method calls by displaying their names during execution,
which can assist with debugging and monitoring the plugin's behavior.

This plugin inherits the same method signatures as the default callback interface,
(located in `ansible/plugins/callback/default.py` in your Python executable's
`site-packages` directory)
allowing it to be used in conjunction with other callback plugins and to respond to
callback events as specified in Ansible's execution flow.

Customization options can be specified in the ansible.cfg file or through environment variables.

The CALLBACK_TYPE of this plugin is `aggregate`, and it will not override any plugins.

Order of operations:
.
├── __init__
├── v2_playbook_on_start
│   ├── v2_playbook_on_vars_prompt (if prompting for facts before running any plays)
│   ├── v2_playbook_on_play_start
│   │   ├── v2_playbook_on_no_hosts_matched (ends current play)
│   │   ├── v2_playbook_on_task_start
│   │   │   └── v2_runner_on_start
│   │   │       ├── v2_runner_on_async_poll (if running in asynchronous mode)
│   │   │       │   ├── v2_runner_on_async_ok
│   │   │       │   └── v2_runner_on_async_failed
│   │   │       ├── v2_on_file_diff (if --diff arg is used)
│   │   │       └── v2_runner_on_ok
│   │   │           or v2_runner_on_unreachable
│   │   │           or v2_runner_on_failed
│   │   │           or v2_runner_on_skipped
│   │   │           ├── v2_playbook_on_include (if a file is included)
│   │   │           ├── v2_playbook_on_no_hosts_remaining (if any_errors_fatal is true
│   │   │           │   or max_fail_percentage is met)
│   │   │           ├── v2_runner_item_on_ok
│   │   │           │   or v2_runner_item_on_failed
│   │   │           │   or v2_runner_item_on_skipped (if running a loop)
│   │   │           └── v2_runner_retry (if retries is set)
│   │   ├── v2_playbook_on_notify
│   │   │   └── v2_playbook_on_handler_task_start
│   │   │       └── v2_runner_on_start
│   │   │           └── ...
│   │   ├── v2_playbook_on_cleanup_task_start
│   │   └── (Repeat v2_playbook_on_task_start until all tasks in the play are completed)
│   └── (Repeat v2_playbook_on_play_start until all plays in the playbook are completed)
└── v2_playbook_on_stats
"""

from functools import wraps
from typing import Any, Callable, Union

from ansible.executor.stats import AggregateStats
from ansible.executor.task_result import TaskResult
from ansible.inventory.host import Host
from ansible.playbook import Playbook
from ansible.playbook.handler import Handler
from ansible.playbook.included_file import IncludedFile
from ansible.playbook.play import Play
from ansible.playbook.task import Task
from ansible.plugins.callback import CallbackBase
from ansible.utils.display import Display

DOCUMENTATION = '''
name: tracer_callback
callback_type: aggregate
short_description: Show the name of the callback function or method after it has been called.
description:
    - This callback plugin allows for tracing of function calls within the Ansible execution environment.
    - It prints out the names of functions or methods as they are invoked, assisting in debugging and understanding the flow of execution.
'''

TRACE = True


def trace_decorator(f: Callable[..., Any]) -> Callable[..., Any]:
    """Show the name of the called function or method for tracing and debugging.

    :param Callable[..., Any] f: The function to be wrapped for tracing.

    :return: A wrapper function that executes f and prints its name.
    :rtype: Callable[..., Any]
    """

    @wraps(f)
    def wrapper(*args, **kwargs) -> Any:
        """Show the name of the function and then call it.

        :param args: Positional arguments for the wrapped function.
        :param kwargs: Keyword arguments for the wrapped function.

        :return: The result of the function or method.
        :rtype: Any
        """
        if TRACE:
            # Display the function name
            print(f'\u001b[1;36m>>> Called {f.__name__}...\u001b[0m')
        # Run the function
        result = f(*args, **kwargs)
        return result

    return wrapper


class CallbackModule(CallbackBase):
    """
    This is an aggregate callback plugin that interfaces with Ansible's
    callback mechanism. It provides a way to trace function and method
    calls by displaying their names during execution, which can assist
    with debugging and monitoring the plugin's behavior.

    This plugin inherits the same method signatures as the default
    callback interface, allowing it to be used in conjunction with other
    callback plugins and to respond to callback events as specified in
    Ansible's execution flow.

    Customization options can be specified in the ansible.cfg file or
    through environment variables.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'tracer_callback'

    @trace_decorator
    def __init__(self, display: Display = None, options: Union[dict, None] = None) -> None:
        """Initializes the callback plugin.

        :param Display display: An instance of the Display class, \
            used for output display, defaults to None.
        :param Union[dict, None] options: Options set for this callback \
            plugin in ansible.cfg or environment variables, \
            defaults to None.

        :return: None
        """
        super(CallbackModule, self).__init__(display, options)

    @trace_decorator
    def v2_playbook_on_start(self, playbook: Playbook) -> None:
        """Runs when a playbook starts.

        :param Playbook playbook: The running playbook instance

        :return: None
        :rtype: None
        """
        # _param_info = f'({type(playbook)}) playbook = {playbook}'
        # self._display.display(_param_info, color='bright yellow')
        # self._display.display(str(playbook.get_plays()), color='bright yellow')
        # self._display.display(str(playbook._file_name), color='bright yellow')
        # self._display.display(str(playbook._entries), color='bright yellow')
        pass

    @trace_decorator
    def v2_playbook_on_vars_prompt(self,
                                   varname: str,
                                   private: bool = True,
                                   prompt: Union[str, None] = None,
                                   encrypt: Union[str, None] = None,
                                   confirm: bool = False,
                                   salt_size: Union[int, None] = None,
                                   salt: Union[str, None] = None,
                                   default: Union[str, None] = None,
                                   unsafe: Union[bool, None] = None) -> None:
        """Runs when a vars_prompt occurs.

        This method allows you to perform additional processing when a \
        vars_prompt occurs, like displaying custom messages. However:

        - You cannot alter the vars_prompt or the play using this method.
        - You cannot access or alter input or facts using this method.

        :param str varname: The name of the fact to be populated
        :param bool private: Do not echo input, defaults to True
        :param Union[str, None] prompt: The prompt to display, \
            defaults to None
        :param Union[str, None] encrypt: The hashing scheme to use, \
            defaults to None
        :param bool confirm: Confirm input, defaults to False
        :param Union[int, None] salt_size: The salt size in bytes, \
            defaults to None
        :param Union[str, None] salt: A salt to use with the hash, \
            defaults to None
        :param Union[str, None] default: The default value of the fact, \
            defaults to None
        :param Union[bool, None] unsafe: Escape input to prevent Jinja \
            injections, defaults to None
        """
        pass

    @trace_decorator
    def v2_playbook_on_play_start(self, play: Play) -> None:
        """Runs when a play starts.

        :param Play play: The current play instance

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_playbook_on_no_hosts_matched(self) -> None:
        """Runs if no nodes targeted by a play are in the inventory.

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_playbook_on_task_start(self, task: Task, is_conditional: bool) -> None:
        """Runs when a task starts.

        :param Task task: The current task instance
        :param bool is_conditional: Not currently used by Ansible

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_runner_on_start(self, host, task: Task) -> None:
        """Run when a task starts running on a host.

        :param Host host: The target host instance
        :param Task task: The current task instance

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_runner_on_async_poll(self, result: TaskResult) -> None:
        """Get details about an unfinished task running in async mode.

        Note: The value of the `poll` keyword in the task determines
        the interval at which polling occurs and this method is run.

        :param result: The parameters of the task and its status.
        :type result: TaskResult

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_runner_on_async_ok(self, result: TaskResult) -> None:
        """Process results of a successful task that ran in async mode.

        :param result: The parameters of the task and its results.
        :type result: TaskResult

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_runner_on_async_failed(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_on_file_diff(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_on_ok(self, result: TaskResult) -> None:
        """Process results of a successful task.

        :param result: The parameters of the task and its results.
        :type result: TaskResult

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_runner_on_unreachable(self, result: TaskResult) -> None:
        """Process results of a task if a target node is unreachable.

        :param result: The parameters of the task and its results.
        :type result: TaskResult

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_runner_on_failed(self, result: TaskResult, ignore_errors: bool = False) -> None:
        """Process results of a failed task.

        Note: The value of 'ignore_errors' tells Ansible whether to
        continue running tasks on the host where this task failed.
        But the 'ignore_errors' directive only works when the task can
        run and returns a value of 'failed'. It does not make Ansible
        ignore undefined variable errors, connection failures, execution
        issues (for example, missing packages), or syntax errors.

        :param result: The parameters of the task and its results.
        :type result: TaskResult
        :param ignore_errors: Whether Ansible should continue \
            running tasks on the host where the task failed.
        :type ignore_errors: bool

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_runner_on_skipped(self, result: TaskResult) -> None:
        """Process results of a skipped task.

        :param result: The parameters of the task and its results.
        :type result: TaskResult

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_playbook_on_include(self, included_file: IncludedFile) -> None:
        pass

    @trace_decorator
    def v2_playbook_on_no_hosts_remaining(self) -> None:
        pass

    @trace_decorator
    def v2_runner_item_on_ok(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_item_on_failed(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_item_on_skipped(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_retry(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_playbook_on_notify(self, handler: Handler, host: Host) -> None:
        """Runs when a handler is notified to run on a target node.

        :param Handler handler: The handler task instance
        :param Host host: The target node instance
        :return: None
        """
        self._display.display(
            f'Handler notified for {host.name}.', color='bright yellow')
        pass

    @trace_decorator
    def v2_playbook_on_handler_task_start(self, task: Task) -> None:
        """Run when a handler starts to access its methods and attributes.

        :param Task task: The current task instance

        :return: None
        :rtype: None
        """
        self._display.display('Handler started.', color='bright yellow')
        pass

    @trace_decorator
    def v2_playbook_on_cleanup_task_start(self, task: Task) -> None:
        """Not currently used by Ansible.

        :param Task task: The current task instance

        :return: None
        :rtype: None
        """
        pass

    @trace_decorator
    def v2_playbook_on_stats(self, stats: AggregateStats) -> None:
        pass

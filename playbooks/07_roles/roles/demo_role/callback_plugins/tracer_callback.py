"""This is an aggregate callback that allows you to trace calls for output.

While it contains all the methods in Ansible's default callback plugin (located in
`ansible/plugins/callback/default.py` in your Python executable's `site-packages` directory),
the CALLBACK_TYPE of this plugin is not `stdout`, and it will not override default STDOUT.
The callbacks will side-by-side; the default plugin will show typical output and this plugin will
show you which function or method was called.

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
│   │   │               ├── v2_runner_on_async_poll (if running in asynchronous mode)
│   │   │               │   ├── v2_runner_on_async_ok
│   │   │               │   └── v2_runner_on_async_failed
│   │   │               ├── v2_on_file_diff (if --diff arg is used)
│   │   │               └── v2_runner_on_ok
│   │   │                   or v2_runner_on_unreachable
│   │   │                   or v2_runner_on_failed
│   │   │                   or v2_runner_on_skipped
│   │   │                   ├── v2_playbook_on_include (if a file is included)
│   │   │                   ├── v2_playbook_on_no_hosts_remaining (if any_errors_fatal is true
│   │   │                   │   or max_fail_percentage is met)
│   │   │                   ├── v2_runner_item_on_ok
│   │   │                   │   or v2_runner_item_on_failed
│   │   │                   │   or v2_runner_item_on_skipped (if running a loop)
│   │   │                   └── v2_runner_retry (if retries is set)
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
short_description: Show which callback function or method was called.
description:
    - Show which callback function or method was called.
'''

TRACE = True


def trace_decorator(f: Callable[..., Any]) -> Callable[..., Any]:
    """Show the name of the called function or method for tracing and debugging.

    :param Callable[..., Any] f: The function to be wrapped

    :return: The result of the wrapped function
    :rtype: Callable[..., Any]
    """
    if TRACE:
        @wraps(f)
        def wrapper(*args, **kwargs) -> Callable[..., Any]:
            """Show the name of the function and then call it.

            :return: The result of the function or method
            :rtype: Callable[..., Any]
            """
            # Display the function name
            print(f'\u001b[1;36m>>> Called {f.__name__}...\u001b[0m')
            # Run the function
            result = f(*args, **kwargs)
            return result

        return wrapper


class CallbackModule(CallbackBase):
    """
    This is an abstract class that displays the name of the function or method called
    alongside the output of the default stdout callback function or method.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'tracer_callback'

    @trace_decorator
    def __init__(self, display: Display = None, options: Union[dict, None] = None) -> None:
        """Initialize the class.

        :param Display display: An instance of the Display class, defaults to None
        :param Union[dict, None] options: Options set for this callback plugin in ansible.cfg \
            or in environment variables, defaults to None

        :return: None
        """
        super(CallbackModule, self).__init__(display, options)

    @trace_decorator
    def v2_playbook_on_start(self, playbook: Playbook) -> None:
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
        pass

    @trace_decorator
    def v2_playbook_on_play_start(self, play: Play) -> None:
        pass

    @trace_decorator
    def v2_playbook_on_no_hosts_matched(self) -> None:
        pass

    @trace_decorator
    def v2_playbook_on_task_start(self, task: Task, is_conditional: bool) -> None:
        pass

    @trace_decorator
    def v2_playbook_on_notify(self, handler: Handler, host: Host) -> None:
        pass

    @trace_decorator
    def v2_playbook_on_handler_task_start(self, task: Task) -> None:
        pass

    @trace_decorator
    def v2_playbook_on_cleanup_task_start(self, task: Task) -> None:
        pass

    @trace_decorator
    def v2_runner_on_start(self, host, task: Task) -> None:
        pass

    @trace_decorator
    def v2_runner_on_async_poll(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_on_async_ok(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_on_async_failed(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_on_file_diff(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_on_ok(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_on_unreachable(self, result: TaskResult) -> None:
        pass

    @trace_decorator
    def v2_runner_on_failed(self, result: TaskResult, ignore_errors: bool = False) -> None:
        pass

    @trace_decorator
    def v2_runner_on_skipped(self, result: TaskResult) -> None:
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
    def v2_playbook_on_stats(self, stats: AggregateStats) -> None:
        pass

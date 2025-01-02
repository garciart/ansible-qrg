# Ansible Quick Reference Guide (QRG)

Brain dump of common tasks and settings that I use with Ansible.

-----

## Getting Started

Link to instructions to [create a Linux Virtual Machine in Windows](/xtra/linux-vm-in-windows.md).

Creating the environment:

```shell
git clone https://github.com/garciart/ansible-qrg.git
python3.12 -B -m venv .venv
source .venv/bin/activate
python -B -m pip install --upgrade pip
python -B -m pip install ansible
python -B -m pip install ansible-lint
```

Deactivating the environment:

```shell
deactivate
```

> **NOTE** - Python normally saves intermediate bytecode in `__pycache__` folders, which can take up space. To prevent this, use the `-B` option when running a Python module or modify your system:
>
> **Linux:**
>
> ```bash
> sed -i -e $'$a\\\nexport PYTHONDONTWRITEBYTECODE=1' ~/.bashrc
> source ~/.bashrc
> ```
>
> **Windows:**
>
> ```bash
> setx PYTHONDONTWRITEBYTECODE=1 /m
> ```

-----

## Playbooks

Link to [reserved keywords list](/xtra/reserved-ansible-keywords.md).

### Playbook Basics

- [vars.yml](/playbooks/01_basics/vars.yml "Initialize different data types used by Ansible")
- [say_hello.yml](/playbooks/01_basics/say_hello.yml "Show a greeting using the debug module")
- [check_for_errors.yml](/playbooks/01_basics/check_for_errors.yml "Check for errors and styling issues")
- [run_multiple_tasks.yml](/playbooks/01_basics/run_multiple_tasks.yml "Run multiple tasks in a play")
- [run_multiple_plays.yml](/playbooks/01_basics/run_multiple_plays.yml "Run multiple plays in a playbook")
- [target_multiple_nodes.yml](/playbooks/01_basics/target_multiple_nodes.yml "Target multiple nodes nodes in a playbook")
- [continue_lines.yml](/playbooks/01_basics/continue_lines.yml "Split long strings to improve readability")
- [group_tasks.yml](/playbooks/01_basics/group_tasks.yml "Group tasks using blocks")
- [handle_errors.yml](/playbooks/01_basics/handle_errors.yml "Handle errors using blocks")

### Variable Basics

- [use_variables.yml](/playbooks/02a_variable_basics/use_variables.yml "Set and show the value of a scalar variable")
- [use_default_values.yml](/playbooks/02a_variable_basics/use_default_values.yml "Use default values if variables are undefined or empty")
- [use_different_types.yml](/playbooks/02a_variable_basics/use_different_types.yml "Set and show different types of scalar variables")
- [use_lists.yml](/playbooks/02a_variable_basics/use_lists.yml "Set and show lists of variables")
- [use_dicts.yml](/playbooks/02a_variable_basics/use_dicts.yml "Set and show dictionaries of variables")
- [use_list_dicts.yml](/playbooks/02a_variable_basics/use_list_dicts.yml "Set and show a list of dictionaries")
- [get_var_type.yml](/playbooks/02a_variable_basics/get_var_type.yml "Show variables and their types")
- [use_return_values.yml](/playbooks/02a_variable_basics/use_return_values.yml "Get and show the return values of a task")
- [use_special_vars.yml](/playbooks/02a_variable_basics/use_special_vars.yml "Get and show special variables and facts")
- [use_cmd_line_vars.yml](/playbooks/02a_variable_basics/use_cmd_line_vars.yml "Get and show command line variables")
- [demo_var_scope.yml](/playbooks/02a_variable_basics/demo_var_scope.yml "Demonstrate variable scope in a playbook")
- [set_facts.yml](/playbooks/02a_variable_basics/set_facts.yml "Set a fact usable by the plays and tasks in a playbook")
- [demo_var_precedence.yml](/playbooks/02a_variable_basics/demo_var_precedence.yml "Demonstrate variable precedence in a play")

### Working with Variables

- [format_variables.yml](/playbooks/02b_variable_output/format_variables.yml "Format output using filters")
- [transform_variables.yml](/playbooks/02b_variable_output/transform_variables.yml "Transform variables using filters")
- [concat_variables.yml](/playbooks/02b_variable_output/concat_variables.yml "Concatenate different types of variables")
- [slice_variables.yml](/playbooks/02b_variable_output/slice_variables.yml "Show parts of a variable using slicing")
- [use_special_chars.yml](/playbooks/02b_variable_output/use_special_chars.yml "Use reserved and special characters")
- [cast_variables.yml](/playbooks/02b_variable_output/cast_variables.yml "Cast variables to other types")
- [convert_data_strings.yml](/playbooks/02b_variable_output/convert_data_strings.yml "Convert data strings to structures")
- [split_strings.yml](/playbooks/02b_variable_output/split_strings.yml "Split strings into lists of items")
- [find_replace_text.yml](/playbooks/02b_variable_output/find_replace_text.yml "Find text and replace text")

### Working with Lists

- [find_in_lists.yml](find_in_lists.yml "Find items in a list")
- [add_to_lists.yml](add_to_lists.yml "Add items to a list")
- [update_lists.yml](update_lists.yml "Update items in a list")
- [remove_from_lists.yml](remove_from_lists.yml "Remove items from a list")
- [join_lists.yml](join_lists.yml "Join lists into a single list")
- [split_lists.yml](split_lists.yml "Split a list into multiple lists")
- [copy_lists.yml](copy_lists.yml "Copy lists fully or in part")
- [get_list_diff.yml](get_list_diff.yml "Get the differences between lists")
- [list_to_dict.yml](list_to_dict.yml "Convert a list to a dictionary")

### Working with Dictionaries

- [find_in_dicts.yml](find_in_dicts.yml "Find items in a dictionary")
- [get_dict_keys.yml](get_dict_keys.yml "Get a list of keys in a dictionary")
- [get_dict_values.yml](get_dict_values.yml "Get a list of values in a dictionary")
- [add_to_dicts.yml](add_to_dicts.yml "Add items to a dictionary")
- [update_dicts.yml](update_dicts.yml "Update items in a dictionary")
- [remove_from_dicts.yml](remove_from_dicts.yml "Remove items from a dictionary")
- [join_dicts.yml](join_dicts.yml "Join dictionaries into a single dictionary")
- [split_dicts.yml](split_dicts.yml "Split a dictionary into multiple dictionaries")
- [copy_dicts.yml](copy_dicts.yml "Copy dictionaries fully or in part")
- [get_dict_diff.yml](get_dict_diff.yml "Get the differences between dictionaries")
- [dict_to_list.yml](dict_to_list.yml "Convert a dictionary to a list")

### Conditions

- [perform_math.yml](/playbooks/03_conditions/perform_math.yml "Perform calculations using constants and variables")
- [demo_order_of_ops.yml](/playbooks/03_conditions/demo_order_of_ops.yml "Demonstrate the order of operations")
- [check_equality.yml](/playbooks/03_conditions/check_equality.yml "Check if values are equal")
- [test_variables.yml](/playbooks/03_conditions/test_variables.yml "Test if an expression is true or false")
- [use_conditionals.yml](/playbooks/03_conditions/use_conditionals.yml "Check for a condition in a task")
- [combine_conditions.yml](/playbooks/03_conditions/combine_conditions.yml "Check for multiple conditions in a task")
- [validate_vars.yml](/playbooks/03_conditions/validate_vars.yml "Check if a variable is undefined, null, or empty")
- [test_strings.yml](/playbooks/03_conditions/test_strings.yml "Test if a string starts with, contains, or ends with value")

### Debugging

- [use_verbosity.yml](/playbooks/04_debugging/use_verbosity.yml "Limit output using the verbosity parameter")
- [pause_plays.yml](/playbooks/04_debugging/pause_plays.yml "Pause a play for time or wait for input")
- [get_user_input.yml](/playbooks/04_debugging/get_user_input.yml "Get and show user input")
- [profile_tasks.yml](/playbooks/04_debugging/profile_tasks.yml "Get the time it takes to run tasks")
- [log_output.yml](/playbooks/04_debugging/log_output.yml "Log the output of a play")
- [run_select_tasks.yml](/playbooks/04_debugging/run_select_tasks.yml "Run or skip tasks based on command line arguments")
- [debug_plays.yml](/playbooks/04_debugging/debug_plays.yml "Debug a play using the Ansible debugger")
- [end_plays.yml](/playbooks/04_debugging/end_plays.yml "End a play is a condition is met")

### Loops

- [loop_numbers.yml](/playbooks/05_loops/loop_numbers.yml "Loop over a range of numbers in reverse")
- [loop_lists.yml](/playbooks/05_loops/loop_lists.yml "Loop over a list of items")
- [loop_dicts.yml](/playbooks/05_loops/loop_dicts.yml "Loop over a dictionary")
- [loop_list_dicts.yml](/playbooks/05_loops/loop_list_dicts.yml "Loop over a list of dictionaries")
- [loop_nested.yml](/playbooks/05_loops/loop_nested.yml "Loop over nested lists")
- [loop_until.yml](/playbooks/05_loops/loop_until.yml "Loop until a condition is met")
- [show_loop_index.yml](/playbooks/05_loops/show_loop_index.yml "Show loop index with loop_control")

### File Operations

- [include_vars.yml](/playbooks/06_file_operations/include_vars.yml "Use variables from external files")
- [import_tasks.yml](/playbooks/06_file_operations/import_tasks.yml "Import and run tasks from external YAML files")
- [include_tasks.yml](/playbooks/06_file_operations/include_tasks.yml "Include and run tasks from external YAML files")
- [fizzbuzz.yml](/playbooks/06_file_operations/fizzbuzz.yml "Run FizzBuzz using include_tasks")
- [use_templates.yml](/playbooks/06_file_operations/use_templates.yml "Use templates to create formatted files")
- [import_playbook.yml](/playbooks/06_file_operations/import_playbook.yml "Import and run another playbook")
- [create_directory.yml](/playbooks/06_file_operations/create_directory.yml "Create a subdirectory in the current working directory")
- [create_files.yml](/playbooks/06_file_operations/create_files.yml "Create files")
- [read_files.yml](/playbooks/06_file_operations/read_files.yml "Read the contents of files")
- [add_content.yml](/playbooks/06_file_operations/add_content.yml "Add content to files")
- [find_content.yml](/playbooks/06_file_operations/find_content.yml "Find and show content from files")
- [replace_content.yml](/playbooks/06_file_operations/replace_content.yml "Edit content in files")
- [remove_content.yml](/playbooks/06_file_operations/remove_content.yml "Remove content from files")
- [copy_files.yml](/playbooks/06_file_operations/copy_files.yml "Copy files to another file or location")
- [delete_files.yml](/playbooks/06_file_operations/delete_files.yml "Delete files")
- [delete_directory.yml](/playbooks/06_file_operations/delete_directory.yml "Delete directory")

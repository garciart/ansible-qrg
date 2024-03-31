# A4P

Repository for a4p source code.

Link to instructions to [create a Linux Virtual Machine in Windows](/linux-in-windows.md).

Link to [reserved keywords list](/reserved_keywords.md).

-----

## Playbooks

### Playbook Basics

- [vars.yml](/playbooks/01_basics/vars.yml "Initialize different data types used by Ansible")
- [say_hello.yml](/playbooks/01_basics/say_hello.yml "Show a greeting using the debug module")
- [check_for_errors.yml](/playbooks/01_basics/check_for_errors.yml "Check for errors and styling issues")
- [run_multiple_tasks.yml](/playbooks/01_basics/run_multiple_tasks.yml "Run multiple tasks in a play")
- [run_multiple_plays.yml](/playbooks/01_basics/run_multiple_plays.yml "Run multiple plays in a playbook")
- [target_multiple_nodes.yml](/playbooks/01_basics/target_multiple_nodes.yml "Target multiple nodes nodes in a playbook")
- [split_strings.yml](/playbooks/01_basics/split_strings.yml "Split long strings to improve readability")
- [group_tasks.yml](/playbooks/01_basics/group_tasks.yml "Group tasks using blocks")
- [handle_errors.yml](/playbooks/01_basics/handle_errors.yml "Handle errors using blocks")

### Variable Basics

- [use_variables.yml](/playbooks/02_variables/use_variables.yml "Set and show the value of a scalar variable")
- [use_default_values.yml](/playbooks/02_variables/use_default_values.yml "Use default values if variables are undefined or empty")
- [use_multiple_vars.yml](/playbooks/02_variables/use_multiple_vars.yml "Set and show different types of scalar variables")
- [use_lists.yml](/playbooks/02_variables/use_lists.yml "Set and show lists of variables")
- [use_dicts.yml](/playbooks/02_variables/use_dicts.yml "Set and show dictionaries of variables")
- [use_list_dicts.yml](/playbooks/02_variables/use_list_dicts.yml "Set and show a list of dictionaries")
- [get_var_type.yml](/playbooks/02_variables/get_var_type.yml "Show variables and their types")
- [use_return_values.yml](/playbooks/02_variables/use_return_values.yml "Get and show the return values of a task")
- [use_special_vars.yml](/playbooks/02_variables/use_special_vars.yml "Get and show special variables and facts")
- [set_facts.yml](/playbooks/02_variables/set_facts.yml "Set a fact usable by the plays and tasks in a playbook")
- [use_cmd_line_vars.yml](/playbooks/02_variables/use_cmd_line_vars.yml "Get and show command line variables")
- [demo_var_scope.yml](/playbooks/02_variables/demo_var_scope.yml "Demonstrate variable scope in a playbook")
- [demo_var_precedence.yml](/playbooks/02_variables/demo_var_precedence.yml "Demonstrate variable precedence in a play")
- [format_variables.yml](/playbooks/02_variables/format_variables.yml "Format output using filters")
- [transform_variables.yml](/playbooks/02_variables/transform_variables.yml "Transform variables using filters")
- [concat_variables.yml](/playbooks/02_variables/concat_variables.yml "Concatenate different types of variables")
- [slice_variables.yml](/playbooks/02_variables/slice_variables.yml "Show parts of a variable using slicing")

### Conditions

- [perform_math.yml](/playbooks/03_conditions/perform_math.yml "Perform calculations using constants and variables")
- [demo_order_of_ops.yml](/playbooks/03_conditions/demo_order_of_ops.yml "Demonstrate the order of operations")
- [cast_variables.yml](/playbooks/03_conditions/cast_variables.yml "Cast variables to other types")
- [check_equality.yml](/playbooks/03_conditions/check_equality.yml "Check if values are equal")
- [test_variables.yml](/playbooks/03_conditions/test_variables.yml "Test if an expression is true or false")
- [use_conditionals.yml](/playbooks/03_conditions/use_conditionals.yml "Check for a condition in a task")
- [combine_conditions.yml](/playbooks/03_conditions/combine_conditions.yml "Check for multiple conditions in a task")
- [validate_vars.yml](/playbooks/03_conditions/validate_vars.yml "Check if a variable is undefined, null, or empty")

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

- [loop_numbers](/playbooks/05_loops/loop_numbers.yml "Loop over a range of numbers in reverse")
- [loop_lists](/playbooks/05_loops/loop_lists.yml "Loop over a list of items")
- [loop_dicts](/playbooks/05_loops/loop_dicts.yml "Loop over a dictionary")
- [loop_list_dicts](/playbooks/05_loops/loop_list_dicts.yml "Loop over a list of dictionaries")
- [loop_nested](/playbooks/05_loops/loop_nested.yml "Loop over nested lists")

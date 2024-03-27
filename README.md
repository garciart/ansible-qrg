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

- [use_a_variable.yml](/playbooks/02_variables/use_a_variable.yml "Set and show the value of a scalar variable")
- [use_default_values.yml](/playbooks/02_variables/use_default_values.yml "Use default values if variables are undefined or empty")
- [use_multiple_vars.yml](/playbooks/02_variables/use_multiple_vars.yml "Set and show different types of scalar variables")
- [use_lists.yml](/playbooks/02_variables/use_lists.yml "Set and show lists of variables")
- [use_dicts.yml](/playbooks/02_variables/use_dicts.yml "Set and show dictionaries of variables")
- [get_var_type.yml](/playbooks/02_variables/get_var_type.yml)
- [use_return_values.yml](/playbooks/02_variables/use_return_values.yml)
- [use_special_vars.yml](/playbooks/02_variables/use_special_vars.yml)
- [set_facts.yml](/playbooks/02_variables/set_facts.yml)
- [use_cmd_line_vars.yml](/playbooks/02_variables/use_cmd_line_vars.yml)
- [demo_var_scope.yml](/playbooks/02_variables/demo_var_scope.yml "Demonstrate variable scope in a playbook")
- [demo_var_precedence.yml](/playbooks/02_variables/demo_var_precedence.yml "Demonstrate variable precedence in a play")
- [format_variables.yml](/playbooks/02_variables/format_variables.yml)
- [transform_variables.yml](/playbooks/02_variables/transform_variables.yml)
- [concat_variables.yml](/playbooks/02_variables/concat_variables.yml)
- [slice_variables.yml](/playbooks/02_variables/slice_variables.yml)

### Math and Conditions

- [perform_math.yml](/playbooks/03_math_conditions/perform_math.yml)
- [demo_order_of_ops.yml](/playbooks/03_math_conditions/demo_order_of_ops.yml)
- [cast_variables.yml](/playbooks/03_math_conditions/cast_variables.yml)
- [check_equality.yml](/playbooks/03_math_conditions/check_equality.yml)
- [test_variables.yml](/playbooks/03_math_conditions/test_variables.yml)
- [use_conditionals.yml](/playbooks/03_math_conditions/use_conditionals.yml)
- [combine_conditions.yml](/playbooks/03_math_conditions/combine_conditions.yml)
- [check_null_or_empty.yml](/playbooks/03_math_conditions/check_null_or_empty.yml)

### Debugging

- [use_verbosity.yml](/playbooks/04_debugging/use_verbosity.yml)
- [pause_a_play.yml](/playbooks/04_debugging/pause_a_play.yml)
- [get_user_input.yml](/playbooks/04_debugging/get_user_input.yml)
- [profile_tasks.yml](/playbooks/04_debugging/profile_tasks.yml)
- [log_output.yml](/playbooks/04_debugging/log_output.yml)
- [skip_tasks.yml](/playbooks/04_debugging/skip_tasks.yml)
- [debug_plays.yml](/playbooks/04_debugging/debug_plays.yml)

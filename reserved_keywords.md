# Reserved Keywords

The following words have special meanings in Ansible, Jinja2, YAML, and Python, and you should not use them for variable names. For example, if you name a variable `task`, Ansible may attempt to process its value as a task. causing the play to fail.

These lists are not all inclusive and are subject to change.

-----

## Ansible Keywords

(ref: Playbook Keywords at <https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html>)

|                  |                |                     |             |                    |
|------------------|----------------|---------------------|-------------|--------------------|
| action           | debugger       | ignore_unreachable  | register    | vars               |
| always           | delay          | local_action        | remote_user | vars_files         |
| any_errors_fatal | delegate_facts | loop                | rescue      | vars_prompt        |
| args             | delegate_to    | loop_control        | retries     | when               |
| async            | diff           | max_fail_percentage | role        | with_cartesian     |
| become           | environment    | module_defaults     | roles       | with_dict          |
| become_exe       | fact_path      | name                | run_once    | with_flattened     |
| become_flags     | failed_when    | no_log              | serial      | with_indexed_items |
| become_method    | force_handlers | notify              | strategy    | with_items         |
| become_user      | gather_facts   | order               | tags        | with_list          |
| block            | gather_subset  | play                | task        | with_nested        |
| changed_when     | gather_timeout | poll                | tasks       | with_random_choice |
| check_mode       | handlers       | port                | throttle    | with_sequence      |
| collections      | hosts          | post_tasks          | timeout     | with_subelements   |
| connection       | ignore_errors  | pre_tasks           | until       | with_together      |

-----

## YAML Keywords

(ref: YAML Ain’t Markup Language (YAML) at <https://yaml.org/spec/1.2.2/>)

`true`, `false`, `yes`, `no`, `on`, `off`, and `null` have special meanings in YAML and should not be used for variable names. In addition, while data types, such as `bool`, `float`, `int`, `map`, `nan`, `seq`, and `str`, are not reserved, you should not use them for variable names either.

-----

## Jinja2 Keywords

(ref: Template Designer Documentation at <https://jinja.palletsprojects.com/en/3.1.x/templates/>)

|       |           |          |         |           |
|-------|-----------|----------|---------|-----------|
| and   | endblock  | endraw   | in      | pluralize |
| block | endcall   | endtrans | include | print     |
| call  | endfilter | extends  | is      | raw       |
| cycle | endfor    | filter   | macro   | recursive |
| elif  | endif     | for      | not     | set       |
| else  | endmacro  | if       | or      | trans     |

-----

## Jinja2 Builtin Filters

(ref: List of Builtin Filters at <https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters>)

|                |             |            |            |           |
|----------------|-------------|------------|------------|-----------|
| abs            | forceescape | map        | select     | unique    |
| attr           | format      | max        | selectattr | upper     |
| batch          | groupby     | min        | slice      | urlencode |
| capitalize     | indent      | pprint     | sort       | urlize    |
| center         | int         | random     | string     | wordcount |
| default        | items       | reject     | striptags  | wordwrap  |
| dictsort       | join        | rejectattr | sum        | xmlattr   |
| escape         | last        | replace    | title      |           |
| filesizeformat | length      | reverse    | tojson     |           |
| first          | list        | round      | trim       |           |
| float          | lower       | safe       | truncate   |           |

-----

## Jinja2 Buitin Tests

(ref: List of Builtin Tests at <https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-tests>)

|             |        |          |         |           |
|-------------|--------|----------|---------|-----------|
| boolean     | even   | in       | mapping | sequence  |
| callable    | false  | integer  | ne      | string    |
| defined     | filter | iterable | none    | test      |
| divisibleby | float  | le       | number  | true      |
| eq          | ge     | lower    | odd     | undefined |
| escaped     | gt     | lt       | sameas  | upper     |

-----

## Ansible-Specific Jinja2 Filters

(ref: Using filters to manipulate data at <https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html> and <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/filter>)

|             |           |               |                      |                 |
|-------------|-----------|---------------|----------------------|-----------------|
| b64decode   | failed    | mandatory     | search               | to_uuid         |
| b64encode   | from_json | match         | shuffle              | to_yaml         |
| basename    | from_yaml | password_hash | skipped              | union           |
| changed     | hash      | pow           | splitext             | version_compare |
| checksum    | intersect | quote         | success              | win_basename    |
| combine     | ipaddr    | realpath      | symmetric_difference | win_dirname     |
| comment     | ipv4      | regex_escape  | ternary              | win_splitdrive  |
| difference  | ipv6      | regex_replace | to_json              |                 |
| dirname     | isnan     | relpath       | to_nice_json         |                 |
| expand_user | log       | root          | to_nice_yaml         |                 |

-----

## Python Keywords

(ref: Keywords at <https://docs.python.org/3/reference/lexical_analysis.html#keywords>)

|        |          |         |          |        |
|--------|----------|---------|----------|--------|
| and    | continue | finally | is       | raise  |
| as     | def      | for     | lambda   | return |
| assert | del      | from    | none     | true   |
| async  | elif     | global  | nonlocal | try    |
| await  | else     | if      | not      | while  |
| break  | except   | import  | or       | with   |
| class  | false    | in      | pass     | yield  |

-----

## Python Dictionary Attributes and Methods

(ref: Referencing key:value dictionary variables at <https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#referencing-key-value-dictionary-variables>)

|                   |                     |            |            |                             |
|-------------------|---------------------|------------|------------|-----------------------------|
| add               | extend              | is_integer | partition  | strip                       |
| append            | find                | islower    | pop        | swapcase                    |
| as_integer_ratio  | format              | isnumeric  | popitem    | symmetric_difference        |
| bit_length        | fromhex             | isspace    | real       | symmetric_difference_update |
| capitalize        | fromkeys            | issubset   | remove     | title                       |
| center            | get                 | issuperset | replace    | translate                   |
| clear             | has_key             | istitle    | reverse    | union                       |
| conjugate         | hex                 | isupper    | rfind      | update                      |
| copy              | imag                | items      | rindex     | upper                       |
| count             | index               | iteritems  | rjust      | values                      |
| decode            | insert              | iterkeys   | rpartition | viewitems                   |
| denominator       | intersection        | itervalues | rsplit     | viewkeys                    |
| difference        | intersection_update | join       | rstrip     | viewvalues                  |
| difference_update | isalnum             | keys       | setdefault | zfill                       |
| discard           | isalpha             | ljust      | sort       |                             |
| encode            | isdecimal           | lower      | split      |                             |
| endswith          | isdigit             | lstrip     | splitlines |                             |
| expandtabs        | isdisjoint          | numerator  | startswith |                             |

## Other

- You should not use module names, such as `debug`, `set_fact`, `user`. If you want to use a module name for clarity, prepend it with descriptive prefix, such as `target_user`, etc.
- You should not use variable names that are the same as operating system commands or reserved keywords, such as `hostname`, `ifconfig`, `print`, etc. If you want to use a reserved word for clarity, prepend it with descriptive prefix, such as `target_hostname`, etc.

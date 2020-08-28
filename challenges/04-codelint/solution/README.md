# Code Linting & Formatting Challenge Solution

## Introduction

This exercise requires you to fix a repository containing a few Python files and YAML Ansible playbooks. These files have various syntax and formatting errors in them and you need to fix all of them in order for the tests to pass.

The focus here is on using the `black, flake8, yamllint, and ansible-lint` tools one by one to parse the files in the `code` subfolder.

A `Makefile` is provided which runs these tools with the correct parameters for you and it also can create a Python virtualenv with the correct packages installed should you need one (highly recommended).

## Code formatting - black

Let's start with formatting all of the python code in the `code` folder. Run the `make black` command and check what it reports.

```
(venv) .../challenges/codelint/solution (master *%) make black
black --check --diff code
--- code/custom_rules/CapitalNamesRule.py   2020-08-14 18:53:19.948544 +0000
+++ code/custom_rules/CapitalNamesRule.py   2020-08-14 18:54:40.952926 +0000
@@ -1,12 +1,16 @@
 from ansiblelint import AnsibleLintRule
+
+
 class CapitalNamesRule(AnsibleLintRule):
     id = "289"
-    shortdesc="All task names should be capitalized"
-    description='Using all uppercase names creates uniformity and improves readability'
-    severity='LOW'
-    tags= ['formatting", "readability']
+    shortdesc = "All task names should be capitalized"
+    description = (
+        "Using all uppercase names creates uniformity and improves readability"
+    )
+    severity = "LOW"
+    tags = ['formatting", "readability']
     version_added = "v4.0.0"
 
     def matchtask(self, file, task):
         if task.get("name"):
             return task.get("name") != task.get("name").upper()
would reformat code/custom_rules/CapitalNamesRule.py
error: cannot format code/file_copy.py: Cannot parse: 119:24:         if pull is False
Oh no! 💥 💔 💥
1 file would be reformatted, 1 file would fail to reformat.
make: *** [Makefile:20: black] Error 123
```

It says it would reformat one file (`CapitalNamesRule.py`), but that `file_copy.py` fails due to a code error. It's complaining about line 119, so open this file and check what's wrong. It turns out there's a missing `:` after the `if` statement! Fix it, save the file, and run `make black` again.

```
<LONG DIFF OUTPUT SNIPPED>
Oh no! 💥 💔 💥
2 files would be reformatted.
make: *** [Makefile:20: black] Error 1
```

It now shows you the differences ("diffs") between the source files and its reformatting output. The Makefile uses the `--check --diff` flags so no changes are actually made. Go ahead and let the formatter save the changes to both files by running the `black code` command (it will scan for all python files in the `code` folder).

```
(venv) .../challenges/codelint/solution (master *%) black code
reformatted /x/dev/ntc/projects/enablement-catalog/challenges/codelint/solution/code/custom_rules/CapitalNamesRule.py
reformatted /x/dev/ntc/projects/enablement-catalog/challenges/codelint/solution/code/file_copy.py
All done! ✨ 🍰 ✨
2 files reformatted.
```

You can double check now that `make black` succeeds, reporting that no changes are needed.

## Code linting - flake8

Up next, run the `make flake8` command. It reports the following issues.

```
(venv) .../challenges/codelint/solution (master *%) make flake8 
flake8 --ignore E501 code
code/file_copy.py:4:1: F401 'pynxos.errors.CLIError' imported but unused
code/file_copy.py:134:20: F821 undefined name 'hostnam'
make: *** [Makefile:23: flake8] Error 1
```

Open the `code/file_copy.py` file in your editor and look at line 4. If you do a quick search in the file, it does indeed look like `CLIError` is not used anywhere, so you can remove it from the `import` statement.

The second error points at line 134. If you inspect it, you will notice that it looks like a typo, the `e` at the end of `hostname` is missing. Fix the typo and save the file.

Now you can run the linter again and it should all be good - in this case no output means no errors.

```
make flake8 
flake8 --ignore E501 code
```

## YAML Linting

With the python files fixed, it's time to look at the YAML code included in the form of Ansible playbooks. Run the `make yamllint` command and check the output.

```
(venv) .../challenges/codelint/solution (master *%) make yamllint 
yamllint -s code/*.yml
code/pb_csv_report.yml
  3:3       error    wrong indentation: expected 0 but found 2  (indentation)
  6:19      warning  truthy value should be one of [false, true]  (truthy)
  19:19     warning  truthy value should be one of [false, true]  (truthy)
  36:19     warning  truthy value should be one of [false, true]  (truthy)
  52:19     warning  truthy value should be one of [false, true]  (truthy)
  68:19     warning  truthy value should be one of [false, true]  (truthy)
  82:1      error    too many blank lines (3 > 2)  (empty-lines)
  86:19     warning  truthy value should be one of [false, true]  (truthy)
  91:9      error    wrong indentation: expected 6 but found 8  (indentation)

code/pb_snmp_config.yml
  1:1       error    too many blank lines (1 > 0)  (empty-lines)
  2:3       warning  comment not indented like content  (comments-indentation)
  3:1       warning  missing document start "---"  (document-start)
  3:81      error    line too long (101 > 80 characters)  (line-length)
  8:20      error    too many spaces before colon  (colons)
  13:7      error    duplication of key "ios" in mapping  (key-duplicates)

make: *** [Makefile:27: yamllint] Error 1
```

### Fixing pb_csv_report.yml

Open `code/pb_csv_report.yml` in your editor and fix the errors. You will notice that all the plays are indented when they should not be (at 2 spaces instead of 0). In most modern code editors you should be able to select all relevant lines (from 3 to 101) and reduce their indentation by using a keyboard shortcut (e.g. `Ctrl+[` in VSCode).

While YAML accepts `no` instead of `false`, `yamllint` gives you a warning about it. To get rid of it, you can replace all instances of `no` with `false`. Also there's one too many blank lines that you should fix on line 82.

Finally, there's one more indentation problem starting at line 91 (all the way to 101). You will notice the tasks are indented 4 spaces instead of 2.

### Fixing pb_snmp_config.yml

Open `code/pb_snmp_config.yml` in your editor and fix the errors. 

Align the comment indentation with the entry following it. The play name is a bit too wordy, so shorten it a bit so it fits in the 80 characters line length.

On line 8, the extra space before the colon is a problem, as is the fact that the `ios` key is duplicated on line 13. On closer inspection it should really read `junos`.

At the very start, we're missing the YAML `---` document start marker so add that in and you should be done!

Run the `make yamllint` command again and check the output. No news is good news.

```
(venv) .../challenges/codelint/solution (master *%) make yamllint 
yamllint -s code/*.yml
```

## Ansible Linting

The final check is to run `ansible-lint` by using the `make ansible-lint` command.

```
(venv) .../challenges/codelint/solution (master *%) make ansible-lint 
ansible-lint -Rr code/custom_rules code/pb*.yml
[502] All tasks should be named
code/pb_csv_report.yml:11
Task/Handler: file path=./docs/csv/ state=directory __line__=11 __file__=code/pb_csv_report.yml

[502] All tasks should be named
code/pb_csv_report.yml:57
Task/Handler: eos_facts 

[289] All task names should be capitalized
code/pb_csv_report.yml:90
Task/Handler: create master csv report

[289] All task names should be capitalized
code/pb_csv_report.yml:95
Task/Handler: insert columns into csv report

[289] All task names should be capitalized
code/pb_snmp_config.yml:19
Task/Handler: Task 1 - ensure snmp commands exist on ios and vmx devices

make: *** [Makefile:31: ansible-lint] Error 2
```

Two of the tasks in `code/pb_csv_report.yml` are missing names so add in something descriptive!

The repository has a custom rule for `ansible-lint` that asks it to check that task names are all uppercase. It has detected a few instaces where it is not the case, so capitalize the names on the reported line numbers.

Once all issues are fixed, run the `make ansible-lint` command - if it reports nothing, success!

```
(venv) .../challenges/codelint/solution (master *%) make ansible-lint 
ansible-lint -Rr code/custom_rules code/pb*.yml
```

## One final check

To finish the challenge, run **all** of the checks again by using the `make all` command. It should not report any issues.

```
(venv) .../challenges/codelint/solution (master *%) make all
black --check --diff code
All done! ✨ 🍰 ✨
2 files would be left unchanged.
flake8 --ignore E501 code
yamllint -s code/*.yml
ansible-lint -Rr code/custom_rules code/pb*.yml
```

Congratulations, you are done!


## CONFIDENTIAL

### This material is owned by Network to Code, LLC.

**You are NOT permitted to distribute the material, content, slides, labs, and other related material outside of the program.**

Copyright 2020, Network to Code, LLC.

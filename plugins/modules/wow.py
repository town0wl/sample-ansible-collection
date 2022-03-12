#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: wow

short_description: Create file with specified content. Idempotent.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Create file with specified content. Idempotent.

options:
    path:
        description: Path for created file.
        required: true
        type: str
    content:
        description: Content of created file.
        required: true
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_own_namespace.test_neto.wow_module

author:
    - My Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create new file
- name: Create new file
  my_own_namespace.test_neto.wow:
    path: /path/to/new/file
    content: "some text"

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
message:
    description: Result status of file creation
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os
# import os.makedirs
import errno


def check_file_content(path,content):
    with open(path,'r') as f:
        filetext = f.read()
    return bool(filetext==content)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message='Just begin, nothing done yet',
        path = ''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result["path"] = module.params["path"]

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        try:
            if check_file_content(module.params["path"],module.params["content"]):
                result["message"] = "File already exists and has the same content"
            else:
                result["changed"] = True
                result["message"] = "File exists and would be changed"
        except IOError:
            result["changed"] = True
            result["message"] = "File does not exist and would be created"

        module.exit_json(**result)

    try:
        if check_file_content(module.params["path"],module.params["content"]):
            result["message"] = "File already exists and has the same content"
        else:
            with open(module.params["path"],'w') as f:
                f.write(module.params["content"])
            result["changed"] = True
            result["message"] = "File was changed"
    except IOError:
        if not os.path.exists(os.path.dirname(module.params["path"])):
            try:
                os.makedirs(os.path.dirname(module.params["path"]))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(module.params["path"],'w') as f:
            f.write(module.params["content"])
        result["changed"] = True
        result["message"] = "File was created"

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

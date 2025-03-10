import datetime

import requests

from ansible.plugins.action import ActionBase
from ansible.parsing.yaml.objects import AnsibleUnicode

from ansible_collections.epfl_si.actions.plugins.module_utils.subactions import AnsibleActions
from ansible_collections.epfl_si.actions.plugins.module_utils.ansible_api import AnsibleResults
from ansible_collections.epfl_si.quay.plugins.module_utils.quay_actions import QuayActionMixin, returns_none_on_404

class ActionModule (ActionBase, QuayActionMixin):
    """Set up or delete a permission for a robot account.

    See operation details and Ansible-level documentation in
    ../modules/robot_account_permission.py which only exists for documentation
    purposes.
    """
    @AnsibleActions.run_method
    def run (self, args, ansible_api):
        self.args = args
        self.ansible = ansible_api  # For the mixin's `quay_hostname` and `quay_bearer_token`

        self.organization = args['organization']
        self.repository_name = args['repository_name']
        self.robot_account_name = args['robot_account_name']

        self.result = AnsibleResults.empty()
        self.perform_changes(args.get('state', 'present'))
        return self.result

    @property
    def moniker (self):
        return f"permissions of {self.robot_account_name} on {self.quay_hostname}/{self.organization}/{self.repository_name}"

    @property
    def api_v1_url (self):
        return f"/api/v1/repository/{self.organization}/{self.repository_name}/permissions/user/{self.robot_account_name}"

    def perform_changes (self, state):
        exists = self.get_permissions()

        if state == "absent":
            if exists:
                self.do_delete()
        else:
           if not exists:
                self.do_update()
           elif exists["role"] != self.desired_permission:
                self.do_update()

    @returns_none_on_404
    def get_permissions (self):
        try:
            return self.quay_request.get(self.api_v1_url).json()
        except requests.HTTPError as e:
            if (e.response.status_code == 400 and
                e.response.json()["message"] == 'User does not have permission for repo.'):
                return None

    @property
    def desired_permission (self):
        return self.args.get("permission", "read")

    def do_update (self):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#changeuserpermissions
        response = self.quay_request.put(
            self.api_v1_url,
            dict(role=self.desired_permission))
        self.changed(f"Set {self.desired_permission} permission")

    def do_delete (self):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#deleteuserpermissions
        response = self.quay_request.delete(
            self.api_v1_url)
        self.changed(f"Deleted {self.desired_permission} permission")

import datetime

import requests

from ansible.plugins.action import ActionBase
from ansible.parsing.yaml.objects import AnsibleUnicode

from ansible_collections.epfl_si.actions.plugins.module_utils.subactions import AnsibleActions
from ansible_collections.epfl_si.actions.plugins.module_utils.ansible_api import AnsibleResults
from ansible_collections.epfl_si.quay.plugins.module_utils.quay_actions import QuayActionMixin, returns_none_on_404

class ActionModule (ActionBase, QuayActionMixin):
    """Set up or delete a robot account.

    See operation details and Ansible-level documentation in
    ../modules/robot_account.py which only exists for documentation
    purposes.
    """
    @AnsibleActions.run_method
    def run (self, args, ansible_api):
        self.args = args
        self.ansible = ansible_api  # For the mixin's `quay_hostname` and `quay_bearer_token`

        self.organization = args['organization']
        self.robot_account_name = args['short_name']

        self.result = AnsibleResults.empty()
        self.perform_changes(args.get('state', 'present'))
        return self.result

    @property
    def moniker (self):
        return f"{self.robot_account_name} robot account of {self.quay_hostname}/{self.organization}"

    @property
    def api_v1_url (self):
        return f"/api/v1/organization/{self.organization}/robots/{self.robot_account_name}"

    def perform_changes (self, state):
        exists = self.get()

        if state == "absent":
            if exists is not None:
                self.do_delete()
        else:
           if exists is None:
                self.do_create()

    @returns_none_on_404
    def get (self):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#robot-account-permissions-api
        return self.quay_request.get(self.api_v1_url).json()

    @property
    def desired_permission (self):
        return self.args.get("permission", "read")

    def do_create (self):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#creating-robot-account-api
        response = self.quay_request.put(
            self.api_v1_url)
        self.changed(f"Created ${self.moniker}")

    def do_delete (self):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#deleteuserpermissions
        response = self.quay_request.delete(
            self.api_v1_url)
        self.changed(f"Deleted ${self.moniker}")

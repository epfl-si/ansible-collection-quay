import datetime

from ansible.plugins.action import ActionBase
from ansible.parsing.yaml.objects import AnsibleUnicode

from ansible_collections.epfl_si.actions.plugins.module_utils.subactions import AnsibleActions
from ansible_collections.epfl_si.actions.plugins.module_utils.ansible_api import AnsibleResults
from ansible_collections.epfl_si.quay.plugins.module_utils.quay_actions import QuayActionMixin, returns_none_on_404

class ActionModule (ActionBase, QuayActionMixin):
    """Download a Kubeconfig file from the rancher back-end.

    See operation details and Ansible-level documentation in
    ../modules/quay_mirror.py which only exists for documentation
    purposes.
    """
    @AnsibleActions.run_method
    def run (self, args, ansible_api):
        self.args = args
        self.ansible = ansible_api  # For the mixin's `quay_hostname` and `quay_bearer_token`

        self.organization = args['organization']
        self.name = args['name']

        self.result = AnsibleResults.empty()
        self.perform_changes(args.get('state', 'present'))
        return self.result

    @property
    def moniker (self):
        return f"{self.quay_hostname}/{self.organization}/{self.name}"

    @property
    def api_v1_url (self):
        return f"/api/v1/repository/{self.organization}/{self.name}"

    def perform_changes (self, state):
        exists = self.get_repository_data()
        if state == "absent":
            if exists:
                self.do_delete()
        else:
            description = self.args["description"]
            visibility = self.args.get("visibility", "private")
            if exists:
                if exists["description"] != description:
                    self.do_update_description(description)
                if "failed" in self.result:
                    return

                if exists["is_public"] != (visibility == "public"):
                    self.do_update_visibility(visibility)
            else:
                self.do_create(description, visibility)

            if "failed" in self.result:
                return

            mirror_desired = self.args.get('mirror')
            if mirror_desired is not None:
                self.maybe_setup_mirror(mirror_desired, self.get_mirror_info())

    @returns_none_on_404
    def get_repository_data (self):
        return self.quay_request.get(self.api_v1_url).json()


    @property
    def api_v1_mirror_url (self):
        return f"{self.api_v1_url}/mirror"

    @returns_none_on_404
    def get_mirror_info (self):
        return self.quay_request.get(self.api_v1_mirror_url).json()

    def do_delete (self):
        response = self.quay_request.delete(self.api_v1_url)
        if response.status_code == 204:
            self.changed("deleted")
        else:
            self.failed(f"DELETE {self.api_v1_url}", "failed with status {response.status_code}")

    def do_create (self, description, visibility):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#createrepo
        response = self.quay_request.post(
            "/api/v1/repository",
            dict(
                namespace=self.organization,
                repository=self.name,
                description=description,
                visibility=visibility))

        if response.status_code == 201:
            self.changed("created")
        else:
            self.failed("POST /api/v1/repository", f"failed with status {response.status_code}")

    def do_update_description (self, description):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#updaterepo
        response = self.quay_request.put(
            self.api_v1_url,
            dict(description=description))
        if response.status_code == 200:
            self.changed("set description")
        else:
            self.failed(f"PUT {self.api_v1_url}", f"failed with status {response.status_code}")

    def do_update_visibility (self, visibility):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#changerepovisibility
        change_visibility_uri = f"{self.api_v1_url}/changevisibility"
        response = self.quay_request.POST(
            change_visibility_uri,
            dict(visibility=visibility))
        if response.status_code == 200:
            self.changed("set description")
        else:
            self.failed(f"POST {change_visibility_uri}", f"failed with status {response.status_code}")

    def maybe_setup_mirror (self, mirror_desired, mirror_actual):
        # https://docs.redhat.com/en/documentation/red_hat_quay/3/html-single/red_hat_quay_api_guide/index#quay-mirror-api
        desired_postdata = dict(
                is_enabled=True,
                external_reference=mirror_desired["from"],
                robot_username=mirror_desired["robot_account"],
                sync_interval=mirror_desired.get("sync_interval", None),
                sync_start_date=mirror_desired.get("sync_start_date", None),
                root_rule=dict(
                    rule_kind="tag_glob_csv",
                    rule_value=mirror_desired["tags"]))

        if desired_postdata["sync_interval"] is None:
            desired_postdata["sync_interval"] = (
                mirror_actual["sync_interval"] if mirror_actual is not None
                else 3600)

        if desired_postdata["sync_start_date"] is None:
            desired_postdata["sync_start_date"] = (
                mirror_actual["sync_start_date"] if mirror_actual is not None
                else datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'))

        if ( (mirror_actual is not None)
             and (mirror_actual["root_rule"]["rule_kind"] == "tag_glob_csv") ):
            # Merge new tags with old ones
            desired_postdata["root_rule"]["rule_value"].extend(
                t for t in mirror_desired["tags"]
                if t not in desired_postdata["root_rule"]["rule_value"])

        def is_substruct(a, b):
            if type(a) == AnsibleUnicode:
                return is_substruct(str(a), b)
            elif type(b) == AnsibleUnicode:
                return is_substruct(a, str(b))
            elif type(a) != type(b):
                return False
            elif type(a) == dict:
                for k in a.keys():
                    if k not in b:
                        return False
                    if not is_substruct(a[k], b[k]):
                        return False
                return True
            elif type(a) == list:
                if len(a) != len(b):
                    return False
                for (a_elem, b_elem) in zip(a, b):
                    if not is_substruct(a_elem, b_elem):
                        return False
                return True
            else:
                return a == b

        if is_substruct(desired_postdata, mirror_actual):
                return  # Ansible green

        response = self.quay_request.post(
            self.api_v1_mirror_url,
            desired_postdata)
        if response.status_code == 201:
            self.changed("set mirroring information")
        else:
            self.failed(f"POST {self.api_v1_mirror_url}", f"failed with status {response.status_code}")

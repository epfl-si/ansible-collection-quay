# Version 0.10.3

- New action plugin `epfl_si.quay.robot_account`

⚠ Versions 0.10.0 through 0.10.2 were broken in various ways; please don't use them.

# Version 0.9.0

- `epfl_si.quay.repository`: new `mirror.remove_tags` sub-option

# Version 0.8.0

- `epfl_si.quay.repository`: ability to force mirror resync (`.mirror.sync_now`)

# Version 0.7.1

- Documentation touchup
- Support Quay version 3.15.1 (`skopeo_timeout_interval` parameter for creating repositories)

# ~~Version 0.7.0~~

... is buggy; do not use it.

# Version 0.6.5

- Fix a few bugs related to mirroring

# Version 0.6.4

- Same as 0.6.5 except the bugs weren't fixed for real 🤷‍♂️

# Version 0.6.3

- Fix more permayellows in `epfl_si.quay.quay_repository`

# Version 0.6.2

- Fix `module 'datetime' has no attribute 'UTC'` on Python 3.10.x

# Version 0.6.1

- Fix a permayellow involving `epfl_si.quay.quay_repository` and mirroring

# Version 0.6.0

- Better error messages in case Kubernetes rejects our changes
- Update `quay_repository` state (using an HTTP PUT request)

# Version 0.5.0

- Tolerate `mirror.tags` being a single string, rather than a list

# Version 0.4.0

- Introduce the `format_docker_config_json` filter

# Version 0.3.0

- Introduce the `robot_account` lookup plugin

# Version 0.2.0

- Introduce the `robot_account_permission` task

# Version 0.1.0

- Introduce the `quay_repository` task, with support for mirroring

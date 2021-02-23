import os
import os.path
import shutil

from django.core.management.base import BaseCommand
from django.template import Template, Context

REQUIRED = object()
OPTIONAL = object()

LOCAL_SETTINGS_PATH = "local_settings.py"
LOCAL_SETTINGS_TEMPLATE = "deployment/local_settings.tmpl-dev.py"
ANSIBLE_VARIABLES_LOCAL_PATH = "infrastructure/ansible-variables.local.yml"
ANSIBLE_VARIABLES_LOCAL_TEMPLATE = "infrastructure/ansible-variables.local.yml.template"


class Command(BaseCommand):
    local_settings_prompts = [
        # Deployment options
        ("entrez_email", "Enter an email to use to query Entrez when importing data", REQUIRED),
    ]
    infrastructure_prompts = [
        # Infrastructure options.
        ("fqdn", "Enter {0}", "ginkgo-bioworks.11x.engineering"),
        ("key_name", "Please enter an AWS key that will be used to access your EC2 instance", OPTIONAL),
        ("ssh_key_path", "Please enter a path to your private key", OPTIONAL),
        ("zone_id", "Please enter the Route53 zone id for the test applications.", OPTIONAL),
        ("tls_private_key", "Please specify a path to a TLS private key that can be used for deployment", OPTIONAL),
        ("tls_public_key", "Please specify a path to a TLS public key that can be used for deployment", OPTIONAL),
    ]

    def add_arguments(self, parser):
        parser.add_argument("--local-settings", type=str, help=f"path to local settings file. Defaults to `{LOCAL_SETTINGS_PATH}`.")

    def handle(self, *args, **options):
        local_settings_path = options.get("local_settings", LOCAL_SETTINGS_PATH)

        config = self._get_dev_environment_config(self.local_settings_prompts)

        if not os.path.exists(local_settings_path):
            print(f"Creating {local_settings_path}")
            self._render_template(LOCAL_SETTINGS_TEMPLATE, local_settings_path, config)

        if not os.path.exists(ANSIBLE_VARIABLES_LOCAL_PATH):
            print(f"Creating ansible-variables.local.yml")
            self._render_template(ANSIBLE_VARIABLES_LOCAL_TEMPLATE, ANSIBLE_VARIABLES_LOCAL_PATH, config)

    def _render_template(self, template_path, dest, context):
        with open(template_path) as template_file:
            template_string = template_file.read()

        template = Template(template_string)
        content = template.render(Context(context))

        with open(dest, "w") as target:
            target.write(content)

    def _copy_if_not_exists(self, src, dst):
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

    def _has_local_settings(self, path):
        return os.path.exists(path)

    def _get_dev_environment_config(self, prompts):
        config = {}
        for key, prompt, default in prompts:
            value = self._get_user_input(key, prompt, default)
            if value is not None:
                config[key] = value
        return config

    def _get_user_input(self, key, prompt, default):
        while True:
            if default is REQUIRED:
                message = f"{prompt.format(key)} (required): "
            else:
                message = f"{prompt.format(key)}: "
            value = input(message).strip()

            # Return an appropriate value, or try again.
            if value:
                return value
            elif default is OPTIONAL:
                return None
            elif default is REQUIRED:
                print("This value is required.")
            else:
                return default

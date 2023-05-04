import json,yaml
from pathlib import Path

from .data_structures.Files.Config_file import Config_file
from .data_structures.Files.Infrastructure_template_sctructure import Infrastructure_template
from .data_structures.Files.Server_template import ServerTemplate

class SERVICE:
    def __init__(self, config_file_path:Path, infra_templates_directory:Path,
                 playbooks_directory:Path,server_templates_directory:Path) -> None:
        self.config_file_path = config_file_path
        self.infra_templates_directory = infra_templates_directory
        self.playbooks_directory = playbooks_directory
        self.server_templates_directory = server_templates_directory

    def file_open(self, file_path:Path):
        _json_format = ".json"
        _yaml_format = ".yml"

        def config()->Config_file:
            conf_data = json.load(open(self.config_file_path, 'r'))
            data_valid = Config_file(**conf_data)
            return data_valid
        def infr_temp(infrastrucre_temp_name:Path)->Infrastructure_template:
            temp_full_path = self.infra_templates_directory / infrastrucre_temp_name
            temp_full_path = temp_full_path.with_suffix(_yaml_format)
            temp_data = yaml.safe_load(open(temp_full_path, 'r'))
            data_valid = Infrastructure_template(**temp_data)
            return data_valid
        def serv_temp(serv_temp_name:Path)->ServerTemplate:
            temp_full_path = self.infra_templates_directory / serv_temp_name
            temp_full_path = temp_full_path.with_suffix(_yaml_format)
            temp_data = yaml.safe_load(open(temp_full_path, 'r'))
            data_valid = ServerTemplate(**temp_data)
            return data_valid

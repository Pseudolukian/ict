from core.data_structures.OneCloud.API_KEY import API_key
from pathlib import Path
from core.Service import SERVICE

#======Set up pathes=========#
set_up_paths = {"config_file_path":Path("./data/ict_config.json"),}
 = 
infra_templates_directory = Path("./templates/infrastructure")
playbooks_directory = Path("./templates/playbooks")
server_templates_directory = Path("./templates/servers")
#============================#

serv = SERVICE()

print(serv.file_open.infr_temp(infrastrucre_temp_name = "my_main_infra"))
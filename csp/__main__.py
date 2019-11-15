import os 
import re
from os.path import join
from pdb import set_trace

import yaml
from csp import MapColoring

def load_config(config_path):
    """ Loads a yml config file

        Note:
            eval() does not currently work when in the middle of a string or is
            used more than once!
        Args:
            config_path (str): The location of yml file that needs to be loaded.

        Returns:
            dict: Returns a parsed dictionary of the yml file.
    """
    def eval_constructor(loader, node):
        ''' Extract the matched value, expand env variable, and replace the match '''
        value = node.value

        if isinstance(value, str):
            match = "".join(eval_matcher.findall(value))
            return eval(match)

    # Modify loader
    eval_matcher = re.compile(r'eval\(([^}^{]+)\)')
    yaml.add_implicit_resolver('!eval', eval_matcher, None, yaml.SafeLoader)
    yaml.add_constructor('!eval', eval_constructor, yaml.SafeLoader)

    if not os.path.exists(config_path):
        raise ValueError("Config path does not exist!")

    with open(config_path, 'r') as stream:
        try:
            params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            print("{:=^50s}".format("FAILED TO LOAD"))
            set_trace()
            
    return params

def region_selector(region):
    region_file = '{}-adjacency.yml'
    
    if region.lower() == 'us':
       return load_config(join(os.getcwd(), region_file.format(region)))
    elif region.lower() == 'au':
       return load_config(join(os.getcwd(), region_file.format(region)))
    else:
        raise ValueError("Invalid region name {}!".format(region))


if __name__ == '__main__':
    working_dir = os.getcwd()
    config_path = join(working_dir, 'config.yml')
    config = load_config(config_path)
    problem_kwrags = config['problem']
    csp_kwargs = config['csp']
    
    region = region_selector(problem_kwrags['region'])

    csp = MapColoring(region, problem_kwrags['domain_size'])
    assigned = csp(**csp_kwargs)

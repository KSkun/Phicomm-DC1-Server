import json
from typing import List, Dict


class PhiCommDC1Config:
    mac_addr: str

    name: str
    switch_name: List[str]


C: Dict[str, PhiCommDC1Config] = {}


def load_config(file_path: str):
    """Load config fields to object C from file"""
    file = open(file_path, 'r', encoding='utf-8')
    json_str = file.read()
    file.close()

    json_objs = json.loads(json_str)

    var_list = PhiCommDC1Config.__annotations__
    for obj in json_objs:
        config = PhiCommDC1Config()
        for v in var_list:
            if v in obj:
                setattr(config, v, obj[v])
            else:
                raise ValueError('missing field %s in config file %s' % (v, file_path))
        config.mac_addr = config.mac_addr.lower()
        C[config.mac_addr] = config


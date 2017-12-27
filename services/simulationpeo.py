import services.base.frame_storage


class SimulationPEO(services.base.frame_storage.ListFrameStorage):

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = (
        ("committer",           str),
        ("tag",                 list),
        ("tracking",            list),
        ("comment",             list),
    )


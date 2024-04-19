
class CEnemySpawner:
    def __init__(self, level_conf:dict) -> None:
        self.total_time = 0
        self.level_conf = level_conf['enemy_spawn_events']
        self.index_list = []
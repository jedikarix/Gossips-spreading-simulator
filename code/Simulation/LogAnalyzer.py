from collections import defaultdict
from typing import Dict, List


class LogAnalyzer:
    """
    Class for simulation log analysis. Assumes that the log is JSON formatted.
    """
    def __init__(self, log_file: str) -> None:
        """
        Build up the simulation process from log_file JSON formatted
        :param log_file: log filename
        """
        self.log_entries = []
        with open(log_file) as f:
            logs = f.read().splitlines()
        for l in logs:
            self.log_entries.append(dict(eval(l)))

    def get_gossips_evolution(self) -> Dict[int, List[str]]:
        """
        Get gossips evolution during simulation
        :return: dictionary, where key is gossip_id and value is a list with gossip body during the simulation
        """
        gossips = defaultdict(list)
        for log in self.log_entries:
            message = log["message"]
            if message["msg_type"] != "receive":
                continue
            gossip_id = message["msg_id"]
            gossip_body = message["body"]
            gossips[gossip_id].append(gossip_body)
        return gossips

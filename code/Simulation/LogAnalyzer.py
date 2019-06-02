import logging
import time
from collections import defaultdict

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_entries = []
        with open(log_file) as f:
            logs = f.read().splitlines()
        for l in logs:
            self.log_entries.append(dict(eval(l)))

    def get_gossips_evolution(self):
        gossips = defaultdict(list)
        for log in self.log_entries:
            message = log["message"]
            if (message["msg_type"] != "receive"):
                continue
            gossip_id = message["msg_id"]
            gossip_body = message["body"]
            gossips[gossip_id].append(gossip_body)
        return gossips
import json
import re

class StatusParser():
    def __init__(self):
        self.patterns = {
            "server": {
                "hostname"        : re.compile('hostname(?: *):(?: *)(.*)'),
                "version"         : re.compile('version(?: *):(?: *)(.*)'),
                "ip"              : re.compile('udp/ip(?: *):(?: *)(.*):\d'),
                "port"            : re.compile('udp/ip(?: *):(?: *).*:(\d+) '),
                "map"             : re.compile('map(?: *):(?: *)(\w*)'),
                "player_count"    : re.compile('players(?: *):(?: *)(\d+)'),
                "max_player_count": re.compile('players(?: *):(?: *).*\((\d+)')
            },
            "players": {
                "id"              : re.compile('(?: *)(\d+)(?: *)\"'),
                "name"            : re.compile('\d+ \"(.*)\"'),
                "steam_id"        : re.compile('(STEAM_\d:\d:\d+)(?: *)'),
                "time_connected"  : re.compile(' ((?:\d{1,2}:)?\d{2}:\d{2}) '),
                "ping/loss"       : re.compile(' (\d+) '),
                "state"           : re.compile('(active|spawning)'),
                "ip"              : re.compile('(?: *)((?:\d{1,3}\.?){4}):')
            }
        }

    def parse(self, rcon):

        return {
            "hostname"         : self.get_hostname(rcon),
            "version"          : self.get_version(rcon),
            "ip"               : self.get_ip(rcon),
            "port"             : self.get_port(rcon),
            "map"              : self.get_map(rcon),
            "player_count"     : self.get_player_count(rcon),
            "max_player_count" : self.get_max_player_count(rcon),
            "players"          : self.get_players(rcon)
        }

    def get_hostname(self, rcon):
        return re.findall(self.patterns["server"]["hostname"], rcon)[0]

    def get_version(self, rcon):
        return re.findall(self.patterns["server"]["version"], rcon)[0]

    def get_ip(self, rcon):
        return re.findall(self.patterns["server"]["ip"], rcon)[0]

    def get_port(self, rcon):
        return re.findall(self.patterns["server"]["port"], rcon)[0]

    def get_map(self, rcon):
        return re.findall(self.patterns["server"]["map"], rcon)[0]

    def get_player_count(self, rcon):
        return re.findall(self.patterns["server"]["player_count"], rcon)[0]

    def get_max_player_count(self, rcon):
        return re.findall(self.patterns["server"]["max_player_count"], rcon)[0]

    def get_player_info(self, player):
        # Player ping/loss use backwards lookups for when there is a number surrounded by spaces in a player's name
        player_id             = re.findall(self.patterns["players"]["id"], player)[0]
        player_name           = re.findall(self.patterns["players"]["name"], player)[0]
        player_steam_id       = re.findall(self.patterns["players"]["steam_id"], player)[0]
        player_time_connected = re.findall(self.patterns["players"]["time_connected"], player)[0]
        player_ping           = re.findall(self.patterns["players"]["ping/loss"], player)[-2]
        player_loss           = re.findall(self.patterns["players"]["ping/loss"], player)[-1]
        player_ip             = re.findall(self.patterns["players"]["ip"], player)[0]
        player_state          = re.findall(self.patterns["players"]["state"], player)[0]

        return {
            "id"             : player_id,
            "name"           : player_name,
            "steam_id"       : player_steam_id,
            "time_connected" : player_time_connected,
            "ping"           : player_ping,
            "loss"           : player_loss,
            "ip"             : player_ip,
            "state"          : player_state
        }

    def get_players(self, rcon):
        pattern = re.compile("#(?: *)(\d+.*)")
        return [self.get_player_info(player) for player in re.findall(pattern, rcon)]


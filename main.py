import socket
import json
import argparse


class Miner:
    def __init__(self, ip):
        self.ip = ip
        self.board_1 = None
        self.board_2 = None
        self.board_3 = None
        self.boards_data = {}

    def get_state(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self.ip, 4028))
            payload = {"command": "stats"}
            sock.send((json.dumps(payload).encode('utf-8')))
            received = sock.recv(8192)
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

        received = received.replace(b'}{', b',')

        data = json.loads(received[:-1])

        asc_data = data['STATS'][0]

        chain_2 = asc_data['chain_acn2']
        chain_9 = asc_data['chain_acn9']
        chain_10 = asc_data['chain_acn10']
        chain_3 = asc_data['chain_acn3']
        chain_11 = asc_data['chain_acn11']
        chain_12 = asc_data['chain_acn12']
        chain_4 = asc_data['chain_acn4']
        chain_13 = asc_data['chain_acn13']
        chain_14 = asc_data['chain_acn14']

        self.board_1 = {'chain1': int(chain_2), 'chain2': int(chain_9), 'chain3': int(chain_10), 'name': 'board_1'}
        self.board_2 = {'chain1': int(chain_3), 'chain2': int(chain_11), 'chain3': int(chain_12), 'name': 'board_2'}
        self.board_3 = {'chain1': int(chain_4), 'chain2': int(chain_13), 'chain3': int(chain_14), 'name': 'board_3'}

        for board in [self.board_1, self.board_2, self.board_3]:
            dead_num = 0
            fail_num = 0
            work_num = 0
            for chain in board.keys():
                if chain == 'name':
                    pass
                else:
                    if board[chain] == 0:
                        dead_num += 1
                    elif board[chain] < 18:
                        fail_num += 1
                    else:
                        work_num += 1
            if work_num == 3:
                self.boards_data[board['name']] = 'W'
            elif fail_num > 0:
                self.boards_data[board['name']] = 'CI'
            elif dead_num > 0 < 3:
                self.boards_data[board['name']] = 'DC'
            elif dead_num == 3:
                self.boards_data[board['name']] = 'NS'

        return "Board 1: " + self.boards_data['board_1'] + "\n" + \
               "Board 2: " + self.boards_data['board_2'] + "\n" + \
               "Board 3: " + self.boards_data['board_3']


parser = argparse.ArgumentParser(description='T9 Failure Identifier')
parser.add_argument('IP', help='IP address of the miner')
args = parser.parse_args()
HOST = args.IP
miner = Miner(HOST)

if __name__ == '__main__':
    print(miner.get_state())

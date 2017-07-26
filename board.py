#!/usr/bin/python2

from vivadotcl import VivadoInstance


class BoardManager():
    board_map = {}
    board_used = {}

    def __init__(self, vivado):
        v = VivadoInstance(vivado)
        v.connect_hw_server()
        all_targets = v.get_hw_targets()
        for b in all_targets:
            new_vivado = VivadoInstance(vivado)
            new_vivado.connect_hw_server()
            self.board_map[b] = new_vivado
            self.board_used[b] = False

    def program_board(self, board, bitfile):
        v = self.board_map[board]
        return v.program_target(board, bitfile)

    def release_board(self, board):
        self.board_used[board] = False

    def program_bit(self, bitfile):
        for b in self.board_map.keys():
            if not self.board_used[b]:
                self.board_used[b] = True
                msg = self.program_board(b, bitfile)
                return 0, b, msg
        return -1, None, "Error: No boards are available."

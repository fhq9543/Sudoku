# -*- coding: utf-8 -*-
'''sudoku'''

from collections import namedtuple
from copy import deepcopy


class SudokuError(Exception):
    '''sudoku异常'''
    pass


class Record():
    '''记录解题历史'''
    class HistoryRecord():
        '''解题历史记录类
        :param pos_value: Record.posvalue, 有名元组类型, 包含格子位置和可选的数值
        :param sudoku: Sudoku.sudoku, 当前数据的所有内容
        :param pos_value_index: 当前尝试的Record.posvalue.list_序号
        '''
        def __init__(self, pos_value, sudoku, pos_value_index):
            self.pos_value = pos_value
            self.sudoku = sudoku
            self.pos_value_index = pos_value_index

        def __str__(self):
            return self.__repr__()

        def __repr__(self):
            return str((self.pos_value, self.sudoku, self.pos_value_index))

    def __init__(self):
        self.cycle_record = []
        self.history_record = []
        self.posvalue = namedtuple('posvalue', ['row', 'column', 'list_'])

    def add(self, row, column, list_):
        '''将格子可能取值记录到记录容器中
        :param row: 格子的行
        :param column: 格子的列
        :param list_: 格子的可能取值
        '''
        if self.cycle_record and (row, column) < self.cycle_record[-1]:
            raise SudokuError('每一次循环前需清空记录')
        self.cycle_record.append(self.posvalue(row, column, list_))

    def clean(self):
        '''清空格子记录容器'''
        self.cycle_record = []

    def optimal_record(self):
        '''从格子记录容器选出最短可能取值的格子信息
        :return: Record.posvalue
        '''
        opt_record = sorted(self.cycle_record, key=lambda x: len(x[2]) or 10)[0]
        return opt_record

    def forward(self, sudoku):
        '''在解题每一次遍历中找不到唯一值，则调用该函数填入候选值
        :param sudoku: 当前的sudoku，保存到历史记录中
        :return: 要尝试的格子位置以及对应值
        '''
        opt_record = self.optimal_record()
        self.history_record.append(self.HistoryRecord(opt_record, deepcopy(sudoku), 0))
        return (opt_record.row, opt_record.column, opt_record.list_[0])

    def get_last_record(self):
        '''获取最后记录并返回下一个要尝试的格子位置和值
        :return: Record.posvalue, 要尝试的格子位置以及对应值
        '''
        if not self.history_record:
            raise SudokuError('没有历史记录')
        last_record = self.history_record[-1]
        last_record.pos_value_index += 1
        if last_record.pos_value_index == len(last_record.pos_value.list_):
            # 可尝试值已经全部尝试过，返回上一次历史记录状态。
            self.history_record.pop(-1)
            # print(last_record)
            return self.get_last_record()
        return last_record

    def backwards(self):
        '''进行回溯尝试
        :return: 返回记录中的历史sudoku
        '''
        last_record = self.get_last_record()
        sudoku = last_record.sudoku
        sudoku[last_record.pos_value.row][last_record.pos_value.column] = \
            last_record.pos_value.list_[last_record.pos_value_index]
        return sudoku


class Sudoku():
    '''sudoku解题类
    :param filename: 保存待解的sudoku文件名
    '''
    def __init__(self, filename):
        self.sudoku = self.get_sudoku_from_file(filename)
        self.unsolved_num = sum(line.count(0) for line in self.sudoku)
        self.record = Record()
        self.display()

    def update_unsolved_num(self):
        '''更新当前未解的格子数量'''
        self.unsolved_num = sum(line.count(0) for line in self.sudoku)

    @staticmethod
    def get_sudoku_from_file(filename):
        '''从文件中获取sudoku'''
        with open(filename) as f:
            lines = f.readlines()
        return [[int(ele) for ele in line[:9]] for line in lines]

    def get_row_eles(self, row):
        '''获取行已存在的数字'''
        return set(self.sudoku[row])

    def get_column_eles(self, column):
        '''获取列已存在的数字'''
        return set(row[column] for row in self.sudoku)

    def get_grid_eles(self, x_axis, y_axis):
        '''获取九宫格已存在的数字'''
        x_start = x_axis // 3 * 3
        y_start = y_axis // 3 * 3
        ret_set = set()
        for x in range(x_start, x_start+3):
            for y in range(y_start, y_start+3):
                ret_set.add(self.sudoku[x][y])
        return ret_set

    def update(self, x_axis, y_axis, value):
        '''更新sudoku的某个位置'''
        self.sudoku[x_axis][y_axis] = value
        self.unsolved_num -= 1
        # self.display()

    def update_sudoku(self, sudoku):
        '''更新当前的sudoku'''
        self.sudoku = deepcopy(sudoku)
        self.update_unsolved_num()
        # self.display()

    def solve(self):
        '''解题'''
        pre_unsolved_num = 0
        while self.unsolved_num != 0:
            if self.unsolved_num == pre_unsolved_num:
                # 遍历一边之后找不到能填唯一值的位置 ,开始尝试填入候选值
                r, c, v = self.record.forward(self.sudoku)
                self.update(r, c, v)
            pre_unsolved_num = self.unsolved_num
            self.record.clean()
            for row in range(9):
                for column in range(9):
                    if self.sudoku[row][column] != 0:
                        continue
                    row_set = self.get_row_eles(row)
                    column_set = self.get_column_eles(column)
                    grid_set = self.get_grid_eles(row, column)
                    set_ = set(range(1, 10)) - row_set - column_set - grid_set
                    self.record.add(row, column, list(set_))
                    if len(set_) == 1:
                        # 找到当前位置只能填唯一值
                        # print(row, column, set_)
                        self.update(row, column, set_.pop())
                        break
                    elif not set_:
                        try:
                            # 没有能填值的位置，回退到上一次尝试填值的状态并尝试填入其他可填值。
                            sudoku = self.record.backwards()
                            self.update_sudoku(sudoku)
                        except SudokuError as e:
                            print(e)
                            raise SudokuError('无解')
                    else:
                        pass
        self.display()

    def display(self):
        '''sudoku打印'''
        for line in self.sudoku:
            print(line)
        print()


if __name__ == "__main__":
    s = Sudoku('sudokudata.txt')
    s.solve()

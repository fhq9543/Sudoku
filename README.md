## 数独是9*9共81个格子，同时又分为9个九宫格,每一个格中的数字，都保证与其所在横排和竖排以及九宫格内无相同数字。 ##
1. 遍历每一个没有数字的格子，记录这个格子所有候选值。如果存在唯一候选值，则填入。如果没有候选值（证明此次尝试无解），则跳出遍历，从上一个数独记录状态找拥有最少候选值的格子，从这个格子候选值中取一个进行填值。
1. 当遍历一边找不到唯一值的时候，记录此时数独的状态，开始尝试从格子记录容器中找最少候选值的格子，从这个格子候选值中取一个进行填值。
1. 循环进行上面两步，直到填满。

Sudoku ：数独解题类
	
	update_unsolve_num ：更新当前未解的格子数量

	get_sudoku_from_file(filename) ：从文件中获取sudoku
	
	get_row_eles(self, row) ：获取行已存在的数字
	
	get_column_eles(self, column) ：获取列已存在的数字
	
	get_grid_eles(self, x_axis, y_axis) ：获取九宫格已存在的数字
	
	update(self, x_axis, y_axis, value) ：更新sudoku的某个位置
	
	update_sudoku(self, sudoku) ：更新当前的sudoku
	
	solve ：解题
	
	display ：打印当前sudoku
	

Record ：记录解题历史	
	
	HistoryRecord ：解题历史记录类        
		:param pos_value: Record.posvalue, 有名元组类型, 包含格子位置和可选的数值
        :param sudoku: Sudoku.sudoku, 当前数据的所有内容
        :param pos_value_index: 当前尝试的Record.posvalue.list_序号add(self, row, column, list_) ：将格子可能取值记录到记录容器中
        :param row: 格子的行
        :param column: 格子的列
        :param list_: 格子的可能取值
		
	clean ：清除格子记录容器
	
	optimal_record ：从格子记录容器选出最短可能取值的格子信息
	
	forward(self, sudoku) ：在解题每一次遍历中找不到唯一值，则调用该函数填入候选值
        :param sudoku: 当前的sudoku，保存到历史记录中
        :return: 要尝试的格子位置以及对应值
		
	get_last_record ：获取最后记录并返回下一个要尝试的格子位置和值
        :return: Record.posvalue, 要尝试的格子位置以及对应值
	
	backwards ：进行回溯尝试
        :return: 返回记录中的历史sudoku
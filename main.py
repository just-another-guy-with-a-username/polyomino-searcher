import sys
import copy

class Polyomino:
	def __init__(self, rows, columns, graph=[]):
		self.rows = rows
		self.columns = columns
		self.one_hor_ref_sym = False
		self.two_ref_sym = False
		self.one_dia_ref_sym = False
		self.nin_rot_sym = False
		self.hal_rot_sym = False
		self.graph = graph
		if not self.graph:
			for _ in range(rows):
				row = []
				for _ in range(columns):
					row.append(False)
				self.graph.append(row)

	def __repr__(self):
		shape = ""
		for row in self.graph:
			for cell in row:
				if cell:
					shape += "[]"
				else:
					shape += "  "
			shape += "\n"
		return shape

	def add_block(self, row, col):
		self.graph[row][col] = True

	def reflect_h(self):
		for i in range(len(self.graph)):
			self.graph[i].reverse()

	def reflect_v(self):
		self.graph.reverse()

	def rotate(self):
		new_graph = []
		for _ in range(self.columns):
			row = []
			for _ in range(self.rows):
				row.append(False)
			new_graph.append(row)
		for i in range(len(self.graph)):
			for j in range(len(self.graph[i])):
				if self.graph[i][j]:
					new_graph[-(j+1)][i] = True
		self.graph = new_graph
		self.columns, self.rows = self.rows, self.columns

	def counter_rotate(self):
		new_graph = []
		for _ in range(self.columns):
			row = []
			for _ in range(self.rows):
				row.append(False)
			new_graph.append(row)
		for i in range(len(self.graph)):
			for j in range(len(self.graph[i])):
				if self.graph[i][j]:
					new_graph[j][-(i+1)] = True
		self.graph = new_graph
		self.columns, self.rows = self.rows, self.columns

	def expand(self):
		empty_row = []
		for _ in range(self.columns):
			empty_row.append(False)
		self.graph.insert(0, empty_row[:])
		self.graph.append(empty_row[:])
		for row in self.graph:
			row.insert(0, False)
			row.append(False)
		self.rows += 2
		self.columns += 2

	def rot_sym_check(self):
		graph = copy.deepcopy(self.graph)
		self.rotate()
		if self.graph == graph:
			self.nin_rot_sym = True
			self.hal_rot_sym = True
		else:
			self.rotate()
			if self.graph == graph:
				self.hal_rot_sym = True
				self.nin_rot_sym = False
		if not self.hal_rot_sym:
			self.rotate()
			self.rotate()

	def rel_sym_check(self):
		graph = copy.deepcopy(self.graph)
		self.reflect_h()
		graph2 = copy.deepcopy(self.graph)
		self.reflect_h()
		self.reflect_v()
		graph3 = copy.deepcopy(self.graph)
		self.rotate()
		graph4 = copy.deepcopy(self.graph)
		self.reflect_v()
		self.reflect_h()
		graph5 = copy.deepcopy(self.graph)
		self.rotate()
		self.rotate()
		self.rotate()
		self.reflect_h()
		if graph == graph2 and graph == graph3:
			self.two_ref_sym = True
			self.one_hor_ref_sym = True
			self.one_dia_ref_sym = True
		elif graph == graph2 or graph == graph3:
			self.two_ref_sym = False
			self.one_dia_ref_sym = False
			self.one_hor_ref_sym = True
		elif graph == graph4 or graph == graph5:
			self.two_ref_sym = False
			self.one_hor_ref_sym = False
			self.one_dia_ref_sym = True

	def sym_check(self):
		self.rot_sym_check()
		self.rel_sym_check()

	def clear_excess(self):
		has_true = False
		for row in self.graph[:]:
			for cell in row:
				if cell:
					has_true = True
			if not has_true:
				self.graph.remove(row)
				self.rows -= 1
			has_true = False
		self.rotate()
		for row in self.graph[:]:
			for cell in row:
				if cell:
					has_true = True
			if not has_true:
				self.graph.remove(row)
				self.rows -= 1
			has_true = False
		self.counter_rotate()

	def prep_for_list(self):
		self.clear_excess()
		self.sym_check()

	def adjacent_squares(self):
		adjacents = []
		for i in range(self.rows):
			for j in range(self.columns):
				if i == 0:
					if self.graph[i+1][j]:
						adjacents.append((i, j))
						continue
				elif j == 0:
					if self.graph[i][j+1]:
						adjacents.append((i, j))
						continue
				elif i == self.rows - 1:
					if self.graph[i-1][j]:
						adjacents.append((i, j))
						continue
				elif j == self.columns - 1:
					if self.graph[i][j-1]:
						adjacents.append((i, j))
						continue
				else:
					if (self.graph[i+1][j] or self.graph[i][j-1] or self.graph[i][j+1] or self.graph[i-1][j]) and not self.graph[i][j]:
						adjacents.append((i, j))
						continue
		return adjacents

	def __deepcopy__(self, memo):
		deepcopy_method = self.__deepcopy__
		self.__deepcopy__ = None
		cp = copy.deepcopy(self, memo)
		self.__deepcopy__ = deepcopy_method
		cp.__deepcopy__ = deepcopy_method
		return cp

	def new_polyominoes(self):
		self.expand()
		adjacents = self.adjacent_squares()
		new_polyominoes = []
		for loc in adjacents:
			new = Polyomino(self.rows, self.columns, copy.deepcopy(self.graph))
			new.add_block(loc[0], loc[1])
			new.clear_excess()
			new_polyominoes.append(new)
		self.clear_excess()
		return new_polyominoes

def search(n):
	n -= n%1
	if n <= 0 :
		return []
	if n == 1:
		p = Polyomino(1, 1)
		p.add_block(0, 0)
		return [p]
	prev_gen = search(n-1)
	kept = []
	graphs = []
	for prev in prev_gen:
		next_gen = prev.new_polyominoes()
		for next in next_gen:
			if next.graph in graphs:
				continue
			next.rotate()
			if next.graph in graphs:
				continue
			next.rotate()
			if next.graph in graphs:
				continue
			next.rotate()
			if next.graph in graphs:
				continue
			next.reflect_v()
			if next.graph in graphs:
				continue
			next.rotate()
			if next.graph in graphs:
				continue
			next.rotate()
			if next.graph in graphs:
				continue
			next.rotate()
			if next.graph in graphs:
				continue
			if next.rows > next.columns:
				next.rotate()
			kept.append(next)
			graphs.append(next.graph)
	return kept

def listify_step(polyominoes_section, pos, graph):
	if pos == len(polyominoes_section):
		return graph
	graph2 = copy.deepcopy(polyominoes_section[pos].graph)
	num_rows = max([len(graph), len(graph2)])
	while len(graph) < num_rows:
		empty_row = []
		for cell in graph[0]:
			empty_row.append(False)
		graph.append(empty_row)
	while len(graph2) < num_rows:
		empty_row = []
		for cell in graph2[0]:
			empty_row.append(False)
		graph2.append(empty_row)
	for i in range(num_rows):
		graph[i].append(False)
		graph[i] += graph2[i]
	return listify_step(polyominoes_section, pos + 1, graph)

def listify(polyominoes, n):
	n = int(n-n%1)
	pol_list = []
	for i in range(0, len(polyominoes), n):
		c_group = None
		if len(polyominoes) - i > n - 1:
			c_group = listify_step(polyominoes[i+1:i + n], 0, polyominoes[i].graph)
		else:
			c_group = listify_step(polyominoes[i+1:], 0, polyominoes[i].graph)
		pol_list.append(Polyomino(len(c_group), len(c_group[0]), c_group))
	return pol_list

if len(sys.argv) > 1:
	polyominoes = search(float(sys.argv[1]))
else:
	polyominoes = search(4)
if len(sys.argv) > 2:
	pol_list = listify(polyominoes, float(sys.argv[2]))
else:
	pol_list = listify(polyominoes, 4)
for p in pol_list:
	print(p)
print(f"n = {len(polyominoes)}")

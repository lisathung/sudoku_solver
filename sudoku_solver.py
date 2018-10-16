# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
"""
A Sudoku puzzle is a grid of 81 squares; the majority of enthusiasts label the columns 1-9, the rows A-I, 
and call a collection of nine squares (column, row, or box) a unit and the squares that share a unit the peers. 
"""
root = Tk(  )
size = 9
cols = '123456789'
rows = 'ABCDEFGHI'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

#Notations
squares = cross(rows,cols)	#names for every individual square on board
unitlist = ([cross(rows, c) for c in cols] +
        [cross(r, cols) for r in rows] +
        [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]) #rows, columns and squares
units = dict((s, [u for u in unitlist if s in u]) for s in squares) #maps the columns,rows and units of a square 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)	#peers for each square

def findNextCellToFill(cells, key):
	"""
	finds an empty cell to fill, if there are none left. the puzzle is "solved", return -1
	Input: list of GUI cells, key
	Output: returns key of next empty cell. If no empty cell, return -1
	"""

	#checks if all cells are filled
	if all((len(cells[key]) == 1) for key in cells):
		return -1

	#chooses an empty cell
	min_key = min(cells.keys(), key=(lambda k: cells[k]))
	return min_key

def isValid(cells,key,num):
	"""
	function for checking if the number of cell is not present in any of its peers, if double is found puzzle is invalid
	Input: list of GUI cells, key, number being tested
	Output: If num is not present in peers of key, it is valid. Return true, False otherwise
	"""
	check = all(num not in cells[peer_key] for peer_key in peers[key])
	return check

def solveSudoku(cells,cell_values,key = "A1"):
	"""
	Recursive function for solving a particular cell using depth first search
	Input: list of GUI cells, dictionary of current cell values, key
	Output: return True if solved, False otherwise 
	"""
	key = findNextCellToFill(cell_values, key) #looking for empty squares to fill

	if key == -1:
		return True		#no more empty squares, puzzle solved
	else:
		for num in cols:
			if isValid(cell_values,key,num):
				cell_values[key] = num 	#Testing out number
				if solveSudoku(cells,cell_values,key):
					return True
				cell_values[key] = ""	#resetting changes and removes number that was tested
	return False	#puzzle not solved

def masterSolve(cells,cell_values):
	"""
	Main solve function performs 
	i)	inital Update
	ii)	Checks validity of puzzle
	iii)final update.
	Input: list of GUI cells, dictionary of current cell values
	Output: updates cells and cell_values
	"""

	#takes in the sudoku problem via input from user and updates values
	for cell,key in zip(cells,cell_values):	
		cell_values[key] = cell.get() if cell.get()!= "" else ""
	
	#two repeating numbers belonging to the same peer group is an invalid puzzle
	for key in cell_values:
		if any(cell_values[key] in cell_values[peer_key] for peer_key in peers[key]) and cell_values[key] != "":
			messagebox.showinfo("Error","Invalid Puzzle")
			return -2

	#runs depth first algo to solve sudoku problem
	result =  solveSudoku(cells,cell_values)

	#updating final values for GUI	
	for cell, key in zip(cells,cell_values):
		cell.delete(0,END)
		cell.insert(0,cell_values[key])

def createGrid(cell_values):
	"""
	Function for creating Inital Grid
	Input: list of squares
	Output: creates sudoku board
	"""
	cells = [None for i in range(size**2)] #stores cells of grid
	cell_count = 0
	for i in range(size):
		for j in range(size):
			cells[cell_count] = (Entry(root, width = 5, borderwidth = 1 )) #creating cells
			cells[cell_count].grid(row = i, column = j)	#placing cells
			cell_count +=1

	#button press to solve
	run = Button(root, text = "Solve", command = lambda: masterSolve(cells,cell_values), width = 3, borderwidth = 2).grid(row = 10, column = 4)

def main():
	cell_values = dict((s, "") for s in squares)	#stores current value of each cell
	createGrid(cell_values)		#creating GUI

main()
root.mainloop()
from spreadsheet.baseSpreadsheet import BaseSpreadsheet
from spreadsheet.cell import Cell
from math import isclose
from typing import List, Tuple

# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Trie-based dictionary implementation.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2023, RMIT University'
# ------------------------------------------------------------------------

class CSRSpreadsheet(BaseSpreadsheet):

    def __init__(self):
        self.cola = []      # indicates which columns have values
        self.vala = []      # indicates the values for populated cells
        self.filled = []      # indicates the cumulative number of non-blank cells (first entry is 0, beginning of first row)
        self.num_cols = 0   # needed when empty columns are appended


    def buildSpreadsheet(self, lCells: List[Cell]):
        """
        Construct the data structure to store nodes.
        @param lCells: list of cells to be stored
        """
        for cell in lCells:
            print(f"trying to add {cell.val} at {cell.row}, {cell.col}")
            while not self.update(cell.row, cell.col, cell.val):
                # well, we gotta add the row or column.
                if cell.row >= self.num_rows():
                    self.appendRow()
                if cell.col >= self.num_cols:
                    self.appendCol()

        # TODO remove this
        self.print_spreadsheet()

    def appendRow(self):
        """
        Appends an empty row to the spreadsheet.

        @return True if operation was successful, or False if not.
        """
        if not self.filled:
            filled_cells = 0
        else:
            filled_cells = self.filled[-1] # if self.cnta else 0
        self.filled.append(filled_cells)
        return True


    def appendCol(self):
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """
        self.num_cols += 1
        return True


    def insertRow(self, rowIndex: int)->bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row to insert the new row AFTER.  If inserting as first row, specify rowIndex to be -1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """
        success = False
        if rowIndex == -1:
            self.appendRow()
        elif 0 <= rowIndex < self.num_rows():
            end_of_row = rowIndex
            filled_cells = self.filled[end_of_row]
            self.filled.insert(end_of_row, filled_cells)  # python insert is BEFORE index
            success = True
        return success


    def insertCol(self, colIndex: int)->bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column to insert the new column  AFTER. If inserting as first row, specify colIndex to be -1.

        return True if operation was successful, or False if not, e.g., colIndex is invalid.
        """
        success = False
        if colIndex == -1:
            self.appendCol()
        elif 0 <= colIndex <= self.num_cols:
            for index in range(0, len(self.cola)):
                if self.cola[index] >= colIndex:
                    self.cola[index] += 1
            self.num_cols += 1
            success = True
        return success


    def update(self, rowIndex: int, colIndex: int, value: float) -> bool:
        """
        Update the cell with the input/argument value.

        @param rowIndex Index of row to update.
        @param colIndex Index of column to update.
        @param value Value to update.  Can assume they are floats.

        @return True if cell can be updated.  False if cannot, e.g., row or column indices do not exist.
        """
        can_update = True
        existing_cell = False

        if (rowIndex >= self.num_rows()) or (colIndex >= self.num_cols):
            can_update = False
            # print('row or col out of bounds')
        else:
            print(f'Updating R {rowIndex}, C {colIndex} to {value}')
            # calculate index for cola/vala
            filled_cells_at_start_of_row = self.filled[rowIndex]
            filled_cells_by_end_of_row  = self.filled[rowIndex + 1]
            index = filled_cells_at_start_of_row     # index into vals/cols at start of row
            
            while not (filled_cells_at_start_of_row == filled_cells_by_end_of_row == 0) \
                  and index <= filled_cells_by_end_of_row \
                  and self.cola \
                  and index < len(self.cola) \
                  and self.cola[index] <= colIndex:
                if self.cola[index] == colIndex:
                    existing_cell = True
                    break
                index += 1
                # if self.cola[index] > colIndex:
                #     break
                        
            # now we know where we need to update/delete/insert
            if existing_cell:
                old_value = self.vala[index]
                difference = value - old_value
                self.vala[index] = value
            else:
                self.cola.insert(index, colIndex)
                self.vala.insert(index, value)
                for r in range(rowIndex + 1, self.num_rows() + 1):
                    self.filled[r] += 1

        return can_update


    def rowNum(self)->int:
        """
        @return Number of rows the spreadsheet has.
        """
        return self.num_rows()


    def colNum(self)->int:
        """
        @return Number of columns the spreadsheet has.
        """
        return self.num_cols


    def find(self, value: float) -> List[Tuple[int, int]]:
        """
        Find and return a list of cells that contain the value 'value'.

        @param value value to search for.

        @return List of cells (row, col) that contains the input value.
	    """

        cells_with_value = []
        col = 0
        index = 0
        filled_cells_so_far = 0   
        for r in range(0, self.num_rows()):
            col = 0
            while col < self.num_cols:
                if filled_cells_so_far < self.filled[r+1] and self.cola[index] == col:
                    if isclose(self.vala[index], value):
                        cell = (r, col)
                        cells_with_value.append(cell)
                    index += 1
                    filled_cells_so_far += 1
                col += 1

        return cells_with_value


    def entries(self) -> List[Cell]:
        """
        @return A list of cells that have values (i.e., all non None cells).
        """
        values = []
        filled_cells_so_far = 0
        row = 0
        index = 0
        while index < len(self.vala):
            while filled_cells_so_far == self.filled[row]:
                row += 1
            filled_cells_so_far += 1
            c = Cell(row - 1, self.cola[index], self.vala[index])
            values.append(c)
            index += 1

        return values


    def num_rows(self) -> int:
        """
        @return Number of rows in the spreadsheet.
        """
        return len(self.filled) - 1 if self.filled else 0
    

    def print_spreadsheet(self) -> None:
        """
        Prints the spreadsheet to the terminal.
        """
        print()
        print('cola\t', self.cola)
        print('vala\t', self.vala)
        print('suma\t', self.filled)
        print()
        
        # print column headers
        print('\t', end='')
        for c in range(0, self.num_cols):
            print(c, '\t', end='')
        print()

        # print rows
        col = 0
        index = 0
        filled_cells_so_far = 0        
        for r in range(0, self.num_rows()):
            print(r, '\t', end='')
            col = 0
            while col < self.num_cols:
                if filled_cells_so_far < self.filled[r+1] and self.cola[index] == col:
                    print(self.vala[index], end='\t')
                    index += 1
                    filled_cells_so_far += 1
                else:
                    print('.', end='\t')
                col += 1
            print()
            
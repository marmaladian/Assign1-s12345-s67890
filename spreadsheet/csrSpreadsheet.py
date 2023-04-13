from spreadsheet.baseSpreadsheet import BaseSpreadsheet
from spreadsheet.cell import Cell
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
        self.suma = []      # indicates the cumulative sum up to [n]th row, len = num_rows + 1
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
        if not self.suma:
            self.suma.append(0)
        sum_for_new_row = self.suma[-1] if self.suma else 0
        self.suma.append(sum_for_new_row)
        # print(f"append row: new size is R {self.num_rows()}, C {self.num_cols}")
        return True         # why would this fail? too many rows?

    def appendCol(self):
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """
        self.num_cols += 1
        # print(f"append col: new size is R {self.num_rows()}, C {self.num_cols}")
        return True         # why would this fail?


    def insertRow(self, rowIndex: int)->bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row to insert the new row AFTER.  If inserting as first row, specify rowIndex to be -1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """
        success = False
        if -1 <= rowIndex < self.num_rows():            # check range
            sum_at_row = self.suma[rowIndex + 1]        # sum for new row = sum for row after
            self.suma.insert(rowIndex + 1, sum_at_row)  # python insert is BEFORE index
            success = True
        return success


    def insertCol(self, colIndex: int)->bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column to insert the new column  AFTER. If inserting as first row, specify colIndex to be -1.

        return True if operation was successful, or False if not, e.g., colIndex is invalid.
        """
        success = False
        if -1 <= colIndex <= self.num_cols:
            for col in self.cola:
                if col > colIndex:
                    col += 1
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
            # calculate index for cola/vala
            row_start_sum = self.suma[rowIndex]
            row_end_sum   = self.suma[rowIndex + 1]
            index = 0
            sum = 0
            while sum < row_start_sum:
                sum += self.vala[index]
                index += 1
            # refine the index within the row
            while sum <= row_end_sum and self.cola and index < len(self.cola) and self.cola[index] <= colIndex:
                if self.cola[index] == colIndex:
                    existing_cell = True
                index += 1
            
            # now we know where we need to update/delete/insert
            if existing_cell:
                old_value = self.vala[index]
                difference = value - old_value
                self.vala[index] = value
                for r in range(rowIndex + 1, len(self.suma)):
                    self.suma[r] += difference
            else:           # TODO not handling DELETE yet
                old_value = 0
                difference = value - old_value
                # self.cola.insert(index + 2, colIndex)
                # self.vala.insert(index + 2, value)
                self.cola.insert(index, colIndex)
                self.vala.insert(index, value)
                for r in range(rowIndex + 1, len(self.suma)):
                    self.suma[r] += difference

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

        # TO BE IMPLEMENTED

        # REPLACE WITH APPROPRIATE RETURN VALUE
        return []


    def entries(self) -> List[Cell]:
        """
        @return A list of cells that have values (i.e., all non None cells).
        """
        values = []
        sum = 0
        row = 0
        index = 0
        while index < len(self.vala):
            while sum == self.suma[row]:
                row += 1
            sum += self.vala[index]
            c = Cell(row - 1, self.cola[index], self.vala[index])
            values.append(c)
            index += 1

        return values


    def num_rows(self) -> int:
        """
        @return Number of rows in the spreadsheet.
        """
        return len(self.suma) - 1 if self.suma else 0
    

    def print_spreadsheet(self) -> None:
        """
        Prints the spreadsheet to the terminal.
        """
        #   5  .  3
        #   .  4  .
        #   6  . -2

        #   . . . . . . . . . .
        #   . . . . . . . . . .
        #   . . . . . 7 . . . .
        #   . 6 . . . . . . . .
        #   . . . . . . . . . .
        #   . . . . . . . . . .
        #   . . . . . . . . . .
        #   . . . . . . . . . .
        #   . . . . .-6.7 . . .
        #   . . . . . . . . . 2

        print()
        print('cola\t', self.cola)
        print('vala\t', self.vala)
        print('suma\t', self.suma)
        print()

        sum = 0
        vc_index = 0
        for r in range(1, self.num_rows() + 1): # row_sum in self.suma
            col = 0
            while sum != self.suma[r] and col < self.num_cols:          # stops if sum is reached...
                if col == self.cola[vc_index]:
                    value = self.vala[vc_index]
                    print(value, end='\t')
                    sum += value
                    vc_index += 1
                else:
                    print('·', end='\t')
                col += 1
            while col < self.num_cols:
                print('·', end='\t')
                col += 1
            print()
        print()

            



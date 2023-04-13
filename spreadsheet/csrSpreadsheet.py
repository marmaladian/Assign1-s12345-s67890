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
        print("BUILDING SPREADSHEET")
        for cell in lCells:
            print(f"trying to add {cell.val} at {cell.row}, {cell.col}")
            while not self.update(cell.row, cell.col, cell.val):
                # well, we gotta add the row or column.
                if cell.row >= self.num_rows():
                    self.appendRow()
                if cell.col >= self.num_cols:
                    self.appendCol()
        
        # HACK
        # self.suma = [0, 5, 6, 6]
        # self.cola = [0, 1, 2, 3]
        # self.vala = [5, -2, 2, 1]
        # self.num_cols = 4
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
        print(f"append row: new size is R {self.num_rows()}, C {self.num_cols}")
        return True         # why would this fail? too many rows?

    def appendCol(self):
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """
        self.num_cols += 1
        print(f"append col: new size is R {self.num_rows()}, C {self.num_cols}")
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
        if -1 <= colIndex < self.num_cols:
            for col in self.cola:
                if col > colIndex:
                    col += 1
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

        if (rowIndex >= self.num_rows()) or (colIndex >= self.num_cols):
            can_update = False
            print('row or col out of bounds')
        else:
            row_start_sum = self.suma[rowIndex] # if row > current, then return false.
            row_end_sum = self.suma[rowIndex + 1]
            cola_index, cur_sum = 0, 0
            while cur_sum < row_start_sum:
                cur_sum += self.vala[cola_index]
                cola_index += 1
            # now we are in the right part of col_a
            # just have to check if col_a has an entry of our col value, or not
            # before we go past the end of the row (the corresponding valas exceed
            # suma[rowIndex+1])
            # also need to consider if we're at the last row... need to add new row.
            while (self.cola[cola_index] != colIndex) and (cur_sum < row_end_sum):
                cur_sum += self.vala[cola_index]
                cola_index += 1
                if cur_sum >= row_end_sum:
                    self.cola.insert(cola_index - 1, colIndex)
                    self.vala.insert(cola_index - 1, value)
                    # update the rows
                    for row in range(rowIndex + 1, len(self.suma)):
                        self.suma[row] += value

                # if the value at the new cola index tips the sum over, then the value
                # needs to go in just before it.

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
        return []


    def num_rows(self) -> int:
        """
        @return Number of rows in the spreadsheet.
        """
        return len(self.suma) - 1 if self.suma else 0
    

    def print_spreadsheet(self) -> None:
        """
        Prints the spreadsheet to the terminal.
        """
        sum = 0
        vc_index = 0
        for row_sum in self.suma:
            col = 0
            while sum < row_sum:
                if col == self.cola[vc_index]:
                    value = self.vala[vc_index]
                    print(value, end='\t')
                    sum += value
                    vc_index += 1
                else:
                    print('-', end='\t')
                col += 1
            while col < self.num_cols:
                print('-', end='\t')
                col += 1
            print()
        print('---')
        print(self.cola)
        print(self.vala)
        print(self.suma)

            



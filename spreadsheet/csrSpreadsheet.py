from spreadsheet.baseSpreadsheet import BaseSpreadsheet
from spreadsheet.cell import Cell

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
        self.suma = []      # indicates the cumulative sum up to [n]th row


    def buildSpreadsheet(self, lCells: [Cell]):
        """
        Construct the data structure to store nodes.
        @param lCells: list of cells to be stored
        """

        for cell in lCells:
            success = self.update(cell.row, cell.col, cell.val)
            if not success:
                # well, we gotta add the row or column.

                pass
        print(self.cola)
        print(self.vala)
        print(self.suma)


    def appendRow(self):
        """
        Appends an empty row to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # TO BE IMPLEMENTED
        pass


    def appendCol(self):
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # TO BE IMPLEMENTED
        pass


    def insertRow(self, rowIndex: int)->bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row that will be after the newly inserted row.  If inserting as first row, specify rowIndex to be 0.  If inserting a row after the last one, specify rowIndex to be rowNum()-1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """

        # REPLACE WITH APPROPRIATE RETURN VALUE
        return True


    def insertCol(self, colIndex: int)->bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column that will be after the newly inserted row.  If inserting as first column, specify colIndex to be 0.  If inserting a column after the last one, specify colIndex to be colNum()-1.

        return True if operation was successful, or False if not, e.g., colIndex is invalid.
        """

        # REPLACE WITH APPROPRIATE RETURN VALUE
        return True



    def update(self, rowIndex: int, colIndex: int, value: float) -> bool:
        """
        Update the cell with the input/argument value.

        @param rowIndex Index of row to update.
        @param colIndex Index of column to update.
        @param value Value to update.  Can assume they are floats.

        @return True if cell can be updated.  False if cannot, e.g., row or column indices do not exist.
        """
        can_update = True

        if rowIndex >= len(self.suma):
            can_update = False
            print('row out of bounds')
        else:
            row_start_sum = self.suma[rowIndex] # if row > current, then return false.
            row_end_sum = self.suma[rowIndex + 1]
            cola_index, cur_sum = 0
            while cur_sum < row_start_sum:
                cur_sum += self.val[cola_index]
                cola_index += 1
            # now we are in the right part of col_a
            # just have to check if col_a has an entry of our col value, or not
            # before we go past the end of the row (the corresponding valas exceed
            # suma[rowIndex+1])
            # also need to consider if we're at the last row... need to add new row.
            while (self.cola[cola_index] != colIndex) and (cur_sum < row_end_sum):
                cur_sum += self.val[cola_index]
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
        return len(self.suma) - 1


    def colNum(self)->int:
        """
        @return Number of columns the spreadsheet has.
        """
        # HACK  could just store highest col seen as property of spreadsheet
        #       and update when adding/removing?
        # think this will return 0 if cola is null.
        return max(self.cola or [0])


    def find(self, value: float) -> [(int, int)]:
        """
        Find and return a list of cells that contain the value 'value'.

        @param value value to search for.

        @return List of cells (row, col) that contains the input value.
	    """

        # TO BE IMPLEMENTED

        # REPLACE WITH APPROPRIATE RETURN VALUE
        return []


    def entries(self) -> [Cell]:
        """
        return a list of cells that have values (i.e., all non None cells).
        """

        return []

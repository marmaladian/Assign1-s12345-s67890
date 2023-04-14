from spreadsheet.cell import Cell
from spreadsheet.baseSpreadsheet import BaseSpreadsheet


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Array-based spreadsheet implementation.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2023, RMIT University'
# ------------------------------------------------------------------------

class ArraySpreadsheet(BaseSpreadsheet):

    def __init__(self):
        self.spreadsheet = []

    def buildSpreadsheet(self, lCells: [Cell]):  # type: ignore
        """
        Construct the data structure to store nodes.
        @param lCells: list of cells to be stored
        """
        # look at all the cells
        # for each cell, check if the row and column are in the spreadsheet
        # if so, update the cell
        # if not, create enough rows and columns to fit the cell
        for cell in lCells:
            if cell.row >= self.rowNum() or cell.col >= self.colNum():
                while cell.row >= self.rowNum():
                    self.appendRow()
                while cell.col >= self.colNum():
                    self.appendCol()
            self.update(cell.row, cell.col, cell.val)

    def appendRow(self) -> bool:
        """
        Appends an empty row to the spreadsheet.

        @return True if operation was successful, or False if not.
        """
        if self.rowNum() == 0:
            self.spreadsheet.append([])
        else:
            self.spreadsheet.append([None] * self.colNum())
        return True

    def appendCol(self) -> bool:
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        for row in self.spreadsheet:
            row.append(None)
        return True

    def insertRow(self, rowIndex: int) -> bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row that will be after the newly inserted row.  If inserting as first row, specify rowIndex to be 0.  If inserting a row after the last one, specify rowIndex to be rowNum()-1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """

        if rowIndex < 0 or rowIndex > self.rowNum():
            return False
        if self.rowNum() == 0:
            self.spreadsheet.append([])
        else:
            self.spreadsheet.insert(rowIndex, [None] * self.colNum())
        # add one to row values of all cells below the inserted row
        i = rowIndex + 1
        while i < self.rowNum():
            for j in range(self.colNum()):
                if self.spreadsheet[i][j] is not None:
                    self.spreadsheet[i][j].row += 1
            i += 1
        return True

    def insertCol(self, colIndex: int) -> bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column that will be after the newly inserted row.  If inserting as first column, specify colIndex to be 0.  If inserting a column after the last one, specify colIndex to be colNum()-1.

        return True if operation was successful, or False if not, e.g., colIndex is invalid.
        """

        if colIndex < 0 or colIndex > self.colNum():
            return False
        for row in self.spreadsheet:
            row.insert(colIndex, None)
        # add one to col values of all cells to the right of the inserted column
        j = colIndex + 1
        while j < self.colNum():
            for i in range(self.rowNum()):
                if self.spreadsheet[i][j] is not None:
                    self.spreadsheet[i][j].col += 1
            j += 1
        return True

    def update(self, rowIndex: int, colIndex: int, value: float) -> bool:
        """
        Update the cell with the input/argument value.

        @param rowIndex Index of row to update.
        @param colIndex Index of column to update.
        @param value Value to update.  Can assume they are floats.

        @return True if cell can be updated.  False if cannot, e.g., row or column indices do not exist.
        """

        if rowIndex < 0 or rowIndex >= self.rowNum() or colIndex < 0 or colIndex >= self.colNum():
            return False
        self.spreadsheet[rowIndex][colIndex] = Cell(rowIndex, colIndex, value)
        return True

    def rowNum(self) -> int:
        """
        @return Number of rows the spreadsheet has.
        """
        return len(self.spreadsheet)

    def colNum(self) -> int:
        """
        @return Number of column the spreadsheet has.
        """
        if self.rowNum() == 0:
            return 0
        return len(self.spreadsheet[0])

    def find(self, value: float) -> [(int, int)]:  # type: ignore
        """
        Find and return a list of cells that contain the value 'value'.

        @param value value to search for.

        @return List of cells (row, col) that contains the input value.
            """
        foundCells = []
        for i in range(self.rowNum()):
            for j in range(self.colNum()):
                if self.spreadsheet[i][j] is not None and self.spreadsheet[i][j].val == value:
                    foundCells.append((i, j))
        return foundCells

    def entries(self) -> [Cell]:  # type: ignore
        """
        @return A list of cells that have values (i.e., all non None cells).
        """
        cells = []
        for i in range(self.rowNum()):
            for j in range(self.colNum()):
                if self.spreadsheet[i][j] is not None:
                    cells.append(self.spreadsheet[i][j])
        return cells

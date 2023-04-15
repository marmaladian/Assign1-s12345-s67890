from spreadsheet.baseSpreadsheet import BaseSpreadsheet
from spreadsheet.cell import Cell

# ------------------------------------------------------------------------
# This class  is required TO BE IMPLEMENTED
# Linked-List-based spreadsheet implementation.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2023, RMIT University'
# ------------------------------------------------------------------------


class Node:
    '''
    Doubly linked list node
    '''

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoubleLinkedList:
    '''
    Double linked list class
    '''

    def __init__(self):
        self.head = None
        self.tail = None

    def insertColCell(self, value):
        newNode = Node(value)

        # If the list is empty, set the new node as the head and tail
        if self.head is None:
            self.head = newNode
            self.tail = newNode
            return True

        # If the new node should be inserted at the head of the list
        if newNode.value.col < self.head.value.col:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
            return True

        # If the new node should be inserted at the tail of the list
        if newNode.value.col >= self.tail.value.col:
            newNode.prev = self.tail
            self.tail.next = newNode
            self.tail = newNode
            return True

        # Find the correct position for the new node
        current_node = self.head
        while current_node.next is not None and current_node.next.value.col < newNode.value.col:
            current_node = current_node.next

        # Insert the new node into the list
        newNode.prev = current_node
        newNode.next = current_node.next
        current_node.next.prev = newNode
        current_node.next = newNode

        return True


class LinkedListSpreadsheet(BaseSpreadsheet):

    def __init__(self):
        # initialize head node with empty cell
        self.head = Node(DoubleLinkedList())
        # tail node points to head node initially (they're the same)
        self.tail = self.head

    def buildSpreadsheet(self, lCells: [Cell]):  # type: ignore
        """
        Construct the data structure to store nodes.
        @param lCells: list of cells to be stored
        """
        # CREATE ALL ROWS
        # Create the first node in the list
        if len(lCells) > 0:
            self.head = Node(DoubleLinkedList())
            self.tail = self.head
            self.head.value.head = Node(lCells[0])
            self.head.value.tail = self.head.value.head
            lCells.pop(0)

            currRow = 0

            # Create the rest of the rows
            for cell in lCells:
                # if row is greater than the current greatest row, append a new row
                if cell.row > self.tail.value.head.value.row:
                    self.appendRow()
                # otherwise create row
                else:
                    self.createRow(cell.row)

                currNode = self.head
                currRow = self.head.value.head.value.row
                # Traverse to correct row
                while currNode is not None and currRow < cell.row:
                    currNode = currNode.next
                    currRow = currNode.value.head.value.row
                while currNode is not None and currRow > cell.row:
                    currNode = currNode.prev
                    currRow = currNode.value.head.value.row
                if currRow == cell.row:
                    # shift to correct row linked list that contains columns
                    colList = currNode.value

                    # insert column
                    colList.insertColCell(cell)

    def appendRow(self):
        """
        Appends an empty row to the spreadsheet.
        """
        # create new row and initialize it with empty cell that contains row number
        newRow = Node(DoubleLinkedList())
        emptyNodeCell = Node(
            Cell(self.rowNum(), self.colNum() - 1, None))
        newRow.value.head = emptyNodeCell
        newRow.value.tail = emptyNodeCell

        if self.head is None:
            self.head = newRow
        else:
            self.tail.next = newRow
            newRow.prev = self.tail
        self.tail = newRow
        return True

    def appendCol(self):
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # Move through row LL, appending newCol to each row
        currNode = self.head
        endCol = self.colNum()
        while currNode is not None:
            # Create node that will act as empty column
            newNode = Node(
                Cell(currNode.value.head.value.row, endCol, None))
            if currNode is None:
                return False
            currNode.value.tail.next = newNode
            newNode.prev = currNode.value.tail
            currNode.value.tail = newNode
            currNode = currNode.next
        return True

    def insertRow(self, rowIndex: int) -> bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row that will be after the newly inserted row.  If inserting as first row, specify rowIndex to be 0.  If inserting a row after the last one, specify rowIndex to be rowNum()-1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """
        if rowIndex < -1 or rowIndex >= self.tail.value.head.value.row:
            return False

        # create new row and initialize it with empty cell that contains row number
        newRow = Node(DoubleLinkedList())
        emptyNodeCell = Node(
            Cell(rowIndex, self.colNum() - 1, None))
        newRow.value.head = emptyNodeCell
        newRow.value.tail = emptyNodeCell
        # start at head
        currNode = self.head
        # if inserting as first row, set head to newRow
        if rowIndex < currNode.value.head.value.row:
            newRow.next = currNode
            currNode.prev = newRow
            self.head = newRow
        else:
            # traverse to row before insertion point
            while currNode.next is not None and rowIndex > currNode.next.value.head.value.row:
                if currNode is None:
                    return False
                currNode = currNode.next
            # loop will have overshot so insertNode.next will be current rowNode
            newRow.next = currNode.next
            currNode.next = newRow
            newRow.prev = currNode
        # update row values of all nodes after insertion point
        currNode = newRow.next
        while currNode is not None:
            colNode = currNode.value.head
            while colNode is not None:
                colNode.value.row += 1
                colNode = colNode.next
            currNode = currNode.next
        return True

    def insertCol(self, colIndex: int) -> bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column that will be before the newly inserted row.  If inserting as first column, specify colIndex to be -1.
        """
        if colIndex < -1 or colIndex >= self.tail.value.head.value.col:
            return False
        # traverse row list
        rowNode = self.head
        while rowNode is not None:
            colNode = rowNode.value.head
            # create column with current new max col and row of current row
            newCol = Node(Cell(rowNode.value.tail.value.row,
                          colIndex + 1, None))
            # add column in correct position
            insertedCol = False
            while colNode is not None:
                if colIndex < colNode.value.col and insertedCol is False:
                    # insert column
                    newCol.prev = colNode
                    newCol.next = colNode.next
                    colNode.next = newCol
                    insertedCol = True
                if insertedCol:
                    colNode.value.col += 1
                colNode = colNode.next
            # move to next row
            rowNode = rowNode.next

        return True

    def update(self, rowIndex: int, colIndex: int, value: float) -> bool:
        """
        Update the cell with the input/argument value.

        @param rowIndex Index of row to update.
        @param colIndex Index of column to update.
        @param value Value to update.  Can assume they are floats.

        @return True if cell can be updated.  False if cannot, e.g., row or column indices do not exist.
        """
        # traverse row list
        rowNode = self.head
        rowCreated = False
        while rowNode is not None:
            currRow = rowNode.value.head.value.row
            if currRow == rowIndex:
                # traverse column list
                colList = rowNode.value
                colNode = colList.head
                while colNode is not None and colNode.value.col <= colIndex:
                    if colNode.value.col == colIndex:
                        colNode.value.val = value
                        return True
                    colNode = colNode.next
                # if you're still inside the spreadsheet, create and add new column
                return colList.insertColCell(Cell(rowIndex, colIndex, value))

            # if row hasn't been created yet, but you're still inside spreadsheet, create row
            if rowCreated is False and rowNode.next is not None and rowNode.next.value.head.value.row > rowIndex:
                self.createRow(rowIndex)
                rowCreated = True

            rowNode = rowNode.next
        return False

    def rowNum(self) -> int:
        """
        @return Number of rows the spreadsheet has.
        """
        # Add one to tail row because it is 0 indexed
        return self.tail.value.head.value.row + 1

    def colNum(self) -> int:
        """
        @return Number of column the spreadsheet has.
        """
        maxCol = 0
        # traverse row list and check each row's tail col
        currNode = self.head
        while currNode is not None:
            if currNode.value.tail.value.col > maxCol:
                maxCol = currNode.value.tail.value.col
            currNode = currNode.next
        # Add one to maxCol because it is 0 indexed
        return maxCol + 1

    def find(self, value: float) -> [(int, int)]:  # type: ignore
        """
        Find and return a list of cells that contain the value 'value'.

        @param value value to search for.

        @return List of cells (row, col) that contains the input value.
            """
        foundCells = []
        # traverse every cell and check if value matches
        rowNode = self.head
        while rowNode is not None:
            colNode = rowNode.value.head
            while colNode is not None:
                if colNode.value.val == value:
                    foundCells.append((colNode.value.row, colNode.value.col))
                colNode = colNode.next
            rowNode = rowNode.next
        return foundCells

    def entries(self) -> [Cell]:  # type: ignore
        """
        @return A list of cells that have values (i.e., all non None cells).
        """
        cells = []
        # traverse every cell and check if value matches
        rowNode = self.head
        while rowNode is not None:
            colNode = rowNode.value.head
            while colNode is not None:
                if colNode.value.val is not None:
                    cells.append(colNode.value)
                colNode = colNode.next
            rowNode = rowNode.next
        return cells

    # TODO, this needs to die
    def createRow(self, rowIndex: int) -> bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row that will be after the newly inserted row.  If inserting as first row, specify rowIndex to be 0.  If inserting a row after the last one, specify rowIndex to be rowNum()-1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """
        if rowIndex < -1 or rowIndex >= self.tail.value.head.value.row:
            return False

        # create new row and initialize it with empty cell that contains row number
        newRow = Node(DoubleLinkedList())
        emptyNodeCell = Node(
            Cell(rowIndex, self.colNum() - 1, None))
        newRow.value.head = emptyNodeCell
        newRow.value.tail = emptyNodeCell
        # start at head
        currNode = self.head
        # if inserting as first row, set head to newRow
        if rowIndex < currNode.value.head.value.row:
            newRow.next = currNode
            currNode.prev = newRow
            self.head = newRow
        else:
            # traverse to row before insertion point
            while currNode.next is not None and rowIndex > currNode.next.value.head.value.row:
                if currNode is None:
                    return False
                currNode = currNode.next
            # loop will have overshot so insertNode.next will be current rowNode
            newRow.next = currNode.next
            currNode.next = newRow
            newRow.prev = currNode
        return True

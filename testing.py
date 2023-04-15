import os
import random
import timeit
from spreadsheet.cell import Cell
from spreadsheet.arraySpreadsheet import ArraySpreadsheet
from spreadsheet.linkedlistSpreadsheet import LinkedListSpreadsheet
from spreadsheet.csrSpreadsheet import CSRSpreadsheet

data_dir = 'generation'
data_file_extension = '.data'

if __name__ == '__main__':
    '''
    This script is designed to execute various operations (update, find and
    insert) and measure the execution time.
    
    This script looks for test data files in the ../generation folder then
    creates an array, doubly-linked-list and CSR spreadsheet for each of the
    data files.
    '''

    data_files = []
    test_cases = []

    def get_data_files():
        success = True
        print('Looking for data files:')
        for file in os.listdir(data_dir):
            if file.endswith(data_file_extension):
                data_files.append(file)
                print('\t', os.path.join(data_dir, file))
        if not data_files:
            print('No data files found!')
            success = False
        return success

    def create_cells_from_file(filename):
        cells = []
        values_only = []
        try:
            file = open(filename, 'r')
            for line in file:
                values = line.split()
                currRow = int(values[0])
                currCol = int(values[1])
                currVal = float(values[2])
                currCell = Cell(currRow, currCol, currVal)
                # each line contains a cell
                cells.append(currCell)
                values_only.append(float(values[2]))
            file.close()
            return (cells, values_only)
        except FileNotFoundError as e:
                print(f"Cannot find file {filename}!")


    def create_spreadsheets():
        for filename in data_files:
            (cells, values) = create_cells_from_file(data_dir + '/' + filename)

            array = ArraySpreadsheet()
            array.buildSpreadsheet(cells)

            linked_list = LinkedListSpreadsheet()
            linked_list.buildSpreadsheet(cells)

            csr = CSRSpreadsheet()
            csr.buildSpreadsheet(cells)

            test_case = {
                'filename':       filename,
                'values':         values,
                'array':          array,
                'linked_list':    linked_list,
                'csr':            csr
            }
            test_cases.append(test_case)

    def test_find(iterations):
        for test_case in test_cases:
            
            array = test_case['array']
            linked_list = test_case['linked_list']
            csr = test_case['csr']

            (_, _, _, _, max_val, _) = test_case['filename'].split('_')
            findable_value = random.choice(test_case['values'])
            not_findable_value = float(max_val) + 25

            def find_test_helper(spreadsheet, value):
                result = spreadsheet.find(value)

            print(f'testing findable values for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: find_test_helper(array, findable_value), number=iterations))
            print('ll:\t', timeit.timeit(lambda: find_test_helper(linked_list, findable_value), number=iterations))
            print('csr:\t', timeit.timeit(lambda: find_test_helper(csr, findable_value), number=iterations))
            print()

            print(f'testing unfindable values for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: find_test_helper(array, not_findable_value), number=iterations))
            print('ll:\t', timeit.timeit(lambda: find_test_helper(linked_list, not_findable_value), number=iterations))
            print('csr:\t', timeit.timeit(lambda: find_test_helper(csr, not_findable_value), number=iterations))
            print()

    def test_insert(iterations):
        for test_case in test_cases:
            (rows, cols, fill_percent, min_val, max_val, _) = test_case['filename'].split('_')

            array = test_case['array']
            linked_list = test_case['linked_list']
            csr = test_case['csr']

            last_row = int(rows) - 1
            last_col = int(cols) - 1

            def insert_row_test_helper(spreadsheet, row):
                spreadsheet.insertRow(row)
                
            def insert_col_test_helper(spreadsheet, col):
                spreadsheet.insertCol(col)

            # ROWS
            # insert row at start
            print(f'testing insert row at start for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_row_test_helper(array, 0), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_row_test_helper(linked_list, 0), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_row_test_helper(csr, 0), number=iterations))
            print()

            # insert row at end
            print(f'testing insert at last row for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_row_test_helper(array, last_row), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_row_test_helper(linked_list, last_row), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_row_test_helper(csr, last_row), number=iterations))
            print()

            # append row
            print(f'testing insert row at end (append) for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_row_test_helper(array, -1), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_row_test_helper(linked_list, -1), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_row_test_helper(csr, -1), number=iterations))
            print()
            
            # insert row in middle
            print(f'testing insert at middle-ish row for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_row_test_helper(array, last_row // 2), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_row_test_helper(linked_list, last_row // 2), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_row_test_helper(csr, last_row // 2), number=iterations))
            print()

            # insert random row
            print(f'testing insert at random row for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_row_test_helper(array, random.randint(0, last_row)), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_row_test_helper(linked_list, random.randint(0, last_row)), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_row_test_helper(csr, random.randint(0, last_row)), number=iterations))
            print()

            # COLS
            # insert col at start
            print(f'testing insert col at start for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_col_test_helper(array, 0), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_col_test_helper(linked_list, 0), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_col_test_helper(csr, 0), number=iterations))
            print()

            # insert col at end
            print(f'testing insert at last col for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_col_test_helper(array, last_col), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_col_test_helper(linked_list, last_col), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_col_test_helper(csr, last_col), number=iterations))
            print()

            # append col
            print(f'testing insert col at end (append) for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_col_test_helper(array, -1), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_col_test_helper(linked_list, -1), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_col_test_helper(csr, -1), number=iterations))
            print()
            
            # insert col in middle
            print(f'testing insert at middle-ish col for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_col_test_helper(array, last_col // 2), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_col_test_helper(linked_list, last_col // 2), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_col_test_helper(csr, last_col // 2), number=iterations))
            print()

            # insert random col
            print(f'testing insert at random col for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: insert_col_test_helper(array, random.randint(0, last_col)), number=iterations))
            print('ll:\t', timeit.timeit(lambda: insert_col_test_helper(linked_list, random.randint(0, last_col)), number=iterations))
            print('csr:\t', timeit.timeit(lambda: insert_col_test_helper(csr, random.randint(0, last_col)), number=iterations))
            print()


    def test_update(iterations):
        for test_case in test_cases:
            (rows, cols, fill_percent, min_val, max_val, _) = test_case['filename'].split('_')

            array = test_case['array']
            linked_list = test_case['linked_list']
            csr = test_case['csr']

            last_row = int(rows) - 1
            last_col = int(cols) - 1
            update_value = 55           # exact number should not matter

            def update_test_helper(spreadsheet, row, col, value):
                spreadsheet.update(row, col, value)
                # result = spreadsheet.update(row, col, value)
                # if not result:
                    # raise RuntimeError('Update should not fail in testing')


            # test random row, col
            print(f'testing random row, col update for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: update_test_helper(array, random.randint(0, last_row), random.randint(0, last_col), update_value), number=iterations))
            print('ll:\t',    timeit.timeit(lambda: update_test_helper(array, random.randint(0, last_row), random.randint(0, last_col), update_value), number=iterations))
            print('csr:\t',   timeit.timeit(lambda: update_test_helper(array, random.randint(0, last_row), random.randint(0, last_col), update_value), number=iterations))
            print()

            # test first row, first col
            print(f'testing first row, first col update for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: update_test_helper(array, 0, 0, update_value), number=iterations))
            print('ll:\t',    timeit.timeit(lambda: update_test_helper(array, 0, 0, update_value), number=iterations))
            print('csr:\t',   timeit.timeit(lambda: update_test_helper(array, 0, 0, update_value), number=iterations))
            print()

            # test last row, last col
            print(f'testing last row, last col update for {test_case["filename"]}')
            print('array:\t', timeit.timeit(lambda: update_test_helper(array, last_row, last_col, update_value), number=iterations))
            print('ll:\t',    timeit.timeit(lambda: update_test_helper(array, last_row, last_col, update_value), number=iterations))
            print('csr:\t',   timeit.timeit(lambda: update_test_helper(array, last_row, last_col, update_value), number=iterations))
            print()


    def run():
        if (get_data_files()):
            create_spreadsheets()
            # test_find(100)
            test_insert(100)
            # test_update(10000)


        




    run()
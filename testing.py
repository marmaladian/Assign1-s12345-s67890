import os
import random
import timeit
from spreadsheet.cell import Cell
from spreadsheet.arraySpreadsheet import ArraySpreadsheet
from spreadsheet.linkedlistSpreadsheet import LinkedListSpreadsheet
from spreadsheet.csrSpreadsheet import CSRSpreadsheet
from generation import dataGenerator

data_dir = 'data_files'
data_file_extension = '.data'

if __name__ == '__main__':
    '''
    This script is designed to execute various operations (update, find and
    insert) and measure the execution time.
    '''

    data_files = []
    test_cases = []
    results = []
    entries_out = []

    def remove_data_files():
        print('Removing old data files!')
        for file in os.listdir(data_dir):
            os.remove(os.path.join(data_dir, file))
    

    def get_data_files():
        success = True
        print('Looking for data files:')
        for file in os.listdir(data_dir):
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
        print('Building spreadsheets...')
        for filename in data_files:
            (cells, values) = create_cells_from_file(data_dir + '/' + filename)

            array = ArraySpreadsheet()
            array.buildSpreadsheet(cells)

            csr = CSRSpreadsheet()
            csr.buildSpreadsheet(cells)

            # building linked list last, because it pops first item from cells!
            linked_list = LinkedListSpreadsheet()
            linked_list.buildSpreadsheet(cells)


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

            print(test_case['filename'].split('_'))

            (rows, cols, fill_percent, min_val, max_val) = test_case['filename'].split('_')
            findable_value = random.choice(test_case['values'])
            not_findable_value = float(max_val) + 25

            def find_test_helper(spreadsheet, value):
                result = spreadsheet.find(value)

            data_desc = f'R {rows}, C {cols}, ~{fill_percent} filled, {iterations} iterations'

            tests = [
                ['find: existing value',        data_desc, lambda: findable_value],
                ['find: non-existing value',    data_desc, lambda: not_findable_value]
            ]

            for test in tests:
                print('executing: ', test[0])
                results.append([test[0], test[1], 'array', timeit.timeit(lambda: find_test_helper(array, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'linked_list', timeit.timeit(lambda: find_test_helper(linked_list, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'csr', timeit.timeit(lambda: find_test_helper(csr, test[2]()), number=iterations)])


    def test_insert(iterations):
        for test_case in test_cases:
            (rows, cols, fill_percent, min_val, max_val) = test_case['filename'].split('_')

            array = test_case['array']
            linked_list = test_case['linked_list']
            csr = test_case['csr']

            last_row = int(rows) - 1
            last_col = int(cols) - 1

            def insert_row_test_helper(spreadsheet, row):
                spreadsheet.insertRow(row)
                
            def insert_col_test_helper(spreadsheet, col):
                spreadsheet.insertCol(col)

            data_desc = f'R {rows}, C {cols}, ~{fill_percent} filled, {iterations} iterations'

            row_tests = [
                ['insert: row at start',        data_desc, lambda: 0],
                ['insert: row at end',          data_desc, lambda: last_row],
                ['insert: row after end',       data_desc, lambda: -1],
                ['insert: row into middle',     data_desc, lambda: last_row // 2],
                ['insert: row at random pos.',  data_desc, lambda: random.randint(0, last_row)]
            ]

            col_tests = [
                ['insert: col at start',        data_desc, lambda: 0],
                ['insert: col at end',          data_desc, lambda: last_col],
                ['insert: col after end',       data_desc, lambda: -1],
                ['insert: col into middle',     data_desc, lambda: last_col // 2],
                ['insert: col at random pos.',  data_desc, lambda: random.randint(0, last_col)]
            ]

            for test in row_tests:
                print('executing: ', test[0])
                results.append([test[0], test[1], 'array', timeit.timeit(lambda: insert_row_test_helper(array, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'linked_list', timeit.timeit(lambda: insert_row_test_helper(linked_list, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'csr', timeit.timeit(lambda: insert_row_test_helper(csr, test[2]()), number=iterations)])

            for test in col_tests:
                print('executing: ', test[0])
                results.append([test[0], test[1], 'array', timeit.timeit(lambda: insert_col_test_helper(array, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'linked_list', timeit.timeit(lambda: insert_col_test_helper(linked_list, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'csr', timeit.timeit(lambda: insert_col_test_helper(csr, test[2]()), number=iterations)])


    def test_update(iterations):
        for test_case in test_cases:
            (rows, cols, fill_percent, min_val, max_val) = test_case['filename'].split('_')

            array = test_case['array']
            linked_list = test_case['linked_list']
            csr = test_case['csr']

            last_row = int(rows) - 1
            last_col = int(cols) - 1
            update_value = 55           # exact number should not matter

            def update_test_helper(spreadsheet, row, col, value):
                spreadsheet.update(row, col, value)

            data_desc = f'R {rows}, C {cols}, ~{fill_percent} filled, {iterations} iterations'

            tests = [
                ['update: random row, random column', data_desc, lambda: random.randint(0, last_row), lambda: random.randint(0, last_col), update_value],
                ['update: first row, first column', data_desc, lambda: 0, lambda: 0, update_value],
                ['update: last row, last column', data_desc, lambda: last_row, lambda: last_col, update_value]
            ]

            for test in tests:
                print('executing: ', test[0])
                results.append([test[0], test[1], 'array', timeit.timeit(lambda: update_test_helper(array, test[2](), test[3](), update_value), number=iterations)])
                results.append([test[0], test[1], 'linked_list', timeit.timeit(lambda: update_test_helper(linked_list, test[2](), test[3](), update_value), number=iterations)])
                results.append([test[0], test[1], 'csr', timeit.timeit(lambda: update_test_helper(csr, test[2](), test[3](), update_value), number=iterations)])

    def compare_entries():
       for test_case in test_cases:
            (rows, cols, fill_percent, min_val, max_val) = test_case['filename'].split('_')

            array = test_case['array']
            linked_list = test_case['linked_list']
            csr = test_case['csr']

            data_desc = f'R {rows}, C {cols}, ~{fill_percent} filled'

            entries_out.append([data_desc, 'array', array.entries()])
            entries_out.append([data_desc, 'linked_list', linked_list.entries()])
            entries_out.append([data_desc, 'csr', csr.entries()])
            

    def run():
        # delete existing files in data directory
        remove_data_files()
        
        print('Generating new data files...')
        # create source data
        # small spreadsheets
        small = 5
        dataGenerator.dataGen(data_dir, small, small,               0.3, -100000, 100000)
        dataGenerator.dataGen(data_dir, small // 10, small * 10,    0.3, -100000, 100000)
        dataGenerator.dataGen(data_dir, small * 10, small // 10,      0.3, -100000, 100000)
        
        dataGenerator.dataGen(data_dir, small, small,               1.0, -100000, 100000)
        dataGenerator.dataGen(data_dir, small // 10, small * 10,    1.0, -100000, 100000)
        dataGenerator.dataGen(data_dir, small * 10, small // 10,    1.0, -100000, 100000)

        # medium spreadsheets
        medium = 250
        dataGenerator.dataGen(data_dir, medium, medium,             0.3, -100000, 100000)
        dataGenerator.dataGen(data_dir, medium // 10, medium * 10,  0.3, -100000, 100000)
        dataGenerator.dataGen(data_dir, medium * 10, medium // 10,  0.3, -100000, 100000)
        
        dataGenerator.dataGen(data_dir, medium, medium,             1.0, -100000, 100000)
        dataGenerator.dataGen(data_dir, medium // 10, medium * 10,  1.0, -100000, 100000)
        dataGenerator.dataGen(data_dir, medium * 10, medium // 10,  1.0, -100000, 100000)

        # large spreadsheets
        large = 500
        dataGenerator.dataGen(data_dir, large, large,               0.3, -100000, 100000)
        dataGenerator.dataGen(data_dir, large // 10, large * 10,    0.3, -100000, 100000)
        dataGenerator.dataGen(data_dir, large * 10, large // 10,    0.3, -100000, 100000)
        
        dataGenerator.dataGen(data_dir, large, large,               1.0, -100000, 100000)
        dataGenerator.dataGen(data_dir, large // 10, large * 10,    1.0, -100000, 100000)
        dataGenerator.dataGen(data_dir, large * 10, large // 10,    1.0, -100000, 100000)

        if (get_data_files()):
            create_spreadsheets()
            # # test_find(100)
            # # test_insert(100)
            # # test_update(100)

        print(f'{len(results)} tests completed.')
        print('---------------------------------------------------------------------------------------------------------------------------------')
        for result in results:
            print(f'{result[0]:40}\t{result[1]:30}\t{result[2]:10}\t{result[3]}')

        # compare_entries()
        # for entry in entries_out:
        #     print(f'{entry[0]:40}\t{entry[1]:30}')
        #     for entry in entry[2]:
        #         print(entry, end='\t')
        #     print()

    run()
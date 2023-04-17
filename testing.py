import os
import random
import time
import timeit
import csv
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
            print(f'\t- {filename}')
            (cells, values) = create_cells_from_file(data_dir + '/' + filename)
            print('\t\tarray...')
            array = ArraySpreadsheet()
            array.buildSpreadsheet(cells)
            print('\t\tcsr...')
            csr = CSRSpreadsheet()
            csr.buildSpreadsheet(cells)
            print('\t\tlinked list...')
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
                print('executing: ', test[0], '\t', test[1])
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
                print('executing: ', test[0], '\t', test[1])
                results.append([test[0], test[1], 'array', timeit.timeit(lambda: insert_row_test_helper(array, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'linked_list', timeit.timeit(lambda: insert_row_test_helper(linked_list, test[2]()), number=iterations)])
                results.append([test[0], test[1], 'csr', timeit.timeit(lambda: insert_row_test_helper(csr, test[2]()), number=iterations)])

            for test in col_tests:
                print('executing: ', test[0], '\t', test[1])
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
                print('executing: ', test[0], '\t', test[1])
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
            

    def generate_data_files():
        print('Generating new data files...')

        sizes = [10, 32, 100, 316, 1000]
        densities = [0.33, 0.66, 1.0]
        (min_val, max_val) = [-100000, 1000000]

        for sz in sizes:
            for density in densities:
                dataGenerator.dataGen(data_dir, sz, sz,             density, min_val, max_val)
                dataGenerator.dataGen(data_dir, sz // 10, sz  * 10, density, min_val, max_val)
                dataGenerator.dataGen(data_dir, sz  * 10, sz // 10, density, min_val, max_val)       

    def run():
        remove_data_files()
        generate_data_files()
    
        print('Starting tests...')

        if (get_data_files()):
            create_spreadsheets()
            test_find(100)
            test_insert(100)
            test_update(100)
            
        # create a new file for writing
        t = str(time.time())
        with open(f'results_{t}.csv', mode='w', newline='') as results_file:
            results_writer = csv.writer(results_file, delimiter=',')

            # write the header row
            results_writer.writerow(['implementation', 'action', 'num_rows', 'num_cols', 'filled', 'time'])

            print(f'{len(results)} tests completed.')
            print('---------------------------------------------------------------------------------------------------------------------------------')
            for result in results:
                print(f'{result[0]:35}\t{result[1]:35}\t{result[2]:>10}\t{result[3]}') 
            
                # write results to csv file
                # split result[1] (data description) into num_rows, num_cols, percentage filled
                data_details = result[1].split()
                results_writer.writerow([result[2], result[0], int(data_details[1][:-1]), int(data_details[3][:-1]), float(data_details[4][1:]), float(result[3])])

        # compare_entries()
        # for entry in entries_out:
        #     print(f'{entry[0]:40}\t{entry[1]:30}')
        #     for entry in entry[2]:
        #         print(entry, end='\t')
        #     print()

    for _ in range (0, 10):
        run()
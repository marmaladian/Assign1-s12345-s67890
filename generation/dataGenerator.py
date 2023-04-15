import random
import sys

if __name__ == '__main__':
    '''
    dataGen generates a text file of spreadsheet values
    filename is in the format: numRows_numCols_filled_lowVal_highVal_distribution
    run from the command line with the following arguments:

    @param numCols: the number of columns
    @param numRows: the number of rows
    @param filled: fill probability (0.0 - 1.0)
    @param lowVal: the lowest possible value in the spreadsheet
    @param highVal: the highest possible value in the spreadsheet
    '''
    # Fetch the command line arguments
    args = sys.argv

    def dataGen(numRows, numCols, filled, lowVal, highVal):
        # Create a file for writing
        with open(str(numRows) + '_' + str(numCols) + '_' + str(filled) + '_' + str(lowVal) + '_' + str(highVal), 'w') as file:

            # Loop through each cell in the spreadsheet
            for row in range(numRows):
                for col in range(numCols):
                    # Fill probability
                    if random.random() < filled:
                        # Generate a randomised value
                        value = round(random.uniform(lowVal, highVal),
                                      random.randint(0, 5))

                        # Write the row, column, and value to the file
                    file.write(f'{row} {col} {value}\n')

    # call the function:
    dataGen(int(args[1]), int(args[2]), float(args[3]),
            int(args[4]), int(args[5]))

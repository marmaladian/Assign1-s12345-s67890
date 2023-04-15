import random
import sys

if __name__ == '__main__':
    '''
    dataGen generates a text file of spreadsheet values
    filename is in the format: numRows_numCols_filled_lowVal_highVal_distribution
    run from the command line with the following arguments:

    @param numRows: the number of rows
    @param numCols: the number of columns
    @param filled: fill probability (0.0 - 1.0)
    @param lowVal: the lowest possible value in the spreadsheet
    @param highVal: the highest possible value in the spreadsheet
    @param distribution: the distribution of the values in the spreadsheet (uniform, normal)
    '''
    # Fetch the command line arguments
    args = sys.argv

    def dataGen(numRows, numCols, filled, lowVal, highVal, distribution):
        # Create a file for writing
        with open(str(numRows) + '_' + str(numCols) + '_' + str(filled) + '_' + str(lowVal) + '_' + str(highVal) + '_' + distribution + '.data', 'w') as file:

            # Loop through each cell in the spreadsheet
            for row in range(numRows):
                for col in range(numCols):
                    # Fill probability
                    if random.random() < filled:
                        # Generate a value for this cell based on the distribution
                        if distribution == 'uniform':
                            value = round(random.uniform(lowVal, highVal),
                                          random.randint(0, 5))
                        elif distribution == 'normal':
                            value = round(random.normalvariate(
                                lowVal, highVal), random.randint(0, 5))
                        else:
                            raise ValueError('Invalid distribution')

                        # Write the row, column, and value to the file
                        file.write(f'{row} {col} {value}\n')

    # call the function:
    dataGen(int(args[1]), int(args[2]), float(args[3]),
            int(args[4]), int(args[5]), args[6])

import random

if __name__ == '__main__':
    '''
    dataGen generates a text file of spreadsheet values

    @param size: the size of the spreadsheet
    @param filled: the percentage of the spreadsheet that is filled
    @param valRange: the range of values in the spreadsheet
    @param distribution: the distribution of the values in the spreadsheet (uniform, normal)
    '''
    def dataGen(size, filled, valRange, distribution):
        # Create a file for writing
        with open('sampleSpreadsheet.txt', 'x') as file:
            # Calculate the number of cells to fill
            numCells = int(size * size * filled)

            # Loop through each cell in the spreadsheet
            for row in range(numCells):
                for col in range(numCells):
                    # Fill probability
                    if random.random() < filled:
                        # Generate a value for this cell based on the distribution
                        if distribution == 'uniform':
                            value = round(random.uniform(-valRange, valRange),
                                          random.randint(0, 5))
                        elif distribution == 'normal':
                            value = round(random.normalvariate(
                                -valRange, valRange), random.randint(0, 5))
                        else:
                            raise ValueError('Invalid distribution')

                        # Write the row, column, and value to the file
                        file.write(f'{row} {col} {value}\n')

    dataGen(10, 0.1, 100, 'uniform')

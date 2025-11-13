rows = 0
cols = 0
visited = set()
outputStrings = []
score = 0
numOfMoves = 0
inputNum = 0

class cluster:
    def __init__(self, color, indices):
        self.color = color
        self.indices = indices
    
    def toString(self):
        return self.indices
    
def calcScore(moveSize):
    global score
    score += pow(moveSize-1, 2)
    
def findCluster(grid, i, j, color):
    cluster = []
    thisCell = grid[i][j]

    if (i+1, j+1) not in visited:
        visited.add((i+1, j+1))
        cluster.append((i+1, j+1))

    up = i > 0 and grid[i-1][j] == thisCell
    down = i < rows-1 and grid[i+1][j] == thisCell
    left = j > 0 and grid[i][j-1] == thisCell
    right = j < cols-1 and grid[i][j+1] == thisCell

    if not (left or up or right or down):
        return cluster

    if up and (i, j+1) not in visited:
        subClust = findCluster(grid, i-1, j, color)
        for index in subClust:
            cluster.append(index)
    if down and (i+2, j+1) not in visited:
        subClust = findCluster(grid, i+1, j, color)
        for index in subClust:
            cluster.append(index)
    if left and (i+1, j) not in visited:
        subClust = findCluster(grid, i, j-1, color)
        for index in subClust:
            cluster.append(index)
    if right and (i+1, j+2) not in visited:
        subClust = findCluster(grid, i, j+1, color)
        for index in subClust:
            cluster.append(index)
    return cluster

def getClusters(grid):
    global visited
    clusters = []
    for i in range(0, rows):
        for j in range(0, cols):
            if(i+1, j+1) not in visited and grid[i][j] != 0:
                thisClust = findCluster(grid, i, j, grid[i][j])
                clusters.append(cluster(grid[i][j], thisClust))
    visited = set()
    return clusters

def checkIfValidMoves(clusters):
    for cluster in clusters:
        if len(cluster.indices) > 1:
            return True
        
def findBiggestCluster(clusters, grid):
    biggestCluster, bestScore = clusters[0], -10**9
    for cl in clusters:
        k = len(cl.indices)
        score = (k - 1) ** 2
        test = [row[:] for row in grid]
        updateGrid(test, cl)
        empties = sum(1 for j in range(cols) if test[rows - 1][j] == 0)
        score += 2 * empties
        if score > bestScore:
            biggestCluster, bestScore = cl, score
    return biggestCluster

def clearCol(grid, col):
    currentCol = col
    while currentCol < cols -1:
        for i in range(0, rows):
            right = grid[i][currentCol + 1]
            grid[i][currentCol] = right
        currentCol += 1
    for i in range(0, rows):
        grid[i][currentCol] = 0
    return grid

def updateGrid(grid, removedCluster):
    indices = sorted(removedCluster.indices)
    for index in indices:
        row = index[0] - 1
        col = index[1] - 1
        while row > 0:
            above = grid[row-1][col]
            if above == 0:
                break
            grid[row][col] = above
            row -= 1
        grid[row][col] = 0
    bottomRow = rows -1
    for i in range(0, cols):
        if grid[bottomRow][i] == 0:
            grid = clearCol(grid, i)
            if grid[bottomRow][i] == 0:
                grid = clearCol(grid, i)
            
    return grid




def solver(grid):
    global numOfMoves
    global outputStrings
    clusters = getClusters(grid)
    while len(clusters) > 0 and checkIfValidMoves(clusters):
        bestMove = findBiggestCluster(clusters, grid)
        grid = updateGrid(grid, bestMove)
        numOfMoves += 1
        moveSize = len(bestMove.indices)
        moveInd = bestMove.indices[0]
        moveColor = bestMove.color
        calcScore(moveSize)
        outputStr = f"{moveColor} {moveSize} {rows - (moveInd[0]-1)} {moveInd[1]}"
        outputStrings.append(outputStr)
        clusters = getClusters(grid)

def takeInput():
    global rows
    global cols
    global inputNum
    grid = []
    inputNum = input("Which input would you like to run?  ")
    with open(f"input_group{inputNum}.txt", 'r') as file:
        for line in file:
            if ' ' in line:
                sizeInp = line.split(' ')
                rows = int(sizeInp[0])
                cols = int(sizeInp[1])
            else:
                currentRow = []
                for j in range(0, cols):
                    currentRow.append(int(line[j]))
                grid.append(currentRow)
    
    return grid

def main():
    grid = takeInput()

    solver(grid)

    with open(f"output_group{inputNum}.txt", 'w') as file:
        file.write(f"{score}\n")
        file.write(f"{numOfMoves}")
        for i in range(numOfMoves):
            file.write("\n")
            file.write(outputStrings[i])

    # print(score)
    # print(numOfMoves)
    



if __name__ == "__main__":
    main()

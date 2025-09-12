level1 = [[1,0,5,0,3,0,4,0,9],
        [0,3,0,0,0,5,0,1,0],
        [2,0,8,0,6,0,7,0,5],
        [0,0,0,8,0,2,0,9,0],
        [9,0,4,0,1,0,6,0,2],
        [0,5,0,4,0,6,0,8,0],
        [5,0,6,0,8,0,9,0,7],
        [0,7,0,6,0,9,0,5,0],
        [3,0,9,0,5,0,1,0,8]]

def start(problem):
    possibilities = [[[] for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if problem[i][j] == 0:
                possibilities[i][j] = [1,2,3,4,5,6,7,8,9]
            else:
                possibilities[i][j] = [problem[i][j]]
    return possibilities

def print_board(board):
    for i in range(9):
        print(board[i])

def tate_yoko(possibilities):
    new_possibilities = [row[:] for row in possibilities]
    for i in range(9):
        for j in range(9):
            if len(new_possibilities[i][j]) == 1:
                num = new_possibilities[i][j][0]
                for k in range(9):
                    if k != j and num in new_possibilities[i][k]:
                        new_possibilities[i][k].remove(num)
                    if k != i and num in new_possibilities[k][j]:
                        new_possibilities[k][j].remove(num)
    return new_possibilities

def print_answer(possibilities):
    answer = []
    for i in range(9):
        row = []
        for j in range(9):
            num = possibilities[i][j][0] if len(possibilities[i][j]) == 1 else 0
            row.append(num)
        answer.append(row)
    print_board(answer)


if __name__ == "__main__":
    possibilities = start(level3)
    print_board(level3)
    print_board(possibilities)

    new_possibilities = tate_yoko(possibilities)
    while True:
        new_possibilities = tate_yoko(new_possibilities)
        if new_possibilities == possibilities:
            break
    print("tate_yoko_done")
    print_board(new_possibilities)
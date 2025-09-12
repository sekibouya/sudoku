import copy
import question

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

def tate_yoko_sikaku(possibilities):
    new_possibilities = copy.deepcopy(possibilities)
    for i in range(9):
        for j in range(9):
            if len(new_possibilities[i][j]) == 1:
                num = new_possibilities[i][j][0]
                for k in range(9):
                    if k != j and num in new_possibilities[i][k]:
                        new_possibilities[i][k].remove(num)
                    if k != i and num in new_possibilities[k][j]:
                        new_possibilities[k][j].remove(num)
                box_row = (i // 3)
                box_col = (j // 3)
                for m in range(box_row * 3, box_row * 3 + 3):
                    for n in range(box_col * 3, box_col * 3 + 3):
                        if num in new_possibilities[m][n] and not (m == i and n == j):
                            new_possibilities[m][n].remove(num)
    return new_possibilities

def check_only_one_sikaku(possibilities):
    new_possibilities = copy.deepcopy(possibilities)
    for box_row in range(3):
        for box_col in range(3):
            counts = {num: 0 for num in range(1, 10)}
            positions = {num: [] for num in range(1, 10)}
            
            for x in range(box_row*3, box_row*3+3):
                for y in range(box_col*3, box_col*3+3):
                    for num in new_possibilities[x][y]:
                        counts[num] += 1
                        positions[num].append((x, y))
            for num, count in counts.items():
                if count == 1:
                    x, y = positions[num][0]
                    if len(new_possibilities[x][y]) > 1:
                        new_possibilities[x][y] = [num]
    return new_possibilities

def check_only_one_tate_yoko(possibilities):
    new_possibilities = copy.deepcopy(possibilities)
    for i in range(9):
        for j in range(9):
            if len(new_possibilities[i][j]) > 1:
                for num in new_possibilities[i][j]:
                    only_in_tate = [num not in new_possibilities[k][j] for k in range(9) if k != i]
                    only_in_yoko = [num not in new_possibilities[i][k] for k in range(9) if k != j]
                    if all(only_in_tate) or all(only_in_yoko):
                        new_possibilities[i][j] = [num]
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


def solve(board):
    possibilities = start(board)
    while True:
        new_possibilities = tate_yoko_sikaku(possibilities)
        new_possibilities = check_only_one_sikaku(new_possibilities)
        new_possibilities = check_only_one_tate_yoko(new_possibilities)
        if new_possibilities == possibilities:
            break
        possibilities = new_possibilities
    # print_answer(new_possibilities)
    print(possibilities)

if __name__ == "__main__":
    for i,level in enumerate(question.questions):
        print(f"level{i+1}-------------------------")
        for problem in level:
            solve(problem)
            print()
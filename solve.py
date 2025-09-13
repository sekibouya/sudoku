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

def check_common(possibilities):
    new_possibilities = copy.deepcopy(possibilities)
    # possibilities[i][j]の配列の要素集合が、横、縦、四角の中で、その配列の要素集合と等しければ、same_cellsに(i,j)を追加
    # same_cellsの長さと、配列の要素集合の長さが等しければ、same_cellsに含まれないセルから、配列の要素集合の要素を削除
    for i in range(9):
        for j in range(9):
            if len(new_possibilities[i][j]) > 1:
                current_set = set(new_possibilities[i][j])

                # column
                same_cells = []
                same_cells.append((i, j))
                for col in range(9):
                    if col != j and set(new_possibilities[i][col]) == current_set and len(new_possibilities[i][col]) == len(current_set):
                        same_cells.append((i, col))
                if len(same_cells)  == len(current_set):
                    for num in current_set:
                        for col in range(9):
                            if (i, col) not in same_cells and num in new_possibilities[i][col]:
                                new_possibilities[i][col].remove(num)
                
                # row
                same_cells = []
                same_cells.append((i, j))
                for row in range(9):
                    if row != i and set(new_possibilities[row][j]) == current_set and len(new_possibilities[row][j]) == len(current_set) and (row, j) not in same_cells:
                        same_cells.append((row, j))
                if len(same_cells)  == len(current_set):
                    for num in current_set:
                        for row in range(9):
                            if (row, j) not in same_cells and num in new_possibilities[row][j]:
                                new_possibilities[row][j].remove(num)

                # box
                same_cells = []
                same_cells.append((i, j))
                box_row = (i // 3)
                box_col = (j // 3)
                for m in range(box_row * 3, box_row * 3 + 3):
                    for n in range(box_col * 3, box_col * 3 + 3):
                        if (m, n) != (i, j) and set(new_possibilities[m][n]) == current_set and len(new_possibilities[m][n]) == len(current_set) and (m, n) not in same_cells:
                            same_cells.append((m, n))
                if len(same_cells)  == len(current_set):
                    for num in current_set:
                        for m in range(box_row * 3, box_row * 3 + 3):
                            for n in range(box_col * 3, box_col * 3 + 3):
                                if (m, n) not in same_cells and num in new_possibilities[m][n]:
                                    new_possibilities[m][n].remove(num)
                    
    return new_possibilities

def sikaku_to_tate_yoko(possibilities):
    new_possibilities = copy.deepcopy(possibilities)
    for box_row in range(3):
        for box_col in range(3):
            positions = {num: [] for num in range(1, 10)}
            
            for x in range(box_row*3, box_row*3+3):
                for y in range(box_col*3, box_col*3+3):
                    for num in new_possibilities[x][y]:
                        positions[num].append((x, y))
            for num, pos in positions.items():
                if len(pos) > 1:
                    xlist = [x for (x, _) in pos]
                    ylist = [y for (_, y) in pos]
                    if len(set(ylist)) <= 1:
                        col = ylist[0]
                        for row in range(9):
                            if row < box_row*3 or row >= box_row*3+3:
                                if num in new_possibilities[row][col]:
                                    new_possibilities[row][col].remove(num)
                    if len(set(xlist)) <= 1:
                        row = xlist[0]
                        for col in range(9):
                            if col < box_col*3 or col >= box_col*3+3:
                                if num in new_possibilities[row][col]:
                                    new_possibilities[row][col].remove(num)
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

def print_possibilities(possibilities):
    for i in range(9):
        print(possibilities[i])


def solve(board):
    possibilities = start(board)
    while True:
        new_possibilities = tate_yoko_sikaku(possibilities)
        new_possibilities = check_only_one_sikaku(new_possibilities)
        new_possibilities = check_only_one_tate_yoko(new_possibilities)
        new_possibilities = check_common(new_possibilities)
        new_possibilities = sikaku_to_tate_yoko(new_possibilities)
        if new_possibilities == possibilities:
            break
        possibilities = new_possibilities
    return new_possibilities

if __name__ == "__main__":
    for i,level in enumerate(question.questions):
        print(f"level{i+1}-------------------------")
        for problem in level:
            # print_answer(new_possibilities)
            # print(new_possibilities)
            print_possibilities(solve(problem))
            print()
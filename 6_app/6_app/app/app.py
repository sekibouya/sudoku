import copy
import random
from flask import Flask, render_template, request

import app.question as questions

questions=questions.questions
number_of_level = len(questions)

# Flaskオブジェクトの生成
app = Flask(__name__)

# 数独の初期盤面 (定数として定義)
INITIAL_BOARD = [
    [1, 0, 5, 0, 3, 0, 4, 0, 9],
    [0, 3, 0, 0, 0, 5, 0, 1, 0],
    [2, 0, 8, 0, 6, 0, 7, 0, 5],
    [0, 0, 0, 8, 0, 2, 0, 9, 0],
    [9, 0, 4, 0, 1, 0, 6, 0, 2],
    [0, 5, 0, 4, 0, 6, 0, 8, 0],
    [5, 0, 6, 0, 8, 0, 9, 0, 7],
    [0, 7, 0, 6, 0, 9, 0, 5, 0],
    [3, 0, 9, 0, 5, 0, 1, 0, 8]
]

# 盤面の履歴を保存するリスト
# 最初の要素として初期盤面を格納
board_history = [copy.deepcopy(INITIAL_BOARD)]
# 履歴のどの位置を表示しているかを示すインデックス
history_index = 0

@app.route("/")
def index():
    ########################################
    #   メインページを表示用
    ########################################
    global board_history, history_index, number_of_level
    
    # 現在のインデックスにある盤面を表示
    current_board = board_history[history_index]
    
    return render_template("index.html", question=current_board, text="", number_of_level=number_of_level)

@app.route("/change", methods=["POST"])
def change():
    ########################################
    #   入力による更新用
    ########################################
    global board_history, history_index, number_of_level

    # フォームからデータを受け取る
    number_str = request.form.get("number")
    cell_position_str = request.form.get("place")

    # 現在の盤面をテンプレートに渡すために取得
    current_board = board_history[history_index]

    # 空入力の場合、エラーメッセージを表示
    if not number_str or not cell_position_str:
        error_message = "エラー: 数字と配置する場所の両方を選択してください。"
        return render_template("index.html", question=current_board, text=error_message, number_of_level=number_of_level)

    try:
        number = int(number_str)
        cell_position = int(cell_position_str)
        # 座標を計算　(2桁の数字の文字列)
        row = cell_position // 10
        col = cell_position % 10
    except (ValueError, TypeError):
        error_message = "エラー: 無効な入力です。"
        return render_template("index.html", question=current_board, text=error_message, number_of_level=number_of_level)

    # undo操作後に新しい手を指した場合、それ以降の履歴を削除
    if history_index < len(board_history) - 1:
        board_history = board_history[:history_index + 1]

    # 現在の盤面をコピーして新しい盤面を作成
    new_board = copy.deepcopy(current_board)
    # 盤面を更新
    new_board[row][col] = number
    
    # 新しい盤面を履歴に追加
    board_history.append(new_board)
    # 履歴インデックスを最新の状態に進める
    history_index = len(board_history) - 1

    return render_template("index.html", question=board_history[history_index], text="数字を配置しました。", number_of_level=number_of_level)

@app.route("/undo")
def undo():
    ########################################
    #   盤面の状態を一つ戻す用　(Ctrl + Z)
    ########################################
    global history_index, number_of_level
    
    message = ""
    if history_index > 0:
        history_index -= 1
        message = "一つ元に戻しました。"
    else:
        message = "これ以上元に戻せません。"
        
    current_board = board_history[history_index]
    return render_template("index.html", question=current_board, text=message, number_of_level=number_of_level)

@app.route("/redo")
def redo():
    ########################################
    #   undoをやり直す用　(Ctrl + Y)
    ########################################
    global history_index, number_of_level
    
    message = ""
    if history_index < len(board_history) - 1:
        history_index += 1
        message = "一つやり直しました。"
    else:
        message = "これ以上やり直せません。"
        
    current_board = board_history[history_index]
    return render_template("index.html", question=current_board, text=message, number_of_level=number_of_level)

@app.route("/reset")
def reset():
    ########################################
    #  初期化用
    ########################################
    global board_history, history_index, number_of_level
    
    # 履歴とインデックスを初期状態に戻す
    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    
    return render_template("index.html", question=board_history[0], text="ゲームをリセットしました。", number_of_level=number_of_level)

@app.route("/answer")
def answer():
    ########################################
    #  解答生成
    ########################################
    global board_history, history_index, number_of_level

    # 現在の盤面をテンプレートに渡すために取得
    current_board = board_history[history_index]

    # 現在の盤面をコピーして新しい盤面を作成
    new_board = copy.deepcopy(current_board)
    # 盤面を更新
    new_board[row][col] = number
    ########################################
    #  def　auto_answer(board):みたいな関数
    #
    #  answer_board = auto_answer(new_board)
    ########################################
    
    # 新しい盤面を履歴に追加
    board_history.append(new_board)
    # 履歴インデックスを最新の状態に進める
    history_index = len(board_history) - 1

    return render_template("index.html", question=board_history[history_index], text="解答生成", number_of_level=number_of_level)

@app.route("/level1")
def level1():
    global questions, INITIAL_BOARD, board_history, history_index
    level = questions[0]
    INITIAL_BOARD = random.choice(level)

    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    return render_template("index.html", question=board_history[history_index], text="Level 1", number_of_level=number_of_level)

@app.route("/level2")
def level2():
    global questions, INITIAL_BOARD, board_history, history_index
    level = questions[1]
    INITIAL_BOARD = random.choice(level)

    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    return render_template("index.html", question=board_history[history_index], text="Level 2", number_of_level=number_of_level)

@app.route("/level3")
def level3():
    global questions, INITIAL_BOARD, board_history, history_index
    level = questions[2]
    INITIAL_BOARD = random.choice(level)

    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    return render_template("index.html", question=board_history[history_index], text="Level 3", number_of_level=number_of_level)

@app.route("/level4")
def level4():
    global questions, INITIAL_BOARD, board_history, history_index
    level = questions[3]
    INITIAL_BOARD = random.choice(level)

    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    return render_template("index.html", question=board_history[history_index], text="Level 4", number_of_level=number_of_level)

@app.route("/level5")
def level5():
    global questions, INITIAL_BOARD, board_history, history_index
    level = questions[4]
    INITIAL_BOARD = random.choice(level)

    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    return render_template("index.html", question=board_history[history_index], text="Level 5", number_of_level=number_of_level)

@app.route("/level6")
def level6():
    global questions, INITIAL_BOARD, board_history, history_index
    level = questions[5]
    INITIAL_BOARD = random.choice(level)

    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    return render_template("index.html", question=board_history[history_index], text="Level 6", number_of_level=number_of_level)

@app.route("/level7")
def level7():
    global questions, INITIAL_BOARD, board_history, history_index
    level = questions[6]
    INITIAL_BOARD = random.choice(level)

    board_history = [copy.deepcopy(INITIAL_BOARD)]
    history_index = 0
    return render_template("index.html", question=board_history[history_index], text="Level 7", number_of_level=number_of_level)



if __name__ == "__main__":
    app.run(debug=True)
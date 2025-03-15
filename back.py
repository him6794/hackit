KEYWORDS = {'加上', '減去', '乘以', '除以', '取模', '等於', '大於', '小於', '轉型'}
COMMANDS = {'要求在終端機（或控制台）輸出': (lambda x: print(evaluate(x))),
            '設定一指定名稱變數的值，名稱與值分別為': (lambda x: assign_variable(x)),
            '初始化一個指定名稱和長度的陣列，名稱和長度分別為': (lambda x: init_array(x)),
            '設定指定名稱陣列其中一項的值，名稱、項數與值分別為': (lambda x: assign_array(x)),
            '讀取使用者輸入字串，並儲存至變數': (lambda x: get_user_input(x))}
IF = '如果右方判斷式結果為真，執行以下特定操作'
WHILE = '重複並持續驗證右方表達式之真實性，條件滿足時持續執行特定操作'
BREAK = '無視迴圈判斷式要求，直接跳脫迴圈'
CONTINUE = '捨棄以下迴圈內容，直接繼續下一輪迴圈'
EXIT = '無視所有指令，直接退出程式'

variables = {}
arrays = {}

def assign_variable(expression: str):
    global variables
    split_result = expression.split('，')
    if split_result[0][0] != '「' or split_result[0][-1] != '」' or len(split_result[0]) == 2:
        raise ValueError('變數名稱有誤：'+split_result[0])
    variables[split_result[0][1:-1]] = evaluate(split_result[1])

def init_array(expression: str):
    global arrays
    split_result = expression.split('，')
    if split_result[0][0] != '「' or split_result[0][-1] != '」' or len(split_result[0]) == 2:
        raise ValueError('陣列名稱有誤：' + split_result[0])
    arrays[split_result[0][1:-1]] = [None for _ in range(evaluate(split_result[1]))]


def assign_array(expression: str):
    global arrays
    split_result = expression.split('，')
    if split_result[0][0] != '「' or split_result[0][-1] != '」' or len(split_result[0]) == 2:
        raise ValueError('陣列名稱有誤：'+split_result[0])
    arrays[split_result[0][1:-1]][int(evaluate(split_result[1]))] = evaluate(split_result[2])


def get_user_input(variable: str):
    global variables
    if variable[0] != '「' or variable[-1] != '」' or len(variable) == 2:
        raise ValueError('變數名稱有誤：'+variable)
    variables[variable[1:-1]] = input('')

def precedence(op):
    if op == '等於' or op == '大於' or op == '小於':
        return 1
    if op == '加上' or op == '減去':
        return 2
    if op == '乘以' or op == '除以' or op == '取模':
        return 3
    if op == '轉型':
        return 4
    return 0


def apply(a, b, op):
    if op == '加上':
        return a + b
    if op == '減去':
        return a - b
    if op == '乘以':
        if type(a) == type(""):
            return a * int(b)
        return a * b
    if op == '除以':
        return a / b
    if op == '取模':
        return a % b
    if op == '等於':
        return int(a == b)
    if op == '大於':
        return int(a > b)
    if op == '小於':
        return int(a < b)
    if op == '轉型':
        if b == '數字':
            return int(a)
        elif b == '字串':
            return str(a)
        else:
            raise ValueError('未知型態：'+b)


def evaluate(expression: str):
    ops = []
    values = []
    i = 0
    while i < len(expression):
        if expression[i] == ' ' or expression[i] == '　':
            pass
        elif expression[i] == '（':
            ops.append(expression[i])
        elif expression[i] == '）':
            while len(ops) != 0 and ops[-1] != '（':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(apply(val1, val2, op))
            ops.pop()
        elif expression[i].isdigit() or expression[i] == '.' or expression[i] == '-':
            val = ''
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.' or expression[i] == '-'):
                val += expression[i]
                i += 1
            i -= 1
            values.append(float(val))
        elif expression[i] == '「':
            token = ''
            i += 1
            while expression[i] != '」':
                token += expression[i]
                i += 1
            values.append(token)
        elif expression[i:i + 3] == '變數「':
            token = ''
            i += 3
            while expression[i] != '」':
                token += expression[i]
                i += 1
            values.append(variables[token])

        elif expression[i:i + 3] == '陣列「':
            token = ''
            i += 3
            while expression[i] != '」':
                token += expression[i]
                i += 1
            i += 1
            if expression[i:i + 4] != '的索引（':
                raise ValueError('未知的算式：' + expression)
            i += 4
            tmp_exp = ''
            stk = 1
            while i < len(expression):
                if expression[i] == '（':
                    stk += 1
                elif expression[i] == '）':
                    stk -= 1
                tmp_exp += expression[i]
                i += 1
                if stk == 0:
                    break
            i -= 1
            values.append(arrays[token][int(evaluate(tmp_exp[:-1]))])
        else:
            if expression[i:i + 2] not in KEYWORDS:
                raise ValueError('未知的運算子：' + expression[i])
            while len(ops) != 0 and precedence(ops[-1]) >= precedence(expression[i:i + 2]):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(apply(val1, val2, op))
            ops.append(expression[i:i + 2])
            i += 1
        i += 1
    while len(ops) != 0:
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        values.append(apply(val1, val2, op))
    final = values[-1]
    if type(final) == type(1.0) and final % 1.0 == 0:
        return int(final)
    return final


def run_command(command: str):
    for i in COMMANDS.keys():
        if command[:len(i)] == i:
            COMMANDS[i](command[len(i):])
            return
    raise ValueError('未知指令：'+command)


def get_clause(lines: list[str], start_line: int):
    j = start_line
    stk = 1
    while stk > 0:
        j += 1
        if lines[j][:len(IF)] == IF or lines[j][:len(WHILE)] == WHILE:
            stk += 1
        elif lines[j] == '結束以上判斷式或迴圈':
            stk -= 1
    return j


def exec_separate_lines(lines: list[str]):
    i = 0
    while i < len(lines):
        if lines[i] == BREAK:
            return -1
        if lines[i] == CONTINUE:
            return -2
        if lines[i] == EXIT:
            return 0
        if lines[i][:len(IF)] == IF:
            j = get_clause(lines, i)
            if evaluate(lines[i][len(IF):]):
                ret = exec_separate_lines(lines[i+1:j])
                if ret is not None:
                    return ret
            i = j
        elif lines[i][:len(WHILE)] == WHILE:
            j = get_clause(lines, i)
            while evaluate(lines[i][len(WHILE):]):
                ret = exec_separate_lines(lines[i+1:j])
                if ret == -1:
                    break
                if ret == 0:
                    return 0
            i = j
        else:
            run_command(lines[i])
        i += 1


def execute(lines: str):
    split_lines = lines.split('\n')
    split_code = []
    for i in split_lines:
        stripped = i.strip()
        if stripped == '':
            continue
        if stripped[-1] != '。':
            raise ValueError('你忘了加句點。')
        split_code.append(stripped[:-1])
    exec_separate_lines(split_code)

if __name__ == '__main__':
    code = '''
設定一指定名稱變數的值，名稱與值分別為「i」，0。
重複並持續驗證右方表達式之真實性，條件滿足時持續執行特定操作（變數「i」小於10）。
要求在終端機（或控制台）輸出「執行第 」加上變數「i」轉型「字串」加上「 次」。
設定一指定名稱變數的值，名稱與值分別為「i」，變數「i」加上1。
結束以上判斷式或迴圈。
        '''

    execute(code)
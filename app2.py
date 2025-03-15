import sys
import back
from flask import Flask, request, jsonify, send_from_directory
from io import StringIO
from multiprocessing import Process, Queue
import time

app = Flask(__name__, template_folder='templates')
sessions = {}  # 存放執行中的程式狀態

class InputNeeded(Exception):
    """ 自定義異常，用於標記需要輸入的情況 """
    pass

class InputMock:
    """ 模擬 input() 來攔截 back.py 的輸入 """
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue  # 用於接收主進程的輸入
        self.output_queue = output_queue  # 用於通知主進程需要輸入
    
    def readline(self):
        """ 模擬 input()，若無輸入則通知主進程並等待 """
        self.output_queue.put({"needsInput": True})
        user_input = self.input_queue.get()  # 等待主進程提供輸入
        return user_input + '\n'

def run_in_process(session_id, code, input_queue, output_queue):
    """ 在子進程中執行程式碼 """
    sys.stdin = InputMock(input_queue, output_queue)
    sys.stdout = StringIO()
    try:
        executor = back.Executor()
        executor.execute(code)
        output = sys.stdout.getvalue()
        output_queue.put({"output": output, "completed": True})
    except InputNeeded:
        output = sys.stdout.getvalue()
        output_queue.put({"output": output, "needsInput": True})
    except Exception as e:
        output_queue.put({"output": str(e), "completed": True})
    finally:
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index2.html')

@app.route('/run', methods=['POST'])
def run_code():
    """ 開始執行程式 """
    session_id = str(len(sessions))  # 產生唯一的 session ID
    input_queue = Queue()  # 子進程接收輸入的隊列
    output_queue = Queue()  # 子進程發送結果的隊列

    # 儲存會話資訊
    sessions[session_id] = {
        "code": request.json['code'],
        "output": "",
        "input_queue": input_queue,
        "output_queue": output_queue,
        "completed": False
    }

    # 啟動子進程
    process = Process(target=run_in_process, args=(session_id, sessions[session_id]["code"], input_queue, output_queue))
    sessions[session_id]["process"] = process
    process.start()

    # 等待子進程的初步結果
    result = output_queue.get()
    sessions[session_id]["output"] += result.get("output", "")
    if result.get("completed", False):
        sessions[session_id]["completed"] = True
        process.join()  # 清理已完成的進程
        del sessions[session_id]["process"]

    return jsonify({
        "sessionId": session_id,
        "output": sessions[session_id]["output"],
        "needsInput": result.get("needsInput", False)
    })

@app.route('/submit_input', methods=['POST'])
def submit_input():
    """ 接收使用者的輸入並繼續執行 """
    session_id = request.json['sessionId']
    user_input = request.json['input']

    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 400

    session = sessions[session_id]
    session["input_queue"].put(user_input)  # 將輸入發送到子進程

    # 等待子進程的結果
    result = session["output_queue"].get()
    session["output"] += result.get("output", "")

    if result.get("completed", False):
        session["completed"] = True
        session["process"].join()  # 清理進程
        del session["process"]

    return jsonify({
        "sessionId": session_id,
        "output": session["output"],
        "needsInput": result.get("needsInput", False)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=False)  # 使用多進程時不需要 threaded=True

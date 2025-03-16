const runButton = document.getElementById('runCodeButton');
const triangleExampleButton = document.getElementById('triangleExampleButton');
const quadraticExampleButton = document.getElementById('quadraticExampleButton');
const twentyOneExampleButton = document.getElementById('twentyOneExampleButton'); // 新增按鈕
const editor = document.getElementById('codeEditor');
const result = document.getElementById('executionResult');
const inputSection = document.getElementById('inputSection');
const userInput = document.getElementById('userInput');
const submitInput = document.getElementById('submitInput');
const API_BASE_URL = "http://10.219.58.131:5000"; // 指定 API 伺服器的 IP 和端口
let sessionId = null;
// 三角形範例程式碼
const triangleExampleCode = `
要求在終端機（或控制台）輸出「輸入三角形的三邊長（以換行隔開）：」。
讀取使用者輸入字串，並儲存至變數「a」。
設定一指定名稱變數的值，名稱與值分別為「a」，變數「a」轉型「數字」。
讀取使用者輸入字串，並儲存至變數「b」。
設定一指定名稱變數的值，名稱與值分別為「b」，變數「b」轉型「數字」。
讀取使用者輸入字串，並儲存至變數「c」。
設定一指定名稱變數的值，名稱與值分別為「c」，變數「c」轉型「數字」。
設定一指定名稱變數的值，名稱與值分別為「i」，0。
重複並持續驗證右方表達式之真實性，條件滿足時持續執行特定操作（1）。
如果右方判斷式結果為真，執行以下特定操作（變數「a」大於變數「b」）。
設定一指定名稱變數的值，名稱與值分別為「t」，變數「a」。
設定一指定名稱變數的值，名稱與值分別為「a」，變數「b」。
設定一指定名稱變數的值，名稱與值分別為「b」，變數「t」。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作（變數「i」大於1）。
無視迴圈判斷式要求，直接跳脫迴圈。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作（變數「b」大於變數「c」）。
設定一指定名稱變數的值，名稱與值分別為「t」，變數「b」。
設定一指定名稱變數的值，名稱與值分別為「b」，變數「c」。
設定一指定名稱變數的值，名稱與值分別為「c」，變數「t」。
結束以上判斷式或迴圈。
設定一指定名稱變數的值，名稱與值分別為「i」，變數「i」加上1。
結束以上判斷式或迴圈。
要求在終端機（或控制台）輸出「排序後的三邊長：」。
要求在終端機（或控制台）輸出變數「a」轉型「字串」加上「 」加上變數「b」轉型「字串」加上「 」加上變數「c」轉型「字串」加上「 」。
如果右方判斷式結果為真，執行以下特定操作 1 減去（變數「a」加上變數「b」大於變數「c」）。
要求在終端機（或控制台）輸出「不構成三角形。」。
無視所有指令，直接退出程式。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作（變數「a」乘以變數「a」加上變數「b」乘以變數「b」等於變數「c」乘以變數「c」）。
要求在終端機（或控制台）輸出「直角三角形。」。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作（變數「a」乘以變數「a」加上變數「b」乘以變數「b」小於變數「c」乘以變數「c」）。
要求在終端機（或控制台）輸出「鈍角三角形。」。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作（變數「a」乘以變數「a」加上變數「b」乘以變數「b」大於變數「c」乘以變數「c」）。
要求在終端機（或控制台）輸出「銳角三角形。」。
結束以上判斷式或迴圈。
`.trim();

// 一元二次方程式範例程式碼
const quadraticExampleCode = `
要求在終端機（或控制台）輸出「請輸入 x^2 項係數 ，此項必須不為 0」。
讀取使用者輸入字串，並儲存至變數「a」。
設定一指定名稱變數的值，名稱與值分別為「a」，變數「a」轉型「數字」。
如果右方判斷式結果為真，執行以下特定操作（變數「a」等於 0）。
要求在終端機（或控制台）輸出「使用者輸入錯誤，導致 RE 」。
無視所有指令，直接退出程式。
結束以上判斷式或迴圈。
要求在終端機（或控制台）輸出「請輸入 x 項係數」。
讀取使用者輸入字串，並儲存至變數「b」。
設定一指定名稱變數的值，名稱與值分別為「b」，變數「b」轉型「數字」。
要求在終端機（或控制台）輸出「請輸入常數項係數」。
讀取使用者輸入字串，並儲存至變數「c」。
設定一指定名稱變數的值，名稱與值分別為「c」，變數「c」轉型「數字」。
如果右方判斷式結果為真，執行以下特定操作 （變數「b」 乘以 變數「b」 大於 4 乘以 變數「a」 乘以 變數「c」）。
要求在終端機（或控制台）輸出「方程式有兩個相異的實數解」。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作 （變數「b」 乘以 變數「b」 等於 4 乘以 變數「a」 乘以 變數「c」）。
要求在終端機（或控制台）輸出「方程式有兩個一樣的實數解」。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作 （變數「b」 乘以 變數「b」 小於 4 乘以 變數「a」 乘以 變數「c」）。
要求在終端機（或控制台）輸出「方程式有兩個虛數解」。
結束以上判斷式或迴圈。
`.trim();

// 搶21點範例程式碼
const twentyOneExampleCode = `
要求在終端機（或控制台）輸出「搶 21 遊戲，玩家先手，每次可選擇 1~3」。
要求在終端機（或控制台）輸出「輪到玩家，目前剩下 21 」。
設定一指定名稱變數的值，名稱與值分別為「x」，21。
讀取使用者輸入字串，並儲存至變數「a」。
設定一指定名稱變數的值，名稱與值分別為「a」，變數「a」轉型「數字」。
重複並持續驗證右方表達式之真實性，條件滿足時持續執行特定操作（（變數「a」小於 4）加上（變數「a」大於 0）加上 （變數「x」減去 變數「a」加上 1 大於 0）小於 3）。
要求在終端機（或控制台）輸出「輸入無效，請重新輸入」。
讀取使用者輸入字串，並儲存至變數「a」。
設定一指定名稱變數的值，名稱與值分別為「a」，變數「a」轉型「數字」。
結束以上判斷式或迴圈。
設定一指定名稱變數的值，名稱與值分別為「x」，變數「x」減去 變數「a」。
設定一指定名稱變數的值，名稱與值分別為「p」，1。

重複並持續驗證右方表達式之真實性，條件滿足時持續執行特定操作（變數「x」大於 0）。
設定一指定名稱變數的值，名稱與值分別為「e」，0。
如果右方判斷式結果為真，執行以下特定操作（變數「x」取模 4 等於 0）。
要求在終端機（或控制台）輸出「電腦選擇 2 」。
設定一指定名稱變數的值，名稱與值分別為「x」，變數「x」減去 2。
設定一指定名稱變數的值，名稱與值分別為「e」，1。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作（變數「e」等於 0）。
設定一指定名稱變數的值，名稱與值分別為「c」，變數「x」取模 4。
要求在終端機（或控制台）輸出（「電腦選擇 」加上（變數「c」轉型 「字串」））。
設定一指定名稱變數的值，名稱與值分別為「x」，變數「x」減去 變數「c」。
設定一指定名稱變數的值，名稱與值分別為「p」，0。
結束以上判斷式或迴圈。
如果右方判斷式結果為真，執行以下特定操作（變數「x」等於 0）。
要求在終端機（或控制台）輸出「電腦獲勝」。
無視所有指令，直接退出程式。
結束以上判斷式或迴圈。
要求在終端機（或控制台）輸出（「輪到玩家，目前剩下 」加上（變數「x」轉型「字串」））。
讀取使用者輸入字串，並儲存至變數「a」。
設定一指定名稱變數的值，名稱與值分別為「a」，變數「a」轉型「數字」。
重複並持續驗證右方表達式之真實性，條件滿足時持續執行特定操作（（變數「a」小於 4）加上（變數「a」大於 0）加上 （變數「x」減去 變數「a」加上 1 大於 0）小於 3）。
要求在終端機（或控制台）輸出「輸入無效，請重新輸入」。
讀取使用者輸入字串，並儲存至變數「a」。
設定一指定名稱變數的值，名稱與值分別為「a」，變數「a」轉型「數字」。
結束以上判斷式或迴圈。
設定一指定名稱變數的值，名稱與值分別為「x」，變數「x」減去 變數「a」。
設定一指定名稱變數的值，名稱與值分別為「p」，1。
如果右方判斷式結果為真，執行以下特定操作（變數「x」等於 0）。
要求在終端機（或控制台）輸出「玩家獲勝」。
無視所有指令，直接退出程式。
結束以上判斷式或迴圈。
結束以上判斷式或迴圈。
`.trim();

// 執行按鈕事件
runButton.addEventListener('click', async () => {
    const code = editor.value;
    runButton.disabled = true;
    runButton.textContent = '執行中...';
    result.textContent = '';
    inputSection.style.display = 'none';

    try {
        const response = await fetch('/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });

        const resultData = await response.json();
        sessionId = resultData.sessionId;

        // 開始輪詢狀態
        pollStatus();
    } catch (error) {
        result.textContent = '前端請求錯誤或連線失敗。';
        resetButton();
    }
});
// 新增強制結束按鈕事件
stopButton.addEventListener('click', async () => {
    if (!sessionId) {
        result.textContent = '目前沒有執行中的程式。';
        return;
    }

    try {
        const response = await fetch('/stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sessionId })
        });

        if (response.ok) {
            result.textContent += '\n程式已強制終止。';
            resetButton();
        } else {
            result.textContent += '\n終止程式失敗。';
        }
    } catch (error) {
        result.textContent += '\n終止請求失敗：' + error.message;
    }
});

// 輪詢狀態
const pollStatus = async () => {
    if (!sessionId) return;

    try {
        const response = await fetch(`/status/${sessionId}`);
        const data = await response.json();

        if (data.error) {
            result.textContent = data.error;
            resetButton();
            return;
        }

        if (data.output) {
            result.textContent += data.output;
        }

        if (data.needsInput) {
            inputSection.style.display = 'block';
            userInput.focus();
        } else if (data.completed) {
            resetButton();
        } else {
            setTimeout(pollStatus, 300); // 繼續輪詢
        }
    } catch (error) {
        result.textContent = '狀態輪詢失敗。';
        resetButton();
    }
};

// 提交輸入事件
submitInput.addEventListener('click', async () => {
    const inputValue = userInput.value.trim();
    if (!inputValue || !sessionId) {
        alert('請輸入內容或確保 sessionId 存在');
        return;
    }

    try {
        const response = await fetch('/submit_input', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sessionId, input: inputValue })
        });

        if (!response.ok) {
            throw new Error('提交輸入失敗');
        }

        userInput.value = ''; // 清空輸入框
        pollStatus(); // 繼續輪詢狀態
    } catch (error) {
        result.textContent += '\n輸入處理失敗：' + error.message;
    }
});

// 三角形範例按鈕事件
triangleExampleButton.addEventListener('click', () => {
    editor.value = triangleExampleCode;
    result.textContent = '已載入三角形範例程式，請點擊「執行程式碼」運行。';
    editor.focus();
});

// 一元二次方程式範例按鈕事件
quadraticExampleButton.addEventListener('click', () => {
    editor.value = quadraticExampleCode;
    result.textContent = '已載入一元二次方程式範例程式，請點擊「執行程式碼」運行。';
    editor.focus();
});

// 搶21點範例按鈕事件
twentyOneExampleButton.addEventListener('click', () => {
    editor.value = twentyOneExampleCode;
    result.textContent = '已載入搶21點範例程式，請點擊「執行程式碼」運行。';
    editor.focus();
});

// 重置按鈕狀態
const resetButton = () => {
    runButton.disabled = false;
    runButton.textContent = '執行程式碼 ▶';
    sessionId = null;
};
# server.py
from flask import Flask, request, jsonify, render_template_string
import threading

app = Flask(__name__)

# متنی که قراره بین کلاینت‌ها به اشتراک گذاشته بشه
shared_text = "این متن اولیه است."
text_lock = threading.Lock() # برای اطمینان از دسترسی امن به shared_text

# HTML/JS برای فرانت‌اند
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-time Text Sync (Polling)</title>
    <style>
        body { font-family: sans-serif; background-color: #1e1e1e; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { text-align: center; background-color: #2a2a2a; padding: 30px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
        textarea { width: 400px; height: 200px; margin-bottom: 15px; padding: 10px; border: 1px solid #555; border-radius: 5px; background-color: #333; color: #fff; font-size: 16px; resize: none; }
        .controls button { margin: 5px; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; background-color: #007bff; color: white; font-size: 14px; }
        .controls button:hover { background-color: #0056b3; }
        .controls button#resetBtn { background-color: #dc3545; }
        .controls button#resetBtn:hover { background-color: #c82333; }
        #status { margin-top: 10px; color: #aaa; font-size: 12px;}
    </style>
</head>
<body>
    <div class="container">
        <h1>همگام‌سازی متن</h1>
        <textarea id="textEditor"></textarea>
        <div class="controls">
            <button id="copyBtn">کپی کردن</button>
            <button id="resetBtn">ریست کردن</button>
        </div>
        <div id="status">در حال اتصال...</div>
    </div>

    <script>
        const textEditor = document.getElementById('textEditor');
        const statusDiv = document.getElementById('status');
        let lastKnownText = '';
        const POLLING_INTERVAL = 2000; // هر ۲ ثانیه چک کن

        // تابع برای گرفتن آخرین متن از سرور
        async function fetchText() {
            try {
                const response = await fetch('/get_text');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data.text !== lastKnownText) {
                    textEditor.value = data.text;
                    lastKnownText = data.text;
                    statusDiv.textContent = `آخرین به‌روزرسانی: ${new Date().toLocaleTimeString()}`;
                }
            } catch (error) {
                console.error('خطا در دریافت متن:', error);
                statusDiv.textContent = 'خطا در اتصال به سرور.';
                // اینجا می‌تونی کاری کنی که مثلاً هر ۳۰ ثانیه دوباره سعی کنه
            }
        }

        // تابع برای ارسال متن به سرور
        async function sendText() {
            const currentText = textEditor.value;
            if (currentText !== lastKnownText) { // فقط اگر تغییری بود بفرست
                 try {
                    const response = await fetch('/update_text', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: currentText }),
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.json();
                    if (data.success) {
                        lastKnownText = currentText; // به‌روزرسانی متن شناخته شده
                        statusDiv.textContent = 'متن با موفقیت به‌روز شد!';
                        console.log("Text updated successfully");
                    } else {
                         statusDiv.textContent = 'خطا در به‌روزرسانی متن.';
                    }
                } catch (error) {
                    console.error('خطا در ارسال متن:', error);
                    statusDiv.textContent = 'خطا در ارسال متن.';
                }
            }
        }

        // تابع برای کپی کردن متن
        document.getElementById('copyBtn').addEventListener('click', () => {
            textEditor.select();
            document.execCommand('copy');
            statusDiv.textContent = 'متن کپی شد!';
        });

        // تابع برای ریست کردن متن
        document.getElementById('resetBtn').addEventListener('click', async () => {
             try {
                const response = await fetch('/reset_text', { method: 'POST' });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data.success) {
                    textEditor.value = data.text; // نمایش متن ریست شده
                    lastKnownText = data.text;
                    statusDiv.textContent = 'متن ریست شد!';
                } else {
                    statusDiv.textContent = 'خطا در ریست کردن متن.';
                }
            } catch (error) {
                console.error('خطا در ریست کردن متن:', error);
                statusDiv.textContent = 'خطا در ریست کردن متن.';
            }
        });

        // رویداد هنگام تغییر متن در textarea
        textEditor.addEventListener('input', sendText);

        // شروع Polling برای دریافت به‌روزرسانی‌ها
        setInterval(fetchText, POLLING_INTERVAL);

        // بارگذاری اولیه متن هنگام شروع
        fetchText();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_text', methods=['GET'])
def get_text():
    with text_lock:
        return jsonify({'text': shared_text})

@app.route('/update_text', methods=['POST'])
def update_text():
    global shared_text
    data = request.get_json()
    new_text = data.get('text')
    if new_text is not None:
        with text_lock:
            shared_text = new_text
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'No text provided'}), 400

@app.route('/reset_text', methods=['POST'])
def reset_text():
    global shared_text
    with text_lock:
        shared_text = "" # متن ریست شده
    return jsonify({'success': True, 'text': shared_text})

if __name__ == '__main__':
    # برای شبکه لوکال، host='0.0.0.0' رو بذار تا از دستگاه‌های دیگه هم قابل دسترس باشه
    # پورت رو هم می‌تونی عوض کنی
    app.run(host='0.0.0.0', port=5000, debug=True)

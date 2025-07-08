from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # 用來讓 session 可以記住資料（正式部署要改掉）

def generate_answer():
    digits = random.sample(range(10), 4)
    return [str(d) for d in digits]

def evaluate(guess, answer):
    A = sum(g == a for g, a in zip(guess, answer))
    B = sum(min(guess.count(d), answer.count(d)) for d in set(guess)) - A
    return A, B

@app.route("/", methods=["GET", "POST"])
def game():
    if "answer" not in session:
        session["answer"] = generate_answer()
        session["attempts"] = 0
        session["history"] = []

    result = ""
    if request.method == "POST":
        guess = request.form["guess"]
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) < 4:
            result = "❌ 請輸入 4 個不重複的數字！"
        else:
            session["attempts"] += 1
            A, B = evaluate(guess, session["answer"])
            feedback = f"{guess} → {A}A{B}B"
            session["history"].append(feedback)
            if A == 4:
                result = f"✅ 恭喜！你猜對了！答案是 {''.join(session['answer'])}，共猜了 {session['attempts']} 次。"
                session.clear()  # 清掉遊戲狀態
            else:
                result = feedback

    return render_template("index.html", result=result, history=session.get("history", []))

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
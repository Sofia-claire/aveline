from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def integer():
    message = ''  # исправлена опечатка в названии переменной
    
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        message = message + user + ' ' + password  
        return render_template("proba.html", message=message)  # передаем message в шаблон
    
    return render_template('proba.html', message="...")

if __name__ == "__main__":
    print("run server")
    app.run()
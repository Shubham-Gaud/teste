from flask import *
from send import *


app = Flask(__name__)


@app.route('/')
def upload():
    return render_template("b.html")

@app.route('/contact')
def contact():
    return render_template("file_upload_form.html")

@app.route('/about')
def about():
    return render_template("a.html")

@app.route('/op', methods=['GET','POST'])
def op():
    if request.method == 'POST':
        email = request.form.get("fname")
        pwd = request.form.get("lname")
        displayname = request.form.get("le")
        f = request.files['file']
        f.save('data.csv')
        f = request.files['filee']
        f.save('compose.md')
        send(email, pwd, displayname)

        return render_template("success.html", name=f.filename)



if __name__ == "__main__":
    app.run()

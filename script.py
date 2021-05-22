from flask import *
import TextVisualizations as txtv
import HelperTools as ht
import ExtractiveTextSum as ets
import ATS as ats
import webbasedsearch as wbs
app = Flask(__name__)

txt = ""


@app.route('/file_upload_form', methods=['GET', 'POST'])
def file_upload_form():
    return render_template("file_upload_form.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        local_txt = ht.text_file(f.filename)
        global txt
        txt = local_txt
        txtv.run(local_txt)

        return render_template("visualizations.html")


@app.route('/')
def message():
    return render_template('message.html')


@app.route('/inserttext', methods=['GET', 'POST'])
def inserttext():
    return render_template('inserttext.html')


@app.route('/keywords', methods=['GET', 'POST'])
def keywords():
    data = ht.get_keywords(txt)
    return render_template('keywords.html', data=data, context=txt)


@app.route('/keyphrases', methods=['GET', 'POST'])
def keyphrases():
    data = ht.get_keyphrases(txt)
    return render_template('keyphrases.html', data=data, context=txt)


@app.route('/insertlink', methods=['GET', 'POST'])
def insertlink():
    return render_template('insertlink.html')


@app.route('/submit', methods=['POST'])
def submit():
    with open("C://Users//bhaskar//Desktop//FYP//new//static//summary.html", "w", encoding="utf-8") as f:
        f.write(ets.Word_weight(request.form['text']))
    global txt
    txt = request.form['text']
    txtv.run(request.form['text'])
    return render_template("visualizations.html")


@app.route('/submitlink', methods=['POST'])
def submitlink():
    got_the_text = ht.get_text_from_link(request.form['text'])
    with open("C://Users//bhaskar//Desktop//FYP//new//static//summary.html", "w", encoding="utf-8") as f:
        f.write(ets.Word_weight(got_the_text))
    global txt
    txt = request.form['text']
    txtv.run(got_the_text)
    return render_template("visualizations.html")


# --------------------------------------------------------------------------------------------------------------------#
@app.route('/file_upload_formats', methods=['GET', 'POST'])
def file_upload_formats():
    return render_template("file_upload_formats.html")


@app.route('/successats', methods=['POST'])
def successats():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        local_txt = ht.text_file(f.filename)
        global txt
        txt = local_txt
        txtv.run(local_txt)

        return render_template("visualizations.html")


@app.route('/inserttextats', methods=['GET', 'POST'])
def inserttextats():
    return render_template('inserttextats.html')


@app.route('/insertlinkats', methods=['GET', 'POST'])
def insertlinkats():
    return render_template('insertlinkats.html')


@app.route('/submitats', methods=['POST'])
def submitats():
    with open("C://Users//bhaskar//Desktop//FYP//new//static//summary.html", "w", encoding="utf-8") as f:
        f.write(ats.at_sum(request.form['text']))
    global txt
    txt = request.form['text']
    txtv.run(request.form['text'])
    return render_template("visualizations.html")


@app.route('/submitlinkats', methods=['POST'])
def submitlinkats():
    got_the_text = ht.get_text_from_link(request.form['text'])
    with open("C://Users//bhaskar//Desktop//FYP//new//static//summary.html", "w", encoding="utf-8") as f:
        f.write(ats.at_sum(got_the_text))
    global txt
    txt = request.form['text']
    txtv.run(got_the_text)
    return render_template("visualizations.html")


# -----------------------------------------------------------------------------------------------------------#
@app.route('/answering', methods=['GET', 'POST'])
def answering():
    quest = request.form['prasna']
    con = request.form['nepadyam']
    ans = ats.question_answering(quest, con)
    return render_template("Question_Answering.html", question=quest, answer=ans, context=con)


@app.route('/question_answering', methods=['GET', 'POST'])
def question_answering():
    return render_template("Question_Answering.html")


@app.route('/file_upload_formds', methods=['GET', 'POST'])
def file_upload_formds():
    return render_template("file_upload_formds.html")


@app.route('/successds', methods=['POST'])
def successds():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        local_txt = ht.text_file(f.filename)
        return render_template("Question_Answering.html", context=local_txt)


@app.route('/inserttextds', methods=['GET', 'POST'])
def inserttextds():
    return render_template('inserttextds.html')


@app.route('/insertlinkds', methods=['GET', 'POST'])
def insertlinkds():
    return render_template('insertlinkds.html')


@app.route('/submitds', methods=['POST'])
def submitds():
    txt = request.form['text']
    return render_template("Question_Answering.html", context=txt)


@app.route('/submitlinkds', methods=['POST'])
def submitlinkds():
    got_the_text = ht.get_text_from_link(request.form['text'])
    return render_template("Question_Answering.html", context=got_the_text)


@app.route('/successws', methods=['POST'])
def successws():
    txt = request.form['description']
    output=wbs.mainu(txt)
    return render_template("websearch.html", data=output)


@app.route('/websearch', methods=['GET','POST'])
def websearch():

    return render_template("websearch.html")



if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
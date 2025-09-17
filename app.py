from flask import Flask, render_template, request, jsonify, send_file
from ytvideo_to_epub import ytvideo_to_epub

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        yt_url = request.form['yt_url']

        try:
            name, epub_file = ytvideo_to_epub(yt_url, mv_to_gdrive=False)
        except Exception as error:
            return jsonify(str(error)), 400

        return send_file(
            epub_file,
            mimetype='application/epub+zip',
            as_attachment=True,
            download_name=name,
        )
    return render_template(
        'index.html',
        yt_url=request.args.get('url', ''),
    )


if __name__ == '__main__':
    app.run(debug=True)

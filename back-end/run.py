from flaskapi import app

if __name__== '__main__':
    # threaded to allow serving to multiple clients at once
    app.run(threaded=True, debug=True)
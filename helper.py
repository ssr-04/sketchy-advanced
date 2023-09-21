from flask import render_template
import pyqrcode
import png

def file_check(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
    filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def apology(msg, code=400):

  def escape(s):
    """
    Escape special characters.
    """
    for old, new in [("-", "--"), (" ", "-"), ("_",       "__"), ("?", "~q"),("%", "~p"), ("#", "~h"),       ("/", "~s"), ("\"", "''")]:
      s = s.replace(old, new)
      return s

  return render_template("apology.html",top = code, bottom = escape(msg))

def popup(error,msg):
    return render_template("popup.html",error = error,msg = msg)

def qr_code(url):
  my_qr = pyqrcode.create(url)
  my_qr.png("./static/images/Qrcode.png",scale=9)
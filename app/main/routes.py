from app.main import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html')

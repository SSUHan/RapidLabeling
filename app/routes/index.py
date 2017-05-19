from app import rc_app

@rc_app.route('/')
def index_page():
	return 'Hello World!'
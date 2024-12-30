from config import app
from blueprints import rs_bp, factory_bp

app.register_blueprint(rs_bp)
app.register_blueprint(factory_bp)
if __name__ == '__main__':
    app.run(debug=True, port=8080)

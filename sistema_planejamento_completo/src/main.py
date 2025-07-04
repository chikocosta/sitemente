import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from flask_cors import CORS
from datetime import datetime
import json

# Importar módulos do sistema
try:
    from routes.atividades import atividades_bp
    from routes.atividades_aprimoradas import atividades_aprimoradas_bp
    from routes.planejamento import planejamento_bp
    from routes.adaptacoes import adaptacoes_bp
except ImportError:
    # Fallback se os módulos não existirem
    from flask import Blueprint
    atividades_bp = Blueprint('atividades', __name__)
    atividades_aprimoradas_bp = Blueprint('atividades_aprimoradas', __name__)
    planejamento_bp = Blueprint('planejamento', __name__)
    adaptacoes_bp = Blueprint('adaptacoes', __name__)

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'clube_mente_planejamento_2025'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

# Registrar blueprints
app.register_blueprint(planejamento_bp, url_prefix='/planejamento')
app.register_blueprint(atividades_bp, url_prefix='/atividades')
app.register_blueprint(atividades_aprimoradas_bp, url_prefix='/atividades_aprimoradas')
app.register_blueprint(adaptacoes_bp, url_prefix='/adaptacoes')

@app.route('/')
def home():
    """Página principal do sistema de planejamento - redireciona para sistema aprimorado"""
    return redirect(url_for('atividades_aprimoradas.index'))

@app.route('/dashboard')
def dashboard():
    """Dashboard principal para professores"""
    return render_template('dashboard.html')

@app.route('/atividades')
def atividades_index():
    """Página de geração de atividades"""
    return render_template('atividades/index.html')

@app.route('/adaptacoes')
def adaptacoes_index():
    """Página de adaptações para neurotípicos e neuroatípicos"""
    return render_template('adaptacoes/index.html')

@app.route('/planejamento')
def planejamento_index():
    """Página de planejamento de aulas"""
    return render_template('planejamento/index.html')

@app.route('/relatorios')
def relatorios_index():
    """Página de relatórios e acompanhamento"""
    return render_template('relatorios.html')

@app.route('/perfil')
def perfil():
    """Página de perfil do professor"""
    return render_template('perfil.html')

@app.route('/turmas')
def turmas():
    """Página de gerenciamento de turmas"""
    return render_template('turmas.html')

@app.route('/biblioteca')
def biblioteca():
    """Biblioteca de recursos educacionais"""
    return render_template('biblioteca.html')

@app.route('/configuracoes')
def configuracoes():
    """Página de configurações do sistema"""
    return render_template('configuracoes.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


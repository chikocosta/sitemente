#!/usr/bin/env python3
"""
Sistema Completo de Planejamento Educacional
Clube da Mente - 2025

Sistema integrado para professores do ensino fundamental com:
- Gerador de atividades baseado em evidências científicas
- Planejamento de aulas personalizado
- Adaptações para neurodiversidade
- Relatórios e acompanhamento
"""

import os
import sys

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app

if __name__ == '__main__':
    print("🌟 Iniciando Sistema Completo de Planejamento Educacional")
    print("📚 Clube da Mente - Educação Personalizada")
    print("🌐 Acesse: http://localhost:5000")
    print("=" * 50)
    
    # Configurações de desenvolvimento
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Iniciar servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )


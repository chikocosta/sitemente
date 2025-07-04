from flask import Blueprint, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime, timedelta
from fpdf import FPDF
import unicodedata

planejamento_bp = Blueprint('planejamento', __name__)

# Estrutura curricular baseada na BNCC
ESTRUTURA_BNCC = {
    "educacao_infantil": {
        "campos_experiencia": {
            "eu_outro_nos": {
                "nome": "O eu, o outro e o nós",
                "objetivos": [
                    "EI03EO01 - Demonstrar empatia pelos outros",
                    "EI03EO02 - Agir de maneira independente",
                    "EI03EO03 - Ampliar as relações interpessoais",
                    "EI03EO04 - Comunicar suas ideias e sentimentos",
                    "EI03EO05 - Demonstrar valorização das características de seu corpo",
                    "EI03EO06 - Manifestar interesse e respeito por diferentes culturas",
                    "EI03EO07 - Usar estratégias pautadas no respeito mútuo"
                ]
            },
            "corpo_gestos_movimentos": {
                "nome": "Corpo, gestos e movimentos",
                "objetivos": [
                    "EI03CG01 - Criar com o corpo formas diversificadas de expressão",
                    "EI03CG02 - Demonstrar controle e adequação do uso de seu corpo",
                    "EI03CG03 - Criar movimentos, gestos e mímicas",
                    "EI03CG04 - Adotar hábitos de autocuidado",
                    "EI03CG05 - Coordenar suas habilidades manuais"
                ]
            },
            "tracos_sons_cores_formas": {
                "nome": "Traços, sons, cores e formas",
                "objetivos": [
                    "EI03TS01 - Utilizar sons produzidos por materiais e objetos",
                    "EI03TS02 - Expressar-se por meio da linguagem musical",
                    "EI03TS03 - Reconhecer as qualidades do som"
                ]
            },
            "escuta_fala_pensamento_linguagem": {
                "nome": "Escuta, fala, pensamento e linguagem",
                "objetivos": [
                    "EI03EF01 - Expressar ideias, desejos e sentimentos",
                    "EI03EF02 - Inventar brincadeiras cantadas",
                    "EI03EF03 - Escolher e folhear livros",
                    "EI03EF04 - Recontar histórias ouvidas",
                    "EI03EF05 - Recontar histórias ouvidas para produção de reconto escrito",
                    "EI03EF06 - Produzir suas próprias histórias orais e escritas",
                    "EI03EF07 - Levantar hipóteses sobre gêneros textuais",
                    "EI03EF08 - Selecionar livros e textos de gêneros conhecidos",
                    "EI03EF09 - Levantar hipóteses em relação à linguagem escrita"
                ]
            },
            "espacos_tempos_quantidades": {
                "nome": "Espaços, tempos, quantidades, relações e transformações",
                "objetivos": [
                    "EI03ET01 - Estabelecer relações de comparação entre objetos",
                    "EI03ET02 - Observar e descrever mudanças em diferentes materiais",
                    "EI03ET03 - Identificar e selecionar fontes de informações",
                    "EI03ET04 - Registrar observações, manipulações e medidas",
                    "EI03ET05 - Classificar objetos e figuras de acordo com suas semelhanças",
                    "EI03ET06 - Relatar fatos importantes sobre seu nascimento",
                    "EI03ET07 - Relacionar números às suas respectivas quantidades",
                    "EI03ET08 - Expressar medidas, quantidade de tempo e de espaço"
                ]
            }
        }
    },
    "ensino_fundamental": {
        "areas_conhecimento": {
            "linguagens": {
                "nome": "Linguagens",
                "componentes": ["Língua Portuguesa", "Arte", "Educação Física", "Língua Inglesa"],
                "competencias": [
                    "Compreender as linguagens como construção humana",
                    "Conhecer e explorar diversas práticas de linguagem",
                    "Utilizar diferentes linguagens para expressar-se",
                    "Utilizar diferentes tecnologias digitais de informação"
                ]
            },
            "matematica": {
                "nome": "Matemática",
                "componentes": ["Matemática"],
                "competencias": [
                    "Reconhecer que a Matemática é uma ciência humana",
                    "Desenvolver o raciocínio lógico",
                    "Compreender as relações entre conceitos e procedimentos",
                    "Fazer observações sistemáticas de aspectos quantitativos"
                ]
            },
            "ciencias_natureza": {
                "nome": "Ciências da Natureza",
                "componentes": ["Ciências"],
                "competencias": [
                    "Compreender conceitos fundamentais e estruturas explicativas",
                    "Analisar, compreender e explicar características",
                    "Avaliar aplicações e implicações políticas, socioambientais"
                ]
            },
            "ciencias_humanas": {
                "nome": "Ciências Humanas",
                "componentes": ["História", "Geografia"],
                "competencias": [
                    "Compreender a si e ao outro como identidades diferentes",
                    "Analisar o mundo social, cultural e digital",
                    "Identificar, comparar e explicar a intervenção do ser humano"
                ]
            }
        }
    }
}

# Metodologias pedagógicas
METODOLOGIAS = {
    "ativa": {
        "nome": "Metodologia Ativa",
        "descricao": "Coloca o aluno como protagonista do aprendizado",
        "estrategias": [
            "Aprendizagem baseada em problemas",
            "Aprendizagem baseada em projetos",
            "Sala de aula invertida",
            "Gamificação",
            "Peer instruction"
        ]
    },
    "construtivista": {
        "nome": "Construtivismo",
        "descricao": "Conhecimento é construído pelo próprio aluno",
        "estrategias": [
            "Experimentação",
            "Descoberta guiada",
            "Resolução de problemas",
            "Trabalho colaborativo",
            "Reflexão sobre o processo"
        ]
    },
    "sociointeracionista": {
        "nome": "Sociointeracionismo",
        "descricao": "Aprendizagem através da interação social",
        "estrategias": [
            "Trabalho em grupos",
            "Discussões dirigidas",
            "Tutoria entre pares",
            "Projetos colaborativos",
            "Mediação do professor"
        ]
    },
    "montessori": {
        "nome": "Método Montessori",
        "descricao": "Ambiente preparado para autoeducação",
        "estrategias": [
            "Materiais sensoriais",
            "Ambiente preparado",
            "Liberdade com responsabilidade",
            "Educação pela paz",
            "Respeito ao ritmo da criança"
        ]
    }
}

# Tipos de avaliação
TIPOS_AVALIACAO = {
    "diagnostica": {
        "nome": "Avaliação Diagnóstica",
        "objetivo": "Identificar conhecimentos prévios",
        "momento": "Início do processo",
        "instrumentos": ["Questionários", "Observação", "Conversas", "Desenhos"]
    },
    "formativa": {
        "nome": "Avaliação Formativa",
        "objetivo": "Acompanhar o processo de aprendizagem",
        "momento": "Durante o processo",
        "instrumentos": ["Portfólio", "Autoavaliação", "Observação sistemática", "Registros"]
    },
    "somativa": {
        "nome": "Avaliação Somativa",
        "objetivo": "Verificar resultados finais",
        "momento": "Final do processo",
        "instrumentos": ["Provas", "Trabalhos", "Apresentações", "Projetos"]
    }
}

def limpar_texto_para_pdf(texto):
    """Limpa texto para compatibilidade com PDF"""
    if not texto:
        return ""
    
    # Normaliza o texto para remover caracteres especiais
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    
    # Substitui caracteres problemáticos
    substituicoes = {
        '•': '-', '★': '*', '✓': 'v', '✔': 'v', '✕': 'x', '✖': 'x',
        '…': '...', '–': '-', '—': '-', '"': '"', '"': '"', ''': "'", ''': "'",
    }
    
    for antigo, novo in substituicoes.items():
        texto = texto.replace(antigo, novo)
    
    return texto

@planejamento_bp.route('/')
def index():
    """Página principal do planejamento"""
    return render_template('planejamento/index.html', 
                         estrutura_bncc=ESTRUTURA_BNCC,
                         metodologias=METODOLOGIAS,
                         tipos_avaliacao=TIPOS_AVALIACAO)

@planejamento_bp.route('/criar_plano', methods=['POST'])
def criar_plano():
    """Cria um plano de aula personalizado"""
    try:
        dados = request.get_json()
        
        # Validação dos dados
        campos_obrigatorios = ['titulo', 'nivel_ensino', 'duracao', 'objetivos']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return jsonify({'success': False, 'error': f'Campo {campo} é obrigatório'})
        
        # Gerar plano de aula
        plano = gerar_plano_personalizado(dados)
        
        # Gerar PDF
        pdf_filename = gerar_pdf_plano(plano, dados)
        
        return jsonify({
            'success': True,
            'plano': plano,
            'pdf_path': pdf_filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def gerar_plano_personalizado(dados):
    """Gera plano de aula personalizado"""
    titulo = dados['titulo']
    nivel = dados['nivel_ensino']
    duracao = dados['duracao']
    objetivos = dados['objetivos']
    metodologia = dados.get('metodologia', 'ativa')
    recursos = dados.get('recursos', [])
    adaptacoes = dados.get('adaptacoes_neurodiversidade', [])
    
    # Estruturar plano baseado no nível de ensino
    if nivel == "educacao_infantil":
        plano = gerar_plano_educacao_infantil(titulo, duracao, objetivos, metodologia)
    else:
        plano = gerar_plano_ensino_fundamental(titulo, duracao, objetivos, metodologia)
    
    # Adicionar recursos específicos
    plano['recursos_necessarios'] = adaptar_recursos_plano(recursos)
    
    # Adicionar adaptações para neurodiversidade
    if adaptacoes:
        plano['adaptacoes_neurodiversidade'] = gerar_adaptacoes_plano(adaptacoes)
    
    # Adicionar metodologia detalhada
    plano['metodologia_detalhada'] = METODOLOGIAS[metodologia]
    
    # Adicionar cronograma detalhado
    plano['cronograma'] = gerar_cronograma_aula(duracao, plano['atividades'])
    
    # Adicionar avaliação
    plano['avaliacao'] = gerar_estrategias_avaliacao(objetivos)
    
    return plano

def gerar_plano_educacao_infantil(titulo, duracao, objetivos, metodologia):
    """Gera plano específico para educação infantil"""
    return {
        'titulo': titulo,
        'nivel': 'Educação Infantil',
        'duracao': duracao,
        'objetivos_gerais': objetivos,
        'campos_experiencia': selecionar_campos_experiencia(objetivos),
        'atividades': gerar_atividades_educacao_infantil(metodologia, duracao),
        'organizacao_espacial': gerar_organizacao_espacial_ei(),
        'materiais_sensoriais': gerar_materiais_sensoriais(),
        'rotina_estruturada': gerar_rotina_estruturada(duracao)
    }

def gerar_plano_ensino_fundamental(titulo, duracao, objetivos, metodologia):
    """Gera plano específico para ensino fundamental"""
    return {
        'titulo': titulo,
        'nivel': 'Ensino Fundamental',
        'duracao': duracao,
        'objetivos_gerais': objetivos,
        'competencias_bncc': selecionar_competencias_bncc(objetivos),
        'atividades': gerar_atividades_ensino_fundamental(metodologia, duracao),
        'sequencia_didatica': gerar_sequencia_didatica(duracao),
        'interdisciplinaridade': gerar_conexoes_interdisciplinares(),
        'tecnologia_educacional': gerar_recursos_tecnologicos()
    }

def selecionar_campos_experiencia(objetivos):
    """Seleciona campos de experiência baseados nos objetivos"""
    campos_selecionados = []
    
    for objetivo in objetivos:
        if any(palavra in objetivo.lower() for palavra in ['social', 'emocional', 'relacionamento']):
            campos_selecionados.append(ESTRUTURA_BNCC['educacao_infantil']['campos_experiencia']['eu_outro_nos'])
        elif any(palavra in objetivo.lower() for palavra in ['motor', 'movimento', 'corpo']):
            campos_selecionados.append(ESTRUTURA_BNCC['educacao_infantil']['campos_experiencia']['corpo_gestos_movimentos'])
        elif any(palavra in objetivo.lower() for palavra in ['arte', 'música', 'criativo']):
            campos_selecionados.append(ESTRUTURA_BNCC['educacao_infantil']['campos_experiencia']['tracos_sons_cores_formas'])
        elif any(palavra in objetivo.lower() for palavra in ['linguagem', 'comunicação', 'fala']):
            campos_selecionados.append(ESTRUTURA_BNCC['educacao_infantil']['campos_experiencia']['escuta_fala_pensamento_linguagem'])
        elif any(palavra in objetivo.lower() for palavra in ['matemática', 'número', 'espaço', 'tempo']):
            campos_selecionados.append(ESTRUTURA_BNCC['educacao_infantil']['campos_experiencia']['espacos_tempos_quantidades'])
    
    return list({campo['nome']: campo for campo in campos_selecionados}.values())

def selecionar_competencias_bncc(objetivos):
    """Seleciona competências BNCC baseadas nos objetivos"""
    competencias_selecionadas = []
    
    for objetivo in objetivos:
        if any(palavra in objetivo.lower() for palavra in ['linguagem', 'comunicação', 'texto']):
            competencias_selecionadas.append(ESTRUTURA_BNCC['ensino_fundamental']['areas_conhecimento']['linguagens'])
        elif any(palavra in objetivo.lower() for palavra in ['matemática', 'número', 'cálculo']):
            competencias_selecionadas.append(ESTRUTURA_BNCC['ensino_fundamental']['areas_conhecimento']['matematica'])
        elif any(palavra in objetivo.lower() for palavra in ['ciência', 'natureza', 'experimento']):
            competencias_selecionadas.append(ESTRUTURA_BNCC['ensino_fundamental']['areas_conhecimento']['ciencias_natureza'])
        elif any(palavra in objetivo.lower() for palavra in ['história', 'geografia', 'sociedade']):
            competencias_selecionadas.append(ESTRUTURA_BNCC['ensino_fundamental']['areas_conhecimento']['ciencias_humanas'])
    
    return list({comp['nome']: comp for comp in competencias_selecionadas}.values())

def gerar_atividades_educacao_infantil(metodologia, duracao):
    """Gera atividades específicas para educação infantil"""
    atividades_base = {
        "ativa": [
            "Roda de conversa interativa",
            "Exploração sensorial livre",
            "Brincadeiras dirigidas",
            "Atividades de movimento",
            "Expressão artística"
        ],
        "construtivista": [
            "Experimentação com materiais",
            "Descoberta através do brincar",
            "Construção com blocos",
            "Investigação da natureza",
            "Criação de hipóteses"
        ],
        "sociointeracionista": [
            "Brincadeiras em grupo",
            "Contação de histórias coletiva",
            "Jogos cooperativos",
            "Projetos em equipe",
            "Dramatizações"
        ],
        "montessori": [
            "Atividades de vida prática",
            "Materiais sensoriais estruturados",
            "Exercícios de silêncio",
            "Cuidado do ambiente",
            "Trabalho individual concentrado"
        ]
    }
    
    atividades = atividades_base.get(metodologia, atividades_base["ativa"])
    
    # Adaptar quantidade baseada na duração
    if duracao <= 30:
        return atividades[:2]
    elif duracao <= 60:
        return atividades[:3]
    else:
        return atividades[:4]

def gerar_atividades_ensino_fundamental(metodologia, duracao):
    """Gera atividades específicas para ensino fundamental"""
    atividades_base = {
        "ativa": [
            "Resolução de problemas em grupos",
            "Projeto investigativo",
            "Debate estruturado",
            "Experimentos práticos",
            "Apresentações dos alunos"
        ],
        "construtivista": [
            "Construção de conceitos através da experiência",
            "Elaboração de hipóteses",
            "Teste de teorias",
            "Reflexão sobre o processo",
            "Sistematização do conhecimento"
        ],
        "sociointeracionista": [
            "Trabalho colaborativo",
            "Discussão em grupos",
            "Tutoria entre pares",
            "Projetos interdisciplinares",
            "Seminários estudantis"
        ],
        "montessori": [
            "Pesquisa individual",
            "Materiais autocorretivos",
            "Ambiente preparado para estudo",
            "Escolha livre de atividades",
            "Concentração prolongada"
        ]
    }
    
    atividades = atividades_base.get(metodologia, atividades_base["ativa"])
    
    # Adaptar quantidade baseada na duração
    if duracao <= 45:
        return atividades[:3]
    elif duracao <= 90:
        return atividades[:4]
    else:
        return atividades[:5]

def gerar_organizacao_espacial_ei():
    """Gera sugestões de organização espacial para educação infantil"""
    return {
        "cantos_atividade": [
            "Canto da leitura com almofadas e livros",
            "Canto dos jogos com materiais manipuláveis",
            "Canto da arte com materiais criativos",
            "Canto do faz de conta com fantasias e objetos"
        ],
        "disposicao_mobiliario": [
            "Mesas baixas para trabalho em grupo",
            "Tapete central para roda de conversa",
            "Prateleiras acessíveis às crianças",
            "Espaço livre para movimento"
        ],
        "materiais_acessiveis": [
            "Altura adequada para as crianças",
            "Organização visual clara",
            "Materiais seguros e variados",
            "Rotulagem com imagens e palavras"
        ]
    }

def gerar_materiais_sensoriais():
    """Gera lista de materiais sensoriais"""
    return {
        "tateis": ["Massinha", "Areia", "Tecidos variados", "Objetos texturizados"],
        "visuais": ["Cores vibrantes", "Formas geométricas", "Espelhos", "Caleidoscópios"],
        "auditivos": ["Instrumentos musicais", "Objetos sonoros", "CDs com sons da natureza"],
        "olfativos": ["Ervas aromáticas", "Essências naturais", "Flores"],
        "gustativos": ["Frutas variadas", "Temperos suaves", "Alimentos com texturas diferentes"]
    }

def gerar_rotina_estruturada(duracao):
    """Gera rotina estruturada baseada na duração"""
    if duracao <= 60:
        return [
            "Acolhida e roda de conversa (10 min)",
            "Atividade principal (30 min)",
            "Lanche e higiene (15 min)",
            "Atividade livre (5 min)"
        ]
    elif duracao <= 120:
        return [
            "Acolhida e roda de conversa (15 min)",
            "Primeira atividade (35 min)",
            "Lanche e higiene (20 min)",
            "Segunda atividade (30 min)",
            "Atividade livre e despedida (20 min)"
        ]
    else:
        return [
            "Acolhida e roda de conversa (20 min)",
            "Primeira atividade (40 min)",
            "Intervalo e lanche (25 min)",
            "Segunda atividade (40 min)",
            "Atividade livre (30 min)",
            "Roda final e despedida (15 min)"
        ]

def gerar_sequencia_didatica(duracao):
    """Gera sequência didática para ensino fundamental"""
    if duracao <= 50:
        return [
            "Problematização inicial (10 min)",
            "Desenvolvimento do conteúdo (25 min)",
            "Sistematização (10 min)",
            "Avaliação (5 min)"
        ]
    elif duracao <= 100:
        return [
            "Problematização inicial (15 min)",
            "Primeira etapa de desenvolvimento (30 min)",
            "Intervalo (10 min)",
            "Segunda etapa de desenvolvimento (30 min)",
            "Sistematização e avaliação (15 min)"
        ]
    else:
        return [
            "Problematização inicial (20 min)",
            "Primeira etapa de desenvolvimento (40 min)",
            "Intervalo (15 min)",
            "Segunda etapa de desenvolvimento (40 min)",
            "Atividade prática (30 min)",
            "Sistematização e avaliação (25 min)"
        ]

def gerar_conexoes_interdisciplinares():
    """Gera sugestões de conexões interdisciplinares"""
    return [
        "Matemática + Arte: Geometria através de obras de arte",
        "Ciências + Português: Produção de textos científicos",
        "História + Geografia: Análise de mapas históricos",
        "Educação Física + Matemática: Estatísticas esportivas",
        "Arte + Ciências: Pigmentos naturais e cores"
    ]

def gerar_recursos_tecnologicos():
    """Gera sugestões de recursos tecnológicos"""
    return [
        "Aplicativos educacionais interativos",
        "Vídeos educativos selecionados",
        "Jogos digitais pedagógicos",
        "Plataformas de pesquisa orientada",
        "Ferramentas de criação digital"
    ]

def adaptar_recursos_plano(recursos):
    """Adapta recursos disponíveis ao plano"""
    recursos_adaptados = {
        "basicos": ["Quadro", "Giz/Marcador", "Papel", "Lápis"],
        "tecnologicos": [],
        "manipulaveis": [],
        "artisticos": []
    }
    
    for recurso in recursos:
        if recurso in ["computador", "tablet", "projetor"]:
            recursos_adaptados["tecnologicos"].append(recurso)
        elif recurso in ["blocos", "jogos", "quebra-cabeca"]:
            recursos_adaptados["manipulaveis"].append(recurso)
        elif recurso in ["tinta", "papel", "pinceis", "massinha"]:
            recursos_adaptados["artisticos"].append(recurso)
    
    return recursos_adaptados

def gerar_adaptacoes_plano(adaptacoes):
    """Gera adaptações específicas para o plano"""
    adaptacoes_detalhadas = {}
    
    for adaptacao in adaptacoes:
        if adaptacao == "tea":
            adaptacoes_detalhadas["tea"] = {
                "estrategias": [
                    "Rotina visual estruturada",
                    "Instruções claras e objetivas",
                    "Redução de estímulos sensoriais",
                    "Tempo adicional para processamento",
                    "Apoio visual constante"
                ],
                "materiais": ["Cartões visuais", "Timer visual", "Fones de ouvido"],
                "organizacao": "Ambiente previsível e organizado"
            }
        elif adaptacao == "tdah":
            adaptacoes_detalhadas["tdah"] = {
                "estrategias": [
                    "Atividades curtas e variadas",
                    "Pausas frequentes",
                    "Movimento incorporado",
                    "Reforço positivo imediato",
                    "Organização visual do espaço"
                ],
                "materiais": ["Fidget toys", "Cronômetro", "Checklist visual"],
                "organizacao": "Espaço organizado com poucos distratores"
            }
        elif adaptacao == "dislexia":
            adaptacoes_detalhadas["dislexia"] = {
                "estrategias": [
                    "Abordagem multissensorial",
                    "Tempo adicional para leitura",
                    "Apoio visual e auditivo",
                    "Fontes adequadas",
                    "Tecnologia assistiva"
                ],
                "materiais": ["Régua de leitura", "Textos em fonte adequada", "Áudio dos textos"],
                "organizacao": "Materiais organizados e acessíveis"
            }
    
    return adaptacoes_detalhadas

def gerar_cronograma_aula(duracao, atividades):
    """Gera cronograma detalhado da aula"""
    cronograma = []
    tempo_por_atividade = duracao // len(atividades) if atividades else duracao
    tempo_atual = 0
    
    for i, atividade in enumerate(atividades):
        if i == 0:
            tempo_atividade = tempo_por_atividade + 5  # Mais tempo para primeira atividade
        elif i == len(atividades) - 1:
            tempo_atividade = duracao - tempo_atual  # Tempo restante para última atividade
        else:
            tempo_atividade = tempo_por_atividade
        
        cronograma.append({
            "horario": f"{tempo_atual:02d}:{(tempo_atual % 60):02d} - {(tempo_atual + tempo_atividade):02d}:{((tempo_atual + tempo_atividade) % 60):02d}",
            "atividade": atividade,
            "duracao": f"{tempo_atividade} min"
        })
        
        tempo_atual += tempo_atividade
    
    return cronograma

def gerar_estrategias_avaliacao(objetivos):
    """Gera estratégias de avaliação baseadas nos objetivos"""
    estrategias = {
        "diagnostica": {
            "instrumentos": ["Conversa inicial", "Observação livre", "Desenho diagnóstico"],
            "objetivo": "Identificar conhecimentos prévios dos alunos"
        },
        "formativa": {
            "instrumentos": ["Observação sistemática", "Registro fotográfico", "Portfólio"],
            "objetivo": "Acompanhar o processo de aprendizagem"
        },
        "somativa": {
            "instrumentos": ["Apresentação final", "Produção individual", "Autoavaliação"],
            "objetivo": "Verificar se os objetivos foram alcançados"
        }
    }
    
    # Adicionar critérios específicos baseados nos objetivos
    criterios = []
    for objetivo in objetivos:
        if "desenvolver" in objetivo.lower():
            criterios.append("Demonstra evolução no desenvolvimento da habilidade")
        elif "compreender" in objetivo.lower():
            criterios.append("Mostra compreensão do conceito apresentado")
        elif "expressar" in objetivo.lower():
            criterios.append("Consegue expressar-se adequadamente")
        elif "participar" in objetivo.lower():
            criterios.append("Participa ativamente das atividades")
    
    estrategias["criterios_avaliacao"] = criterios
    
    return estrategias

def gerar_pdf_plano(plano, dados):
    """Gera PDF do plano de aula"""
    # Criar diretório para PDFs se não existir
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"plano_aula_{timestamp}.pdf"
    filepath = os.path.join(pdf_dir, filename)
    
    # Criar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título
    titulo = limpar_texto_para_pdf(plano['titulo'])
    pdf.cell(0, 10, titulo, ln=True, align="C")
    pdf.ln(5)
    
    # Informações básicas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Nivel: {limpar_texto_para_pdf(plano['nivel'])}", ln=True)
    pdf.cell(0, 8, f"Duracao: {plano['duracao']} minutos", ln=True)
    pdf.ln(5)
    
    # Objetivos
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Objetivos:", ln=True)
    pdf.set_font("Arial", "", 10)
    for objetivo in plano['objetivos_gerais'][:3]:  # Limitar a 3 objetivos
        objetivo_limpo = limpar_texto_para_pdf(objetivo)
        if len(objetivo_limpo) > 80:
            objetivo_limpo = objetivo_limpo[:80] + "..."
        pdf.cell(0, 6, f"- {objetivo_limpo}", ln=True)
    pdf.ln(3)
    
    # Atividades
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Atividades:", ln=True)
    pdf.set_font("Arial", "", 10)
    for i, atividade in enumerate(plano['atividades'][:4], 1):  # Limitar a 4 atividades
        atividade_limpa = limpar_texto_para_pdf(atividade)
        if len(atividade_limpa) > 70:
            atividade_limpa = atividade_limpa[:70] + "..."
        pdf.cell(0, 6, f"{i}. {atividade_limpa}", ln=True)
    pdf.ln(3)
    
    # Cronograma
    if 'cronograma' in plano:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Cronograma:", ln=True)
        pdf.set_font("Arial", "", 10)
        for item in plano['cronograma'][:4]:  # Limitar a 4 itens
            horario = limpar_texto_para_pdf(item['horario'])
            atividade = limpar_texto_para_pdf(item['atividade'])
            if len(atividade) > 50:
                atividade = atividade[:50] + "..."
            pdf.cell(0, 6, f"{horario} - {atividade}", ln=True)
    
    # Rodapé
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Gerado por Sistema de Planejamento Educacional - {datetime.now().strftime('%d/%m/%Y')}", 0, 0, "C")
    
    # Salvar PDF
    pdf.output(filepath)
    
    return filename

@planejamento_bp.route('/download_pdf/<filename>')
def download_pdf(filename):
    """Download do PDF gerado"""
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdfs')
    filepath = os.path.join(pdf_dir, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': 'Arquivo não encontrado'}), 404


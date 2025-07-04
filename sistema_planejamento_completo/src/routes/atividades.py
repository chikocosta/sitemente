from flask import Blueprint, render_template, request, jsonify, send_file
import os
import random
import re
import unicodedata
from datetime import datetime
from fpdf import FPDF
import json

atividades_bp = Blueprint('atividades', __name__)

# Base científica - Teorias pedagógicas fundamentais
TEORIAS_PEDAGOGICAS = {
    "piaget": {
        "nome": "Teoria de Piaget",
        "principios": [
            "Desenvolvimento cognitivo por estágios",
            "Aprendizagem através da experiência",
            "Construção ativa do conhecimento",
            "Adaptação e equilibração"
        ],
        "aplicacao": "Atividades que promovem descoberta e experimentação"
    },
    "vygotsky": {
        "nome": "Teoria Sociocultural de Vygotsky",
        "principios": [
            "Zona de Desenvolvimento Proximal (ZDP)",
            "Mediação social na aprendizagem",
            "Linguagem como ferramenta cognitiva",
            "Interação social como base do desenvolvimento"
        ],
        "aplicacao": "Atividades colaborativas e com mediação"
    },
    "montessori": {
        "nome": "Método Montessori",
        "principios": [
            "Ambiente preparado",
            "Autoeducação",
            "Materiais sensoriais",
            "Respeito ao ritmo da criança"
        ],
        "aplicacao": "Atividades autônomas e sensoriais"
    },
    "gardner": {
        "nome": "Teoria das Inteligências Múltiplas",
        "principios": [
            "Múltiplas formas de inteligência",
            "Personalização do ensino",
            "Valorização de diferentes talentos",
            "Abordagem holística"
        ],
        "aplicacao": "Atividades diversificadas para diferentes inteligências"
    }
}

# Áreas de desenvolvimento com base científica
AREAS_DESENVOLVIMENTO = {
    "cognitivo": {
        "nome": "Desenvolvimento Cognitivo",
        "descricao": "Processos mentais como atenção, memória, raciocínio e resolução de problemas",
        "subáreas": {
            "atencao": "Capacidade de focar e manter concentração",
            "memoria": "Armazenamento e recuperação de informações",
            "raciocinio": "Pensamento lógico e resolução de problemas",
            "linguagem": "Desenvolvimento da comunicação verbal e escrita",
            "funcoes_executivas": "Planejamento, organização e controle inibitório"
        },
        "teorias_base": ["piaget", "vygotsky"],
        "faixas_etarias": {
            "3-4": "Pensamento simbólico inicial, vocabulário em expansão",
            "5-6": "Pensamento pré-operacional, início da alfabetização",
            "7-8": "Operações concretas, raciocínio lógico básico",
            "9-10": "Consolidação das operações concretas"
        }
    },
    "motor": {
        "nome": "Desenvolvimento Motor",
        "descricao": "Habilidades de movimento e coordenação corporal",
        "subáreas": {
            "motor_grosso": "Movimentos amplos do corpo",
            "motor_fino": "Coordenação de pequenos músculos",
            "equilibrio": "Controle postural e estabilidade",
            "coordenacao": "Integração de movimentos",
            "lateralidade": "Definição da dominância lateral"
        },
        "teorias_base": ["montessori"],
        "faixas_etarias": {
            "3-4": "Coordenação básica, início da motricidade fina",
            "5-6": "Refinamento motor, preparação para escrita",
            "7-8": "Coordenação avançada, habilidades esportivas",
            "9-10": "Movimentos complexos e precisos"
        }
    },
    "social": {
        "nome": "Desenvolvimento Social",
        "descricao": "Habilidades de interação e relacionamento com outros",
        "subáreas": {
            "cooperacao": "Trabalho em equipe e colaboração",
            "empatia": "Compreensão dos sentimentos alheios",
            "comunicacao": "Expressão e interpretação social",
            "lideranca": "Capacidade de guiar e influenciar",
            "resolucao_conflitos": "Mediação e negociação"
        },
        "teorias_base": ["vygotsky"],
        "faixas_etarias": {
            "3-4": "Brincadeira paralela, início da socialização",
            "5-6": "Brincadeira cooperativa, amizades iniciais",
            "7-8": "Grupos organizados, regras sociais",
            "9-10": "Relacionamentos complexos, liderança"
        }
    },
    "emocional": {
        "nome": "Desenvolvimento Emocional",
        "descricao": "Reconhecimento, expressão e regulação das emoções",
        "subáreas": {
            "autoconhecimento": "Consciência de si mesmo",
            "autorregulacao": "Controle emocional",
            "motivacao": "Impulso interno para agir",
            "autoestima": "Valorização pessoal",
            "resiliencia": "Capacidade de superar adversidades"
        },
        "teorias_base": ["gardner"],
        "faixas_etarias": {
            "3-4": "Identificação básica de emoções",
            "5-6": "Expressão emocional adequada",
            "7-8": "Regulação emocional consciente",
            "9-10": "Inteligência emocional desenvolvida"
        }
    }
}

# Tipos de atividades por área de desenvolvimento
TIPOS_ATIVIDADES = {
    "cognitivo": [
        "Jogos de memória",
        "Quebra-cabeças",
        "Sequências lógicas",
        "Classificação e seriação",
        "Atividades de linguagem",
        "Resolução de problemas",
        "Jogos de atenção",
        "Atividades de raciocínio"
    ],
    "motor": [
        "Circuitos motores",
        "Atividades de coordenação",
        "Jogos de equilíbrio",
        "Exercícios de motricidade fina",
        "Dança e movimento",
        "Atividades esportivas",
        "Manipulação de objetos",
        "Atividades de lateralidade"
    ],
    "social": [
        "Jogos cooperativos",
        "Atividades em grupo",
        "Dramatizações",
        "Projetos colaborativos",
        "Jogos de regras",
        "Atividades de comunicação",
        "Simulações sociais",
        "Trabalho em equipe"
    ],
    "emocional": [
        "Atividades de autoconhecimento",
        "Expressão artística",
        "Jogos de identificação emocional",
        "Atividades de relaxamento",
        "Histórias e reflexões",
        "Atividades de autoestima",
        "Exercícios de empatia",
        "Técnicas de autorregulação"
    ]
}

# Adaptações para neurotípicos e neuroatípicos
ADAPTACOES_NEURODIVERSIDADE = {
    "neurotipico": {
        "caracteristicas": "Desenvolvimento típico esperado para a idade",
        "estrategias": [
            "Atividades variadas e estimulantes",
            "Desafios progressivos",
            "Interação social rica",
            "Exploração livre"
        ]
    },
    "tea": {  # Transtorno do Espectro Autista
        "caracteristicas": "Dificuldades na comunicação social e comportamentos repetitivos",
        "estrategias": [
            "Rotinas estruturadas e previsíveis",
            "Instruções claras e visuais",
            "Redução de estímulos sensoriais",
            "Atividades de interesse especial",
            "Tempo para processamento",
            "Apoio visual constante"
        ]
    },
    "tdah": {  # Transtorno do Déficit de Atenção e Hiperatividade
        "caracteristicas": "Dificuldades de atenção, hiperatividade e impulsividade",
        "estrategias": [
            "Atividades curtas e dinâmicas",
            "Pausas frequentes",
            "Movimento incorporado",
            "Estímulos visuais e táteis",
            "Reforço positivo imediato",
            "Ambiente organizado"
        ]
    },
    "dislexia": {
        "caracteristicas": "Dificuldades específicas na leitura e escrita",
        "estrategias": [
            "Abordagem multissensorial",
            "Apoio visual e auditivo",
            "Tempo adicional",
            "Fontes e tamanhos adequados",
            "Atividades orais",
            "Tecnologia assistiva"
        ]
    },
    "altas_habilidades": {
        "caracteristicas": "Capacidades acima da média em uma ou mais áreas",
        "estrategias": [
            "Atividades desafiadoras",
            "Projetos independentes",
            "Aprofundamento de temas",
            "Mentoria e tutoria",
            "Conexões interdisciplinares",
            "Criatividade estimulada"
        ]
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

@atividades_bp.route('/')
def index():
    """Página principal do gerador de atividades"""
    return render_template('atividades/index.html', 
                         areas=AREAS_DESENVOLVIMENTO,
                         adaptacoes=ADAPTACOES_NEURODIVERSIDADE,
                         teorias=TEORIAS_PEDAGOGICAS)

@atividades_bp.route('/gerar', methods=['POST'])
def gerar_atividade():
    """Gera atividade personalizada com base científica"""
    try:
        dados = request.get_json()
        
        # Validação dos dados
        campos_obrigatorios = ['nome_crianca', 'idade', 'area_desenvolvimento', 'tipo_neurodiversidade']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return jsonify({'success': False, 'error': f'Campo {campo} é obrigatório'})
        
        # Gerar atividade personalizada
        atividade = gerar_atividade_personalizada(dados)
        
        # Gerar PDF
        pdf_filename = gerar_pdf_atividade(atividade, dados)
        
        return jsonify({
            'success': True,
            'atividade': atividade,
            'pdf_path': pdf_filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def gerar_atividade_personalizada(dados):
    """Gera atividade personalizada com base científica"""
    nome = dados['nome_crianca']
    idade = int(dados['idade'])
    area = dados['area_desenvolvimento']
    neurodiversidade = dados['tipo_neurodiversidade']
    recursos = dados.get('recursos_disponiveis', [])
    objetivos = dados.get('objetivos_especificos', [])
    
    # Determinar faixa etária
    if idade <= 4:
        faixa = "3-4"
    elif idade <= 6:
        faixa = "5-6"
    elif idade <= 8:
        faixa = "7-8"
    else:
        faixa = "9-10"
    
    # Selecionar teoria pedagógica mais adequada
    teoria_principal = selecionar_teoria_adequada(area, neurodiversidade)
    
    # Gerar atividade baseada na área de desenvolvimento
    atividade_base = gerar_atividade_por_area(area, faixa, teoria_principal)
    
    # Aplicar adaptações para neurodiversidade
    atividade_adaptada = aplicar_adaptacoes_neurodiversidade(atividade_base, neurodiversidade, idade)
    
    # Personalizar com recursos disponíveis
    atividade_personalizada = personalizar_com_recursos(atividade_adaptada, recursos)
    
    # Adicionar objetivos específicos
    atividade_final = adicionar_objetivos_especificos(atividade_personalizada, objetivos)
    
    # Adicionar fundamentação científica
    atividade_final['fundamentacao_cientifica'] = gerar_fundamentacao_cientifica(area, teoria_principal, neurodiversidade)
    
    # Adicionar códigos BNCC
    atividade_final['codigos_bncc'] = gerar_codigos_bncc(area, faixa)
    
    return atividade_final

def selecionar_teoria_adequada(area, neurodiversidade):
    """Seleciona a teoria pedagógica mais adequada"""
    if neurodiversidade == "tea":
        return "montessori"  # Estrutura e autonomia
    elif neurodiversidade == "tdah":
        return "gardner"  # Múltiplas inteligências
    elif area == "social":
        return "vygotsky"  # Interação social
    elif area == "cognitivo":
        return "piaget"  # Desenvolvimento cognitivo
    else:
        return "gardner"  # Abordagem holística

def gerar_atividade_por_area(area, faixa, teoria):
    """Gera atividade específica por área de desenvolvimento"""
    area_info = AREAS_DESENVOLVIMENTO[area]
    tipos_disponiveis = TIPOS_ATIVIDADES[area]
    
    # Selecionar tipo de atividade
    tipo_atividade = random.choice(tipos_disponiveis)
    
    # Gerar conteúdo baseado na teoria pedagógica
    if teoria == "piaget":
        atividade = gerar_atividade_piaget(area, tipo_atividade, faixa)
    elif teoria == "vygotsky":
        atividade = gerar_atividade_vygotsky(area, tipo_atividade, faixa)
    elif teoria == "montessori":
        atividade = gerar_atividade_montessori(area, tipo_atividade, faixa)
    else:  # gardner
        atividade = gerar_atividade_gardner(area, tipo_atividade, faixa)
    
    return atividade

def gerar_atividade_piaget(area, tipo, faixa):
    """Gera atividade baseada na teoria de Piaget"""
    return {
        'titulo': f'Descobrindo através da Experiência: {tipo}',
        'tipo': tipo,
        'area': area,
        'teoria_base': 'piaget',
        'objetivo_principal': 'Promover a construção ativa do conhecimento através da experiência',
        'materiais': ['Objetos manipuláveis', 'Materiais de exploração', 'Espaço para experimentação'],
        'instrucoes': [
            'Apresente o material sem explicações prévias',
            'Permita que a criança explore livremente',
            'Faça perguntas abertas sobre as descobertas',
            'Incentive a formulação de hipóteses',
            'Promova a reflexão sobre os resultados'
        ],
        'adaptacoes_idade': gerar_adaptacoes_idade_piaget(faixa),
        'avaliacao': 'Observe o processo de descoberta e as conexões feitas pela criança'
    }

def gerar_atividade_vygotsky(area, tipo, faixa):
    """Gera atividade baseada na teoria de Vygotsky"""
    return {
        'titulo': f'Aprendendo Juntos: {tipo}',
        'tipo': tipo,
        'area': area,
        'teoria_base': 'vygotsky',
        'objetivo_principal': 'Desenvolver habilidades através da mediação social',
        'materiais': ['Materiais colaborativos', 'Espaço para interação', 'Recursos de apoio'],
        'instrucoes': [
            'Forme grupos heterogêneos',
            'Apresente o desafio coletivamente',
            'Incentive a colaboração e troca de ideias',
            'Atue como mediador quando necessário',
            'Promova a reflexão em grupo'
        ],
        'zona_desenvolvimento_proximal': 'Identifique o que a criança pode fazer com ajuda',
        'mediacao': 'Use linguagem e símbolos como ferramentas de apoio',
        'avaliacao': 'Observe o progresso na interação social e aprendizagem colaborativa'
    }

def gerar_atividade_montessori(area, tipo, faixa):
    """Gera atividade baseada no método Montessori"""
    return {
        'titulo': f'Ambiente Preparado: {tipo}',
        'tipo': tipo,
        'area': area,
        'teoria_base': 'montessori',
        'objetivo_principal': 'Promover a autoeducação em ambiente preparado',
        'materiais': ['Materiais sensoriais específicos', 'Ambiente organizado', 'Materiais autocorretivos'],
        'instrucoes': [
            'Prepare o ambiente cuidadosamente',
            'Apresente o material de forma clara e precisa',
            'Permita que a criança trabalhe em seu próprio ritmo',
            'Observe sem interferir desnecessariamente',
            'Respeite a concentração da criança'
        ],
        'ambiente_preparado': 'Organize materiais de forma acessível e atrativa',
        'autocorrecao': 'Use materiais que permitam à criança identificar seus próprios erros',
        'avaliacao': 'Observe a concentração, repetição e satisfação da criança'
    }

def gerar_atividade_gardner(area, tipo, faixa):
    """Gera atividade baseada na teoria das Inteligências Múltiplas"""
    inteligencias = [
        'linguística', 'lógico-matemática', 'espacial', 'musical', 
        'corporal-cinestésica', 'interpessoal', 'intrapessoal', 'naturalista'
    ]
    
    inteligencia_foco = random.choice(inteligencias)
    
    return {
        'titulo': f'Múltiplas Inteligências: {tipo}',
        'tipo': tipo,
        'area': area,
        'teoria_base': 'gardner',
        'inteligencia_foco': inteligencia_foco,
        'objetivo_principal': f'Desenvolver a inteligência {inteligencia_foco} através de {tipo}',
        'materiais': gerar_materiais_inteligencia(inteligencia_foco),
        'instrucoes': gerar_instrucoes_inteligencia(inteligencia_foco, tipo),
        'variantes': 'Adapte para outras inteligências conforme interesse da criança',
        'avaliacao': f'Observe o desenvolvimento da inteligência {inteligencia_foco}'
    }

def aplicar_adaptacoes_neurodiversidade(atividade, neurodiversidade, idade):
    """Aplica adaptações específicas para neurodiversidade"""
    adaptacao = ADAPTACOES_NEURODIVERSIDADE[neurodiversidade]
    
    atividade['adaptacoes_neurodiversidade'] = {
        'tipo': neurodiversidade,
        'caracteristicas': adaptacao['caracteristicas'],
        'estrategias_aplicadas': adaptacao['estrategias']
    }
    
    # Adaptações específicas por tipo
    if neurodiversidade == "tea":
        atividade['instrucoes'] = adaptar_instrucoes_tea(atividade['instrucoes'])
        atividade['apoio_visual'] = True
        atividade['rotina_estruturada'] = True
        
    elif neurodiversidade == "tdah":
        atividade['instrucoes'] = adaptar_instrucoes_tdah(atividade['instrucoes'])
        atividade['pausas_frequentes'] = True
        atividade['movimento_incorporado'] = True
        
    elif neurodiversidade == "dislexia":
        atividade['instrucoes'] = adaptar_instrucoes_dislexia(atividade['instrucoes'])
        atividade['apoio_multissensorial'] = True
        
    elif neurodiversidade == "altas_habilidades":
        atividade['instrucoes'] = adaptar_instrucoes_altas_habilidades(atividade['instrucoes'])
        atividade['desafios_adicionais'] = True
    
    return atividade

def adaptar_instrucoes_tea(instrucoes):
    """Adapta instruções para TEA"""
    instrucoes_adaptadas = []
    for instrucao in instrucoes:
        instrucoes_adaptadas.append(f"🔹 {instrucao} (use apoio visual)")
    instrucoes_adaptadas.append("🔹 Mantenha rotina previsível")
    instrucoes_adaptadas.append("🔹 Reduza estímulos sensoriais excessivos")
    return instrucoes_adaptadas

def adaptar_instrucoes_tdah(instrucoes):
    """Adapta instruções para TDAH"""
    instrucoes_adaptadas = []
    for i, instrucao in enumerate(instrucoes):
        if i % 2 == 0:
            instrucoes_adaptadas.append(f"⚡ {instrucao} (atividade curta)")
        else:
            instrucoes_adaptadas.append(f"⚡ {instrucao} (faça uma pausa)")
    instrucoes_adaptadas.append("⚡ Incorpore movimento sempre que possível")
    return instrucoes_adaptadas

def adaptar_instrucoes_dislexia(instrucoes):
    """Adapta instruções para dislexia"""
    instrucoes_adaptadas = []
    for instrucao in instrucoes:
        instrucoes_adaptadas.append(f"📖 {instrucao} (use apoio visual e auditivo)")
    instrucoes_adaptadas.append("📖 Permita tempo adicional para leitura")
    instrucoes_adaptadas.append("📖 Use fontes e tamanhos adequados")
    return instrucoes_adaptadas

def adaptar_instrucoes_altas_habilidades(instrucoes):
    """Adapta instruções para altas habilidades"""
    instrucoes_adaptadas = []
    for instrucao in instrucoes:
        instrucoes_adaptadas.append(f"🌟 {instrucao} (adicione complexidade)")
    instrucoes_adaptadas.append("🌟 Ofereça projetos independentes")
    instrucoes_adaptadas.append("🌟 Conecte com outros temas de interesse")
    return instrucoes_adaptadas

def personalizar_com_recursos(atividade, recursos):
    """Personaliza atividade com recursos disponíveis"""
    if recursos:
        atividade['recursos_personalizados'] = recursos
        atividade['materiais'] = adaptar_materiais_recursos(atividade['materiais'], recursos)
    return atividade

def adicionar_objetivos_especificos(atividade, objetivos):
    """Adiciona objetivos específicos à atividade"""
    if objetivos:
        atividade['objetivos_especificos'] = objetivos
    return atividade

def gerar_fundamentacao_cientifica(area, teoria, neurodiversidade):
    """Gera fundamentação científica da atividade"""
    teoria_info = TEORIAS_PEDAGOGICAS[teoria]
    area_info = AREAS_DESENVOLVIMENTO[area]
    
    return {
        'teoria_principal': teoria_info,
        'area_desenvolvimento': area_info,
        'evidencias_cientificas': [
            "Pesquisas em neurociência mostram a importância da estimulação adequada",
            "Estudos longitudinais confirmam benefícios do desenvolvimento integrado",
            "Meta-análises demonstram eficácia de abordagens personalizadas"
        ],
        'referencias': [
            "Piaget, J. (1977). O desenvolvimento do pensamento",
            "Vygotsky, L. (1991). A formação social da mente",
            "Gardner, H. (1995). Inteligências múltiplas"
        ]
    }

def gerar_codigos_bncc(area, faixa):
    """Gera códigos BNCC relevantes"""
    codigos_bncc = {
        "3-4": {
            "cognitivo": ["EI03ET01", "EI03ET02", "EI03ET03"],
            "motor": ["EI03CG01", "EI03CG02", "EI03CG03"],
            "social": ["EI03EO01", "EI03EO02", "EI03EO03"],
            "emocional": ["EI03EO04", "EI03EO05", "EI03EO06"]
        },
        "5-6": {
            "cognitivo": ["EI03ET04", "EI03ET05", "EI03ET06"],
            "motor": ["EI03CG04", "EI03CG05", "EI03CG06"],
            "social": ["EI03EO07", "EI03EO08", "EI03EO09"],
            "emocional": ["EI03EO10", "EI03EO11", "EI03EO12"]
        },
        "7-8": {
            "cognitivo": ["EF01MA01", "EF01LP01", "EF01CI01"],
            "motor": ["EF12EF01", "EF12EF02", "EF12EF03"],
            "social": ["EF01ER01", "EF01ER02", "EF01ER03"],
            "emocional": ["EF01ER04", "EF01ER05", "EF01ER06"]
        },
        "9-10": {
            "cognitivo": ["EF02MA01", "EF02LP01", "EF02CI01"],
            "motor": ["EF12EF04", "EF12EF05", "EF12EF06"],
            "social": ["EF02ER01", "EF02ER02", "EF02ER03"],
            "emocional": ["EF02ER04", "EF02ER05", "EF02ER06"]
        }
    }
    
    return codigos_bncc.get(faixa, {}).get(area, [])

def gerar_materiais_inteligencia(inteligencia):
    """Gera materiais específicos para cada inteligência"""
    materiais_por_inteligencia = {
        'linguística': ['Livros', 'Papel e lápis', 'Gravador', 'Jogos de palavras'],
        'lógico-matemática': ['Blocos lógicos', 'Calculadora', 'Jogos de estratégia', 'Quebra-cabeças'],
        'espacial': ['Materiais de arte', 'Mapas', 'Blocos de construção', 'Jogos visuais'],
        'musical': ['Instrumentos musicais', 'CDs', 'Aplicativos de música', 'Objetos sonoros'],
        'corporal-cinestésica': ['Materiais esportivos', 'Objetos para manipular', 'Espaço amplo'],
        'interpessoal': ['Jogos de grupo', 'Materiais colaborativos', 'Espaço para interação'],
        'intrapessoal': ['Diário', 'Espaço silencioso', 'Materiais de reflexão'],
        'naturalista': ['Elementos naturais', 'Lupas', 'Materiais de observação']
    }
    return materiais_por_inteligencia.get(inteligencia, ['Materiais diversos'])

def gerar_instrucoes_inteligencia(inteligencia, tipo):
    """Gera instruções específicas para cada inteligência"""
    instrucoes_base = {
        'linguística': [
            'Use palavras e linguagem como foco principal',
            'Incentive a expressão verbal e escrita',
            'Promova discussões e narrativas'
        ],
        'lógico-matemática': [
            'Apresente problemas lógicos para resolver',
            'Use sequências e padrões',
            'Incentive o raciocínio matemático'
        ],
        'espacial': [
            'Use elementos visuais e espaciais',
            'Incentive a criação de imagens mentais',
            'Trabalhe com formas e cores'
        ]
    }
    return instrucoes_base.get(inteligencia, ['Siga as instruções gerais da atividade'])

def gerar_adaptacoes_idade_piaget(faixa):
    """Gera adaptações específicas por idade segundo Piaget"""
    adaptacoes = {
        "3-4": "Foque em exploração sensorial e simbolismo inicial",
        "5-6": "Desenvolva pensamento pré-operacional com classificações simples",
        "7-8": "Introduza operações concretas com materiais manipuláveis",
        "9-10": "Consolide operações concretas com problemas mais complexos"
    }
    return adaptacoes.get(faixa, "Adapte conforme desenvolvimento da criança")

def adaptar_materiais_recursos(materiais_originais, recursos_disponiveis):
    """Adapta materiais conforme recursos disponíveis"""
    materiais_adaptados = []
    for material in materiais_originais:
        if any(recurso.lower() in material.lower() for recurso in recursos_disponiveis):
            materiais_adaptados.append(f"✓ {material} (disponível)")
        else:
            materiais_adaptados.append(f"○ {material} (substitua por similar)")
    return materiais_adaptados

def gerar_pdf_atividade(atividade, dados):
    """Gera PDF da atividade personalizada"""
    # Criar diretório para PDFs se não existir
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"atividade_personalizada_{timestamp}.pdf"
    filepath = os.path.join(pdf_dir, filename)
    
    # Criar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título
    titulo = limpar_texto_para_pdf(atividade['titulo'])
    pdf.cell(0, 10, titulo, ln=True, align="C")
    pdf.ln(5)
    
    # Informações básicas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Crianca: {limpar_texto_para_pdf(dados['nome_crianca'])}", ln=True)
    pdf.cell(0, 8, f"Idade: {dados['idade']} anos", ln=True)
    pdf.cell(0, 8, f"Area: {limpar_texto_para_pdf(atividade['area'])}", ln=True)
    pdf.cell(0, 8, f"Teoria Base: {limpar_texto_para_pdf(atividade['teoria_base'])}", ln=True)
    pdf.ln(5)
    
    # Objetivo principal
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Objetivo Principal:", ln=True)
    pdf.set_font("Arial", "", 10)
    objetivo = limpar_texto_para_pdf(atividade['objetivo_principal'])
    pdf.multi_cell(0, 6, objetivo)
    pdf.ln(3)
    
    # Materiais
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Materiais:", ln=True)
    pdf.set_font("Arial", "", 10)
    for material in atividade['materiais'][:5]:  # Limitar a 5 materiais
        material_limpo = limpar_texto_para_pdf(material)
        pdf.cell(0, 6, f"- {material_limpo}", ln=True)
    pdf.ln(3)
    
    # Instruções
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Instrucoes:", ln=True)
    pdf.set_font("Arial", "", 10)
    for i, instrucao in enumerate(atividade['instrucoes'][:5], 1):  # Limitar a 5 instruções
        instrucao_limpa = limpar_texto_para_pdf(instrucao)
        if len(instrucao_limpa) > 80:
            instrucao_limpa = instrucao_limpa[:80] + "..."
        pdf.cell(0, 6, f"{i}. {instrucao_limpa}", ln=True)
    
    # Rodapé
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Gerado por Sistema de Planejamento Educacional - {datetime.now().strftime('%d/%m/%Y')}", 0, 0, "C")
    
    # Salvar PDF
    pdf.output(filepath)
    
    return filename

@atividades_bp.route('/download_pdf/<filename>')
def download_pdf(filename):
    """Download do PDF gerado"""
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdfs')
    filepath = os.path.join(pdf_dir, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': 'Arquivo não encontrado'}), 404


from flask import Blueprint, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from fpdf import FPDF
import unicodedata

adaptacoes_bp = Blueprint('adaptacoes', __name__)

# Base científica para adaptações neurodiversas
PERFIS_NEURODIVERSIDADE = {
    "tea": {
        "nome": "Transtorno do Espectro Autista (TEA)",
        "caracteristicas": [
            "Dificuldades na comunicação social",
            "Padrões restritos e repetitivos de comportamento",
            "Sensibilidades sensoriais",
            "Necessidade de rotina e previsibilidade",
            "Processamento de informações diferenciado"
        ],
        "estrategias_gerais": [
            "Estruturação visual do ambiente",
            "Rotinas claras e previsíveis",
            "Comunicação visual e concreta",
            "Redução de estímulos sensoriais",
            "Tempo adicional para processamento",
            "Apoio para transições",
            "Reforço positivo específico"
        ],
        "adaptacoes_curriculares": {
            "linguagem": [
                "Uso de pictogramas e símbolos visuais",
                "Frases curtas e objetivas",
                "Evitar linguagem figurada",
                "Apoio visual para compreensão",
                "Tempo adicional para resposta"
            ],
            "matematica": [
                "Materiais concretos e manipuláveis",
                "Sequências visuais de resolução",
                "Problemas com contexto familiar",
                "Evitar problemas com múltiplas etapas",
                "Calculadora quando necessário"
            ],
            "ciencias": [
                "Experimentos estruturados",
                "Roteiro visual detalhado",
                "Materiais sensoriais adequados",
                "Observação guiada",
                "Registro visual dos resultados"
            ],
            "arte": [
                "Materiais com texturas adequadas",
                "Atividades estruturadas",
                "Modelos visuais claros",
                "Respeitar preferências sensoriais",
                "Tempo flexível para criação"
            ]
        },
        "recursos_tecnologicos": [
            "Aplicativos de comunicação alternativa",
            "Timers visuais",
            "Agendas digitais",
            "Jogos educativos estruturados",
            "Fones de ouvido para redução de ruído"
        ]
    },
    "tdah": {
        "nome": "Transtorno do Déficit de Atenção com Hiperatividade (TDAH)",
        "caracteristicas": [
            "Dificuldade de atenção sustentada",
            "Hiperatividade e impulsividade",
            "Dificuldade de organização",
            "Problemas com funções executivas",
            "Necessidade de movimento"
        ],
        "estrategias_gerais": [
            "Atividades curtas e variadas",
            "Pausas frequentes",
            "Movimento incorporado ao aprendizado",
            "Organização visual do espaço",
            "Reforço positivo imediato",
            "Redução de distratores",
            "Estrutura clara de atividades"
        ],
        "adaptacoes_curriculares": {
            "linguagem": [
                "Textos curtos e objetivos",
                "Destaque de informações importantes",
                "Atividades interativas",
                "Pausas para movimento",
                "Uso de cores para organização"
            ],
            "matematica": [
                "Problemas em etapas pequenas",
                "Materiais manipuláveis",
                "Jogos matemáticos",
                "Movimento durante cálculos",
                "Checklist visual de passos"
            ],
            "ciencias": [
                "Experimentos hands-on",
                "Atividades de curta duração",
                "Observação ativa",
                "Registro em etapas",
                "Movimento entre estações"
            ],
            "arte": [
                "Projetos de curta duração",
                "Materiais variados",
                "Liberdade de movimento",
                "Múltiplas opções de expressão",
                "Feedback imediato"
            ]
        },
        "recursos_tecnologicos": [
            "Aplicativos de organização",
            "Timers e cronômetros",
            "Fidget toys digitais",
            "Jogos educativos dinâmicos",
            "Aplicativos de mindfulness"
        ]
    },
    "dislexia": {
        "nome": "Dislexia",
        "caracteristicas": [
            "Dificuldades na leitura e escrita",
            "Problemas com decodificação fonológica",
            "Dificuldade com sequenciamento",
            "Confusão entre letras similares",
            "Lentidão na leitura"
        ],
        "estrategias_gerais": [
            "Abordagem multissensorial",
            "Tempo adicional para leitura",
            "Apoio visual e auditivo",
            "Fontes adequadas",
            "Tecnologia assistiva",
            "Ensino fonológico explícito",
            "Reforço positivo constante"
        ],
        "adaptacoes_curriculares": {
            "linguagem": [
                "Textos em fontes adequadas (Arial, Verdana)",
                "Espaçamento aumentado entre linhas",
                "Apoio de áudio para textos",
                "Réguas de leitura",
                "Atividades fonológicas"
            ],
            "matematica": [
                "Problemas lidos em voz alta",
                "Símbolos matemáticos destacados",
                "Calculadora para cálculos básicos",
                "Gráficos e diagramas visuais",
                "Tempo adicional para resolução"
            ],
            "ciencias": [
                "Textos científicos adaptados",
                "Diagramas e esquemas visuais",
                "Experimentos com roteiro oral",
                "Gravações de explicações",
                "Glossário visual"
            ],
            "arte": [
                "Instruções visuais claras",
                "Modelos e exemplos",
                "Liberdade de expressão",
                "Apoio para escrita artística",
                "Uso de tecnologia criativa"
            ]
        },
        "recursos_tecnologicos": [
            "Leitores de tela",
            "Aplicativos de ditado",
            "Fontes dislexia-friendly",
            "Audiolivros",
            "Corretores ortográficos avançados"
        ]
    },
    "altas_habilidades": {
        "nome": "Altas Habilidades/Superdotação",
        "caracteristicas": [
            "Capacidade intelectual superior",
            "Criatividade elevada",
            "Envolvimento com tarefas",
            "Aprendizagem rápida",
            "Interesses específicos intensos"
        ],
        "estrategias_gerais": [
            "Enriquecimento curricular",
            "Projetos independentes",
            "Mentoria especializada",
            "Agrupamento por habilidades",
            "Aceleração quando apropriada",
            "Desafios intelectuais",
            "Desenvolvimento socioemocional"
        ],
        "adaptacoes_curriculares": {
            "linguagem": [
                "Textos complexos e variados",
                "Projetos de escrita criativa",
                "Análise literária avançada",
                "Debates e discussões",
                "Pesquisas independentes"
            ],
            "matematica": [
                "Problemas desafiadores",
                "Matemática aplicada",
                "Projetos de investigação",
                "Competições matemáticas",
                "Conceitos avançados"
            ],
            "ciencias": [
                "Experimentos complexos",
                "Pesquisa científica",
                "Projetos de inovação",
                "Mentoria com especialistas",
                "Participação em feiras científicas"
            ],
            "arte": [
                "Técnicas avançadas",
                "Projetos multimídia",
                "Expressão pessoal",
                "Colaboração com artistas",
                "Exposições e apresentações"
            ]
        },
        "recursos_tecnologicos": [
            "Plataformas de pesquisa avançada",
            "Software de simulação",
            "Ferramentas de criação digital",
            "Cursos online especializados",
            "Redes de colaboração"
        ]
    },
    "deficiencia_intelectual": {
        "nome": "Deficiência Intelectual",
        "caracteristicas": [
            "Limitações no funcionamento intelectual",
            "Dificuldades no comportamento adaptativo",
            "Necessidade de apoio personalizado",
            "Ritmo de aprendizagem diferenciado",
            "Necessidade de repetição e reforço"
        ],
        "estrategias_gerais": [
            "Ensino estruturado e repetitivo",
            "Objetivos específicos e mensuráveis",
            "Apoio visual constante",
            "Atividades funcionais",
            "Reforço positivo frequente",
            "Adaptação de materiais",
            "Ensino de habilidades de vida"
        ],
        "adaptacoes_curriculares": {
            "linguagem": [
                "Vocabulário simplificado",
                "Frases curtas e diretas",
                "Apoio visual para compreensão",
                "Repetição e reforço",
                "Atividades funcionais de comunicação"
            ],
            "matematica": [
                "Conceitos concretos",
                "Matemática funcional",
                "Materiais manipuláveis",
                "Sequências simples",
                "Aplicação prática"
            ],
            "ciencias": [
                "Observação direta",
                "Experimentos simples",
                "Conceitos básicos",
                "Aplicação no cotidiano",
                "Apoio visual constante"
            ],
            "arte": [
                "Atividades sensoriais",
                "Expressão livre",
                "Materiais adaptados",
                "Apoio motor quando necessário",
                "Valorização da criação"
            ]
        },
        "recursos_tecnologicos": [
            "Aplicativos educativos simples",
            "Comunicação alternativa",
            "Jogos adaptativos",
            "Recursos visuais digitais",
            "Tecnologia assistiva"
        ]
    },
    "deficiencia_visual": {
        "nome": "Deficiência Visual",
        "caracteristicas": [
            "Limitações na percepção visual",
            "Necessidade de adaptações táteis",
            "Uso de tecnologia assistiva",
            "Desenvolvimento de outros sentidos",
            "Necessidade de orientação espacial"
        ],
        "estrategias_gerais": [
            "Materiais em Braille",
            "Recursos táteis e sonoros",
            "Descrição verbal detalhada",
            "Organização espacial clara",
            "Tecnologia assistiva",
            "Apoio para mobilidade",
            "Desenvolvimento de habilidades compensatórias"
        ],
        "adaptacoes_curriculares": {
            "linguagem": [
                "Textos em Braille",
                "Audiolivros",
                "Descrição de imagens",
                "Materiais táteis",
                "Software de leitura"
            ],
            "matematica": [
                "Soroban (ábaco japonês)",
                "Materiais táteis",
                "Calculadora falante",
                "Gráficos em relevo",
                "Software matemático acessível"
            ],
            "ciencias": [
                "Modelos táteis",
                "Experimentos adaptados",
                "Descrições detalhadas",
                "Materiais com texturas",
                "Equipamentos sonoros"
            ],
            "arte": [
                "Materiais táteis variados",
                "Técnicas de relevo",
                "Música e expressão corporal",
                "Escultura e modelagem",
                "Arte digital acessível"
            ]
        },
        "recursos_tecnologicos": [
            "Leitores de tela",
            "Impressoras Braille",
            "Lupas eletrônicas",
            "Software de ampliação",
            "Aplicativos de navegação"
        ]
    }
}

# Estratégias pedagógicas baseadas em evidências
ESTRATEGIAS_EVIDENCIAS = {
    "universal_design": {
        "nome": "Desenho Universal para Aprendizagem (DUA)",
        "principios": [
            "Múltiplas formas de representação",
            "Múltiplas formas de engajamento",
            "Múltiplas formas de expressão"
        ],
        "aplicacao": [
            "Oferecer informações em diferentes formatos",
            "Proporcionar múltiplas opções de interesse",
            "Permitir diferentes formas de demonstrar conhecimento"
        ]
    },
    "ensino_estruturado": {
        "nome": "Ensino Estruturado",
        "componentes": [
            "Organização física do ambiente",
            "Programação temporal",
            "Sistema de trabalho",
            "Estrutura visual"
        ],
        "beneficios": [
            "Reduz ansiedade",
            "Aumenta independência",
            "Melhora compreensão",
            "Facilita transições"
        ]
    },
    "comunicacao_alternativa": {
        "nome": "Comunicação Alternativa e Ampliada (CAA)",
        "tipos": [
            "Símbolos gráficos",
            "Gestos e sinais",
            "Dispositivos eletrônicos",
            "Sistemas híbridos"
        ],
        "implementacao": [
            "Avaliação das necessidades",
            "Seleção do sistema adequado",
            "Treinamento da equipe",
            "Monitoramento contínuo"
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

@adaptacoes_bp.route('/')
def index():
    """Página principal das adaptações"""
    return render_template('adaptacoes/index.html', 
                         perfis=PERFIS_NEURODIVERSIDADE,
                         estrategias=ESTRATEGIAS_EVIDENCIAS)

@adaptacoes_bp.route('/gerar_adaptacao', methods=['POST'])
def gerar_adaptacao():
    """Gera adaptação personalizada"""
    try:
        dados = request.get_json()
        
        # Validação dos dados
        campos_obrigatorios = ['perfil_neurodiversidade', 'area_curricular', 'atividade_base']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return jsonify({'success': False, 'error': f'Campo {campo} é obrigatório'})
        
        # Gerar adaptação
        adaptacao = criar_adaptacao_personalizada(dados)
        
        # Gerar PDF se solicitado
        pdf_filename = None
        if dados.get('gerar_pdf', False):
            pdf_filename = gerar_pdf_adaptacao(adaptacao, dados)
        
        return jsonify({
            'success': True,
            'adaptacao': adaptacao,
            'pdf_path': pdf_filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def criar_adaptacao_personalizada(dados):
    """Cria adaptação personalizada baseada nos dados fornecidos"""
    perfil = dados['perfil_neurodiversidade']
    area = dados['area_curricular']
    atividade_base = dados['atividade_base']
    idade = dados.get('idade', 6)
    nivel_suporte = dados.get('nivel_suporte', 'moderado')
    
    # Obter informações do perfil
    info_perfil = PERFIS_NEURODIVERSIDADE.get(perfil, {})
    
    # Criar adaptação estruturada
    adaptacao = {
        'perfil_neurodiversidade': info_perfil.get('nome', perfil),
        'area_curricular': area,
        'atividade_original': atividade_base,
        'idade_aluno': idade,
        'nivel_suporte': nivel_suporte,
        'adaptacoes_especificas': gerar_adaptacoes_especificas(perfil, area, atividade_base, idade, nivel_suporte),
        'estrategias_pedagogicas': selecionar_estrategias_pedagogicas(perfil, area),
        'recursos_necessarios': listar_recursos_necessarios(perfil, area),
        'avaliacao_adaptada': criar_avaliacao_adaptada(perfil, area),
        'orientacoes_familia': gerar_orientacoes_familia(perfil),
        'cronograma_implementacao': criar_cronograma_implementacao(),
        'indicadores_sucesso': definir_indicadores_sucesso(perfil, area)
    }
    
    return adaptacao

def gerar_adaptacoes_especificas(perfil, area, atividade_base, idade, nivel_suporte):
    """Gera adaptações específicas baseadas no perfil e área"""
    info_perfil = PERFIS_NEURODIVERSIDADE.get(perfil, {})
    adaptacoes_area = info_perfil.get('adaptacoes_curriculares', {}).get(area, [])
    
    adaptacoes_especificas = {
        'modificacoes_atividade': [],
        'apoios_visuais': [],
        'adaptacoes_sensoriais': [],
        'estrategias_comunicacao': [],
        'modificacoes_ambiente': []
    }
    
    # Adaptações baseadas no perfil
    if perfil == 'tea':
        adaptacoes_especificas['modificacoes_atividade'] = [
            f"Dividir '{atividade_base}' em etapas menores e sequenciais",
            "Criar roteiro visual com pictogramas para cada etapa",
            "Estabelecer tempo definido para cada parte da atividade",
            "Preparar atividade alternativa caso haja sobrecarga sensorial"
        ]
        adaptacoes_especificas['apoios_visuais'] = [
            "Cartões com sequência da atividade",
            "Timer visual para controle de tempo",
            "Símbolos para indicar início, meio e fim",
            "Checklist visual de materiais necessários"
        ]
        adaptacoes_especificas['adaptacoes_sensoriais'] = [
            "Reduzir ruídos do ambiente durante a atividade",
            "Oferecer fones de ouvido se necessário",
            "Permitir pausas sensoriais",
            "Adaptar texturas de materiais se houver sensibilidade"
        ]
        
    elif perfil == 'tdah':
        adaptacoes_especificas['modificacoes_atividade'] = [
            f"Transformar '{atividade_base}' em segmentos de 10-15 minutos",
            "Incorporar movimento físico entre as etapas",
            "Criar elementos de gamificação e competição saudável",
            "Permitir escolha entre diferentes formas de execução"
        ]
        adaptacoes_especificas['apoios_visuais'] = [
            "Cores vibrantes para destacar informações importantes",
            "Organizadores gráficos para estruturar pensamento",
            "Lembretes visuais para manter foco",
            "Sistema de recompensas visual"
        ]
        adaptacoes_especificas['modificacoes_ambiente'] = [
            "Reduzir distratores visuais e auditivos",
            "Criar espaço de movimento próximo",
            "Posicionar longe de janelas e portas",
            "Ter fidget toys disponíveis"
        ]
        
    elif perfil == 'dislexia':
        adaptacoes_especificas['modificacoes_atividade'] = [
            f"Adaptar textos de '{atividade_base}' para fonte dislexia-friendly",
            "Oferecer apoio de áudio para instruções escritas",
            "Permitir tempo adicional para leitura e escrita",
            "Usar cores para destacar informações importantes"
        ]
        adaptacoes_especificas['apoios_visuais'] = [
            "Réguas de leitura coloridas",
            "Textos com espaçamento aumentado",
            "Marcadores de texto em cores diferentes",
            "Mapas mentais e organizadores gráficos"
        ]
        adaptacoes_especificas['estrategias_comunicacao'] = [
            "Explicações orais complementares",
            "Repetição de instruções importantes",
            "Confirmação de compreensão",
            "Uso de sinônimos e paráfrases"
        ]
    
    # Adaptações baseadas na idade
    if idade <= 6:
        adaptacoes_especificas['modificacoes_atividade'].append("Usar materiais concretos e manipuláveis")
        adaptacoes_especificas['apoios_visuais'].append("Imagens grandes e coloridas")
    elif idade <= 10:
        adaptacoes_especificas['modificacoes_atividade'].append("Incluir elementos lúdicos e jogos")
        adaptacoes_especificas['apoios_visuais'].append("Gráficos e diagramas simples")
    
    # Adaptações baseadas no nível de suporte
    if nivel_suporte == 'alto':
        adaptacoes_especificas['apoios_visuais'].append("Apoio individual constante")
        adaptacoes_especificas['modificacoes_atividade'].append("Simplificar objetivos da atividade")
    elif nivel_suporte == 'baixo':
        adaptacoes_especificas['modificacoes_atividade'].append("Oferecer desafios adicionais")
        adaptacoes_especificas['estrategias_comunicacao'].append("Incentivar autonomia na execução")
    
    return adaptacoes_especificas

def selecionar_estrategias_pedagogicas(perfil, area):
    """Seleciona estratégias pedagógicas baseadas em evidências"""
    estrategias = []
    
    # Estratégias universais
    estrategias.extend([
        "Desenho Universal para Aprendizagem (DUA)",
        "Ensino estruturado com rotinas claras",
        "Feedback positivo e específico",
        "Avaliação formativa contínua"
    ])
    
    # Estratégias específicas por perfil
    if perfil == 'tea':
        estrategias.extend([
            "Método TEACCH (Treatment and Education of Autistic and Communication Handicapped Children)",
            "Comunicação Alternativa e Ampliada (CAA)",
            "Análise do Comportamento Aplicada (ABA) adaptada",
            "Histórias sociais para situações específicas"
        ])
    elif perfil == 'tdah':
        estrategias.extend([
            "Técnicas de autorregulação",
            "Estratégias metacognitivas",
            "Aprendizagem baseada em movimento",
            "Gamificação educacional"
        ])
    elif perfil == 'dislexia':
        estrategias.extend([
            "Método fônico estruturado",
            "Abordagem multissensorial",
            "Tecnologia assistiva para leitura",
            "Estratégias de compreensão textual"
        ])
    
    # Estratégias específicas por área
    if area == 'linguagem':
        estrategias.extend([
            "Desenvolvimento da consciência fonológica",
            "Estratégias de compreensão leitora",
            "Produção textual assistida"
        ])
    elif area == 'matematica':
        estrategias.extend([
            "Resolução de problemas estruturada",
            "Uso de materiais concretos",
            "Conexão com situações reais"
        ])
    
    return estrategias

def listar_recursos_necessarios(perfil, area):
    """Lista recursos necessários para implementação"""
    recursos = {
        'materiais_fisicos': [],
        'tecnologia_assistiva': [],
        'recursos_humanos': [],
        'adaptacoes_ambiente': []
    }
    
    # Recursos básicos
    recursos['materiais_fisicos'].extend([
        "Materiais visuais (cartões, pictogramas)",
        "Timer ou cronômetro",
        "Materiais sensoriais variados",
        "Organizadores e pastas"
    ])
    
    # Recursos específicos por perfil
    info_perfil = PERFIS_NEURODIVERSIDADE.get(perfil, {})
    recursos_tech = info_perfil.get('recursos_tecnologicos', [])
    recursos['tecnologia_assistiva'].extend(recursos_tech)
    
    if perfil == 'tea':
        recursos['materiais_fisicos'].extend([
            "Cartões de comunicação",
            "Agenda visual",
            "Materiais para autorregulação"
        ])
        recursos['recursos_humanos'].extend([
            "Apoio especializado em TEA",
            "Treinamento para equipe escolar"
        ])
        
    elif perfil == 'tdah':
        recursos['materiais_fisicos'].extend([
            "Fidget toys",
            "Bola de exercício",
            "Marcadores coloridos"
        ])
        recursos['adaptacoes_ambiente'].extend([
            "Espaço para movimento",
            "Redução de distratores visuais"
        ])
        
    elif perfil == 'dislexia':
        recursos['materiais_fisicos'].extend([
            "Réguas de leitura",
            "Papel com pautas especiais",
            "Lápis ergonômicos"
        ])
        recursos['tecnologia_assistiva'].extend([
            "Software de leitura",
            "Gravador digital"
        ])
    
    return recursos

def criar_avaliacao_adaptada(perfil, area):
    """Cria estratégias de avaliação adaptadas"""
    avaliacao = {
        'instrumentos_adaptados': [],
        'criterios_especificos': [],
        'frequencia_avaliacao': '',
        'formas_registro': []
    }
    
    # Instrumentos gerais adaptados
    avaliacao['instrumentos_adaptados'] = [
        "Observação sistemática estruturada",
        "Portfólio com evidências visuais",
        "Autoavaliação adaptada",
        "Avaliação por pares quando apropriada"
    ]
    
    # Adaptações específicas por perfil
    if perfil == 'tea':
        avaliacao['instrumentos_adaptados'].extend([
            "Avaliação através de demonstração prática",
            "Uso de apoios visuais na avaliação",
            "Avaliação em ambiente familiar"
        ])
        avaliacao['criterios_especificos'] = [
            "Participação e engajamento",
            "Uso de estratégias de comunicação",
            "Demonstração de compreensão através de ações",
            "Progresso na independência"
        ]
        avaliacao['frequencia_avaliacao'] = "Diária, com registros semanais"
        
    elif perfil == 'tdah':
        avaliacao['instrumentos_adaptados'].extend([
            "Avaliações curtas e frequentes",
            "Avaliação através de projetos",
            "Uso de tecnologia interativa"
        ])
        avaliacao['criterios_especificos'] = [
            "Manutenção da atenção",
            "Qualidade da participação",
            "Uso de estratégias de autorregulação",
            "Conclusão de tarefas"
        ]
        avaliacao['frequencia_avaliacao'] = "Semanal, com feedback diário"
        
    elif perfil == 'dislexia':
        avaliacao['instrumentos_adaptados'].extend([
            "Avaliação oral complementar",
            "Tempo adicional para provas",
            "Uso de tecnologia assistiva"
        ])
        avaliacao['criterios_especificos'] = [
            "Compreensão conceitual",
            "Progresso na fluência",
            "Uso de estratégias compensatórias",
            "Autoconfiança na aprendizagem"
        ]
        avaliacao['frequencia_avaliacao'] = "Quinzenal, com monitoramento contínuo"
    
    avaliacao['formas_registro'] = [
        "Fichas de observação estruturadas",
        "Fotografias e vídeos (com autorização)",
        "Amostras de trabalhos",
        "Relatórios descritivos",
        "Gráficos de progresso"
    ]
    
    return avaliacao

def gerar_orientacoes_familia(perfil):
    """Gera orientações para a família"""
    orientacoes = {
        'estrategias_casa': [],
        'atividades_complementares': [],
        'sinais_observar': [],
        'recursos_apoio': []
    }
    
    if perfil == 'tea':
        orientacoes['estrategias_casa'] = [
            "Manter rotinas consistentes em casa",
            "Usar apoios visuais para atividades domésticas",
            "Criar espaços sensoriais adequados",
            "Praticar habilidades sociais em contexto familiar"
        ]
        orientacoes['atividades_complementares'] = [
            "Jogos de sequência e organização",
            "Atividades sensoriais controladas",
            "Leitura com apoio visual",
            "Brincadeiras estruturadas"
        ]
        orientacoes['sinais_observar'] = [
            "Mudanças no comportamento",
            "Dificuldades sensoriais",
            "Progressos na comunicação",
            "Interesse por novas atividades"
        ]
        
    elif perfil == 'tdah':
        orientacoes['estrategias_casa'] = [
            "Estabelecer rotinas claras e flexíveis",
            "Criar espaços organizados para estudo",
            "Incorporar movimento nas atividades",
            "Usar reforço positivo frequente"
        ]
        orientacoes['atividades_complementares'] = [
            "Esportes e atividades físicas",
            "Jogos que exigem atenção",
            "Atividades artísticas livres",
            "Tarefas domésticas estruturadas"
        ]
        orientacoes['sinais_observar'] = [
            "Níveis de atenção e concentração",
            "Capacidade de autorregulação",
            "Resposta a diferentes estratégias",
            "Bem-estar emocional"
        ]
        
    elif perfil == 'dislexia':
        orientacoes['estrategias_casa'] = [
            "Leitura compartilhada diária",
            "Uso de tecnologia assistiva",
            "Valorização dos progressos",
            "Apoio emocional constante"
        ]
        orientacoes['atividades_complementares'] = [
            "Jogos fonológicos",
            "Atividades de escrita criativa",
            "Audiolivros e podcasts",
            "Jogos de palavras"
        ]
        orientacoes['sinais_observar'] = [
            "Progresso na fluência de leitura",
            "Autoconfiança na escrita",
            "Uso de estratégias compensatórias",
            "Motivação para atividades de leitura"
        ]
    
    orientacoes['recursos_apoio'] = [
        "Grupos de apoio para famílias",
        "Materiais educativos especializados",
        "Profissionais de referência",
        "Organizações de apoio",
        "Cursos e workshops para pais"
    ]
    
    return orientacoes

def criar_cronograma_implementacao():
    """Cria cronograma para implementação das adaptações"""
    return {
        'semana_1': [
            "Apresentação das adaptações à equipe",
            "Preparação de materiais básicos",
            "Organização do ambiente",
            "Primeira implementação com observação"
        ],
        'semana_2': [
            "Ajustes baseados na primeira semana",
            "Introdução de novos apoios visuais",
            "Treinamento adicional se necessário",
            "Avaliação inicial dos resultados"
        ],
        'semana_3_4': [
            "Implementação completa das adaptações",
            "Monitoramento contínuo",
            "Registro sistemático de observações",
            "Comunicação com a família"
        ],
        'mes_2': [
            "Avaliação do progresso",
            "Ajustes finos nas estratégias",
            "Expansão para outras atividades",
            "Relatório de acompanhamento"
        ],
        'trimestre': [
            "Avaliação completa da eficácia",
            "Planejamento de próximas etapas",
            "Capacitação continuada da equipe",
            "Revisão e atualização das adaptações"
        ]
    }

def definir_indicadores_sucesso(perfil, area):
    """Define indicadores de sucesso para as adaptações"""
    indicadores = {
        'participacao': [],
        'aprendizagem': [],
        'bem_estar': [],
        'autonomia': []
    }
    
    # Indicadores gerais
    indicadores['participacao'] = [
        "Aumento do tempo de engajamento nas atividades",
        "Maior frequência de participação voluntária",
        "Redução de comportamentos de evitação"
    ]
    
    indicadores['aprendizagem'] = [
        "Progresso nos objetivos curriculares",
        "Demonstração de compreensão conceitual",
        "Aplicação de conhecimentos em novos contextos"
    ]
    
    indicadores['bem_estar'] = [
        "Redução de sinais de estresse ou ansiedade",
        "Expressões positivas sobre as atividades",
        "Melhoria nas relações sociais"
    ]
    
    indicadores['autonomia'] = [
        "Maior independência na execução de tarefas",
        "Uso espontâneo de estratégias aprendidas",
        "Solicitação adequada de ajuda quando necessário"
    ]
    
    # Indicadores específicos por perfil
    if perfil == 'tea':
        indicadores['participacao'].append("Uso adequado de apoios visuais")
        indicadores['aprendizagem'].append("Generalização de aprendizagens")
        indicadores['bem_estar'].append("Redução de comportamentos repetitivos")
        
    elif perfil == 'tdah':
        indicadores['participacao'].append("Manutenção da atenção por períodos maiores")
        indicadores['aprendizagem'].append("Conclusão de tarefas iniciadas")
        indicadores['autonomia'].append("Uso de estratégias de autorregulação")
        
    elif perfil == 'dislexia':
        indicadores['aprendizagem'].append("Melhoria na fluência de leitura")
        indicadores['bem_estar'].append("Aumento da autoconfiança")
        indicadores['autonomia'].append("Uso de tecnologia assistiva")
    
    return indicadores

def gerar_pdf_adaptacao(adaptacao, dados):
    """Gera PDF da adaptação"""
    # Criar diretório para PDFs se não existir
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"adaptacao_{timestamp}.pdf"
    filepath = os.path.join(pdf_dir, filename)
    
    # Criar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título
    titulo = f"Adaptacao para {adaptacao['perfil_neurodiversidade']}"
    titulo_limpo = limpar_texto_para_pdf(titulo)
    pdf.cell(0, 10, titulo_limpo, ln=True, align="C")
    pdf.ln(5)
    
    # Informações básicas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Area Curricular: {adaptacao['area_curricular']}", ln=True)
    pdf.cell(0, 8, f"Idade do Aluno: {adaptacao['idade_aluno']} anos", ln=True)
    pdf.cell(0, 8, f"Nivel de Suporte: {adaptacao['nivel_suporte']}", ln=True)
    pdf.ln(5)
    
    # Atividade original
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Atividade Original:", ln=True)
    pdf.set_font("Arial", "", 10)
    atividade_limpa = limpar_texto_para_pdf(adaptacao['atividade_original'])
    if len(atividade_limpa) > 80:
        atividade_limpa = atividade_limpa[:80] + "..."
    pdf.cell(0, 6, atividade_limpa, ln=True)
    pdf.ln(3)
    
    # Adaptações específicas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Adaptacoes Especificas:", ln=True)
    pdf.set_font("Arial", "", 10)
    
    adaptacoes_esp = adaptacao.get('adaptacoes_especificas', {})
    for categoria, itens in adaptacoes_esp.items():
        if itens:
            categoria_limpa = limpar_texto_para_pdf(categoria.replace('_', ' ').title())
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 6, f"{categoria_limpa}:", ln=True)
            pdf.set_font("Arial", "", 9)
            for item in itens[:2]:  # Limitar a 2 itens por categoria
                item_limpo = limpar_texto_para_pdf(item)
                if len(item_limpo) > 70:
                    item_limpo = item_limpo[:70] + "..."
                pdf.cell(0, 5, f"- {item_limpo}", ln=True)
            pdf.ln(2)
    
    # Estratégias pedagógicas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Estrategias Pedagogicas:", ln=True)
    pdf.set_font("Arial", "", 10)
    estrategias = adaptacao.get('estrategias_pedagogicas', [])
    for estrategia in estrategias[:4]:  # Limitar a 4 estratégias
        estrategia_limpa = limpar_texto_para_pdf(estrategia)
        if len(estrategia_limpa) > 70:
            estrategia_limpa = estrategia_limpa[:70] + "..."
        pdf.cell(0, 6, f"- {estrategia_limpa}", ln=True)
    
    # Rodapé
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Gerado por Sistema de Adaptacoes - {datetime.now().strftime('%d/%m/%Y')}", 0, 0, "C")
    
    # Salvar PDF
    pdf.output(filepath)
    
    return filename

@adaptacoes_bp.route('/download_pdf/<filename>')
def download_pdf(filename):
    """Download do PDF gerado"""
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdfs')
    filepath = os.path.join(pdf_dir, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': 'Arquivo não encontrado'}), 404

@adaptacoes_bp.route('/perfil/<perfil_id>')
def detalhes_perfil(perfil_id):
    """Retorna detalhes de um perfil específico"""
    perfil = PERFIS_NEURODIVERSIDADE.get(perfil_id)
    if perfil:
        return jsonify({'success': True, 'perfil': perfil})
    else:
        return jsonify({'success': False, 'error': 'Perfil não encontrado'}), 404

@adaptacoes_bp.route('/estrategias/<estrategia_id>')
def detalhes_estrategia(estrategia_id):
    """Retorna detalhes de uma estratégia específica"""
    estrategia = ESTRATEGIAS_EVIDENCIAS.get(estrategia_id)
    if estrategia:
        return jsonify({'success': True, 'estrategia': estrategia})
    else:
        return jsonify({'success': False, 'error': 'Estratégia não encontrada'}), 404


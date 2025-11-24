from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import re
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stageup-secret-key-change-in-production'
import os

# Garantir que o caminho do DB aponte para a pasta `instance` deste pacote
instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
os.makedirs(instance_dir, exist_ok=True)
db_path = os.path.join(instance_dir, 'stageup.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Padrões de títulos genéricos/promocionais do portal CIEE que não representam vagas reais
GENERIC_TITLE_PATTERNS = [
    r'Quero uma vaga',
    r'A empresa dos seus sonhos',
    r'Conectando a empresa',
    r'Entre com seu acesso',
    r'Entre com seu acesso',
    r'Conectando a empresa com os talentos',
    r'Logar',
]


def is_generic_title(title):
    if not title:
        return False
    for gp in GENERIC_TITLE_PATTERNS:
        if re.search(gp, title, re.I):
            return True
    return False

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    bio = db.Column(db.Text)  # Sobre você
    skills = db.Column(db.Text)  # JSON ou string separada por vírgulas
    location = db.Column(db.String(200))
    timezone = db.Column(db.String(100))
    website = db.Column(db.String(500))
    linkedin_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    portfolio_url = db.Column(db.String(500))
    profile_image = db.Column(db.String(500))
    cover_image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    login_method = db.Column(db.String(20), default='local')  # local, google, apple, linkedin
    social_id = db.Column(db.String(255))
    
def fetch_ciee_vaga_details(codigo_vaga):
    """Tenta buscar várias informações da página da vaga do CIEE.

    Retorna um dicionário com chaves: titulo, empresa, cidade, estado,
    salario, horario, descricao, link_ciee, codigo_vaga.
    """
    try:
        url = f'https://portal.ciee.org.br/quero-uma-vaga/?codigoVaga={codigo_vaga}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None

        s = BeautifulSoup(resp.content, 'html.parser')

        # Título: preferir h1, fallback em meta og:title
        titulo = None
        h1 = s.find('h1')
        if h1 and h1.get_text(strip=True):
            titulo = h1.get_text(strip=True)
        if not titulo:
            og_title = s.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                titulo = og_title.get('content')
        if not titulo and s.title:
            titulo = s.title.get_text(strip=True)

        # Empresa: procurar por elementos próximos ao título com classes ou strong
        empresa = None
        if h1:
            # procurar próximos irmãos que possam conter a empresa
            for sib in h1.find_next_siblings(limit=6):
                text = sib.get_text(' ', strip=True)
                if len(text) > 2 and len(text) < 80:
                    # heurística: se tiver letras maiúsculas e espaço, pode ser empresa
                    empresa = text
                    break

        if not empresa:
            # procurar por elementos com palavras-chave
            cand = s.find(string=re.compile(r'Empresa|Contratante|Contratante:', re.I))
            if cand:
                empresa = cand.strip()

        if not empresa:
            # procurar por strong ou h2 que contenham nomes de empresas
            strong = s.find(['strong', 'h2'], text=True)
            if strong and strong.get_text(strip=True):
                empresa = strong.get_text(strip=True)

        empresa = empresa or 'CIEE'

        # Cidade / estado: procurar por strings com padrão ' - São Paulo - SP' ou ' - SP'
        cidade = None
        estado = None
        location_text = s.find(string=re.compile(r'\b-\b.*-\b[A-Z]{2}\b|São Paulo|Rio de Janeiro', re.I))
        if location_text:
            loc = location_text.strip()
            # tentar extrair cidade e estado
            m = re.search(r'([A-Za-zÀ-ú\s]+)\s*-\s*([A-Za-z\s]+)\s*-\s*([A-Z]{2})', loc)
            if m:
                cidade = m.group(1).strip()
                estado = m.group(3).strip()
            else:
                # fallback
                if 'São Paulo' in loc:
                    cidade = 'São Paulo'
                    estado = 'SP'

        cidade = cidade or 'São Paulo'
        estado = estado or 'SP'

        # Salário/horário: procurar por R$ e por padrões com 'Mês' ou 'Hora'
        salario = None
        salario_elem = s.find(string=re.compile(r'R\$\s*[0-9\.,]+', re.I))
        if salario_elem:
            salario = salario_elem.strip()

        horario = None
        horario_elem = s.find(string=re.compile(r'\d{1,2}:\d{2}\s*(às|a)\s*\d{1,2}:\d{2}', re.I))
        if horario_elem:
            horario = horario_elem.strip()

        # Descrição: procurar seção com título 'Descrição' e coletar parágrafos seguintes
        descricao = ''
        desc_header = s.find(lambda tag: tag.name in ['h2', 'h3', 'strong'] and re.search(r'Descri', tag.get_text(), re.I))
        if desc_header:
            # coletar texto dos próximos nós até próximo header
            parts = []
            for sib in desc_header.find_next_siblings():
                if sib.name and sib.name.startswith('h'):
                    break
                txt = sib.get_text(' ', strip=True)
                if txt:
                    parts.append(txt)
            descricao = '\n'.join(parts).strip()

        # Fallback descrição: pegar o primeiro parágrafo notavelmente grande
        if not descricao:
            p = s.find('p')
            if p:
                descricao = p.get_text(' ', strip=True)

        # Construir dicionário final
        # Detectar títulos genéricos da página inicial do CIEE e ignorar
        generic_patterns = [
            r'Quero uma vaga', r'A empresa dos seus sonhos', r'Conectando a empresa', r'Entre com seu acesso', r'Quero uma vaga -'
        ]
        for gp in generic_patterns:
            if titulo and re.search(gp, titulo, re.I):
                return None

        return {
            'titulo': titulo or f'Vaga CIEE {codigo_vaga}',
            'empresa': empresa,
            'cidade': cidade,
            'estado': estado,
            'salario': salario,
            'horario': horario,
            'area': 'Geral',
            'descricao': descricao or '',
            'link_ciee': url,
            'codigo_vaga': codigo_vaga
        }
    except Exception as e:
        print(f'Erro ao buscar detalhes da vaga {codigo_vaga}: {e}')
    return None

class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    empresa = db.Column(db.String(255))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    tipo_periodo = db.Column(db.String(50))  # Integral, Meio Período
    modalidade = db.Column(db.String(50))  # Presencial, Home Office, Híbrido
    salario = db.Column(db.String(100))
    horario = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    link_ciee = db.Column(db.String(500))
    area = db.Column(db.String(100))
    codigo_vaga = db.Column(db.String(50))  # Código único da vaga no CIEE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AlertaVaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    descricao = db.Column(db.String(255))
    localidade = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Função para buscar vagas da CIEE com códigos reais
def buscar_vagas_ciee(palavra_chave=None, cidade=None):
    """
    Busca vagas no site da CIEE e extrai codigoVaga
    Faz scraping da página de busca do CIEE para obter vagas reais
    """
    vagas = []
    
    try:
        # URL base da CIEE para busca de vagas
        url = "https://portal.ciee.org.br/quero-uma-vaga/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Parâmetros de busca (adaptar conforme estrutura do CIEE)
        params = {}
        if palavra_chave:
            params['q'] = palavra_chave
        if cidade:
            params['city'] = cidade
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procurar por elementos de vaga (adaptar seletores conforme estrutura HTML)
            # Procura por links que contenham 'codigoVaga' ou 'vaga' na URL
            vaga_links = soup.find_all('a', href=re.compile(r'codigoVaga|/vaga/', re.I))
            
            for link in vaga_links[:30]:  # Limitar a 30 vagas
                try:
                    href = link.get('href', '')
                    
                    # Extrair código de vaga da URL
                    codigo_match = re.search(r'codigoVaga=(\d+)', href)
                    codigo_vaga = codigo_match.group(1) if codigo_match else None
                    
                    # Construir link correto se encontrou código
                    if codigo_vaga:
                        # Tentar obter detalhes ricos diretamente da página da vaga
                        details = fetch_ciee_vaga_details(codigo_vaga)
                        # Se não houver detalhes ricos, pular — evita salvar cards genéricos/promocionais
                        if details:
                            # garantir cidade/estado se passaram
                            if not details.get('cidade'):
                                details['cidade'] = cidade or 'São Paulo'
                            if not details.get('estado'):
                                details['estado'] = 'SP'
                            # não adicionar se o título for genérico
                            if not is_generic_title(details.get('titulo')):
                                vagas.append(details)
                        else:
                            # Se não pegou detalhes, pular (não inserir fallback genérico)
                            continue
                except Exception as e:
                    print(f"Erro ao processar vaga: {e}")
                    continue
        
        # Se não encontrar vagas reais, usar vagas de exemplo
        if not vagas:
            vagas = criar_vagas_exemplo(palavra_chave, cidade)

        # Garantir que as vagas específicas solicitadas estejam presentes
        required_codes = ['5859819', '5859771', '5859980']
        present_codes = {v.get('codigo_vaga') for v in vagas if v.get('codigo_vaga')}
        for code in required_codes:
            if code not in present_codes:
                details = fetch_ciee_vaga_details(code)
                if details:
                    vagas.append(details)
                else:
                    # Inserir entrada mínima para garantir redirecionamento funcional
                    vagas.append({
                        'titulo': f'Vaga CIEE {code}',
                        'empresa': 'CIEE',
                        'cidade': cidade or 'São Paulo',
                        'estado': 'SP',
                        'area': 'Geral',
                        'descricao': '',
                        'link_ciee': f'https://portal.ciee.org.br/quero-uma-vaga/?codigoVaga={code}',
                        'codigo_vaga': code
                    })
            
    except Exception as e:
        print(f"Erro ao buscar vagas da CIEE: {e}")
        # Em caso de erro, usar vagas de exemplo
        vagas = criar_vagas_exemplo(palavra_chave, cidade)
    
    return vagas

def criar_vagas_exemplo(palavra_chave=None, cidade=None):
    """Cria vagas de exemplo quando não é possível buscar da CIEE"""
    # URL base da CIEE com parâmetros de busca para melhorar a experiência
    base_url = 'https://portal.ciee.org.br/quero-uma-vaga/'
    
    vagas_exemplo = [
        {
            'titulo': 'Estágio em Infraestrutura - Redes',
            'empresa': 'BEEME',
            'cidade': 'Santo André',
            'estado': 'SP',
            'tipo_periodo': 'Meio Período',
            'modalidade': 'Presencial',
            'salario': 'R$ 951,44 / Mês',
            'horario': '13:00 às 17:00',
            'area': 'Tecnologia',
            'descricao': 'Oportunidade para estudante de TI trabalhar com infraestrutura de redes, suporte técnico e manutenção de sistemas. Conhecimento em redes, protocolos TCP/IP e sistemas operacionais será um diferencial.',
            'link_ciee': f'{base_url}?q=infraestrutura+redes',
            'codigo_vaga': None
        },
        {
            'titulo': 'Estágio Administrativo',
            'empresa': '3M',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'tipo_periodo': 'Período Integral',
            'modalidade': 'Presencial',
            'salario': 'R$ 1.000,00 / Mês',
            'horario': '09:00 às 16:00',
            'area': 'Administração',
            'descricao': 'Estágio em área administrativa com foco em processos internos, organização de documentos, atendimento e suporte às equipes. Excelente oportunidade para desenvolvimento profissional em multinacional.',
            'link_ciee': f'{base_url}?q=administrativo',
            'codigo_vaga': None
        },
        {
            'titulo': 'Estágio em Marketing Digital',
            'empresa': 'Itaú',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'tipo_periodo': 'Meio Período',
            'modalidade': 'Híbrido',
            'salario': 'R$ 1.200,00 / Mês',
            'horario': '14:00 às 18:00',
            'area': 'Marketing',
            'descricao': 'Vaga para estudante de Marketing, Publicidade ou Comunicação. Atuação em campanhas digitais, redes sociais, análise de métricas e criação de conteúdo. Ambiente inovador e aprendizado constante.',
            'link_ciee': f'{base_url}?q=marketing+digital',
            'codigo_vaga': None
        },
        {
            'titulo': 'Estágio em Desenvolvimento de Software',
            'empresa': 'AWS',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'tipo_periodo': 'Período Integral',
            'modalidade': 'Home Office',
            'salario': 'R$ 2.000,00 / Mês',
            'horario': '09:00 às 18:00',
            'area': 'Tecnologia',
            'descricao': 'Oportunidade única para trabalhar com tecnologias cloud, desenvolvimento de aplicações e soluções inovadoras. Conhecimento em Python, Java ou JavaScript será valorizado. Trabalho remoto.',
            'link_ciee': f'{base_url}?q=desenvolvimento+software',
            'codigo_vaga': None
        },
        {
            'titulo': 'Estágio em Recursos Humanos',
            'empresa': 'CIEE',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'tipo_periodo': 'Meio Período',
            'modalidade': 'Presencial',
            'salario': 'R$ 900,00 / Mês',
            'horario': '14:00 às 18:00',
            'area': 'RH',
            'descricao': 'Estágio em RH com foco em recrutamento, seleção e desenvolvimento de pessoas. Acompanhamento de processos seletivos, organização de eventos corporativos e suporte ao departamento.',
            'link_ciee': f'{base_url}?q=recursos+humanos',
            'codigo_vaga': None
        },
        {
            'titulo': 'Estágio em Contabilidade',
            'empresa': 'CIEE',
            'cidade': 'Belo Horizonte',
            'estado': 'MG',
            'tipo_periodo': 'Período Integral',
            'modalidade': 'Presencial',
            'salario': 'R$ 1.100,00 / Mês',
            'horario': '08:00 às 17:00',
            'area': 'Contabilidade',
            'descricao': 'Vaga para estudante de Contabilidade atuar com lançamentos contábeis, conciliações, auxílio na elaboração de relatórios e suporte nas rotinas do departamento contábil.',
            'link_ciee': f'{base_url}?q=contabilidade',
            'codigo_vaga': None
        },
        {
            'titulo': 'Estágio em Design Gráfico',
            'empresa': 'Nubank',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'tipo_periodo': 'Meio Período',
            'modalidade': 'Híbrido',
            'salario': 'R$ 1.500,00 / Mês',
            'horario': '14:00 às 18:00',
            'area': 'Design',
            'descricao': 'Oportunidade para estudante de Design criar materiais visuais, interfaces e peças de comunicação. Domínio de ferramentas como Figma, Adobe Creative Suite será essencial.',
            'link_ciee': f'{base_url}?q=design',
            'codigo_vaga': None
        },
        {
            'titulo': 'Estágio em Análise de Dados',
            'empresa': 'Microsoft',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'tipo_periodo': 'Período Integral',
            'modalidade': 'Home Office',
            'salario': 'R$ 1.800,00 / Mês',
            'horario': '09:00 às 18:00',
            'area': 'Tecnologia',
            'descricao': 'Estágio para trabalhar com análise de dados, criação de dashboards, relatórios e insights de negócio. Conhecimento em SQL, Python ou Power BI será um diferencial.',
            'link_ciee': f'{base_url}?q=analise+dados',
            'codigo_vaga': None
        }
    ]
    
    # Filtrar por palavra-chave se fornecida
    if palavra_chave:
        palavra_chave_lower = palavra_chave.lower()
        vagas_exemplo = [v for v in vagas_exemplo if palavra_chave_lower in v['titulo'].lower() or palavra_chave_lower in v['area'].lower()]
    
    # Filtrar por cidade se fornecida
    if cidade:
        cidade_lower = cidade.lower()
        vagas_exemplo = [v for v in vagas_exemplo if cidade_lower in v['cidade'].lower()]
    
    return vagas_exemplo


def update_or_refresh_vaga(codigo_vaga):
    """Atualiza (ou cria) uma `Vaga` no banco com informações obtidas pelo codigo_vaga.

    Se a vaga já existe, atualiza campos que estiverem vazios ou genéricos.
    Retorna a instância `Vaga`.
    """
    try:
        existing = Vaga.query.filter_by(codigo_vaga=codigo_vaga).first()
        details = fetch_ciee_vaga_details(codigo_vaga)
        if not details:
            return existing

        if existing:
            changed = False
            # Atualizar apenas se vazio ou genérico
            if (not existing.titulo) or existing.titulo.startswith('Vaga CIEE'):
                existing.titulo = details.get('titulo')
                changed = True
            if (not existing.empresa) or existing.empresa == 'CIEE':
                existing.empresa = details.get('empresa')
                changed = True
            if not existing.descricao:
                existing.descricao = details.get('descricao')
                changed = True
            if not existing.link_ciee:
                existing.link_ciee = details.get('link_ciee')
                changed = True
            if not existing.cidade:
                existing.cidade = details.get('cidade')
                changed = True
            if not existing.estado:
                existing.estado = details.get('estado')
                changed = True
            if not existing.salario and details.get('salario'):
                existing.salario = details.get('salario')
                changed = True
            if changed:
                db.session.add(existing)
                db.session.commit()
            return existing
        else:
            vaga = Vaga(**details)
            db.session.add(vaga)
            db.session.commit()
            return vaga
    except Exception as e:
        print(f'Erro ao atualizar/criar vaga {codigo_vaga}: {e}')
    return None


def clean_generic_vagas_db():
    """Remove do banco vagas cujo título parece ser um card/promocional genérico do CIEE."""
    try:
        removed = 0
        for vaga in Vaga.query.all():
            if vaga.titulo and is_generic_title(vaga.titulo):
                db.session.delete(vaga)
                removed += 1
        if removed:
            db.session.commit()
            print(f"Removidas {removed} vagas genéricas/promocionais do banco.")
    except Exception as e:
        print(f"Erro ao limpar vagas genéricas: {e}")

# Rotas
@app.route('/')
def index():
    # Garantir que há vagas no banco
    vagas_count = Vaga.query.count()
    if vagas_count == 0:
        # Criar vagas iniciais se não houver
        vagas_iniciais = criar_vagas_exemplo()
        for vaga_data in vagas_iniciais:
            vaga = Vaga(**vaga_data)
            db.session.add(vaga)
        db.session.commit()
    
    vagas_recentes = Vaga.query.order_by(Vaga.created_at.desc()).limit(8).all()
    return render_template('index.html', vagas_recentes=vagas_recentes)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/vagas')
def vagas():
    palavra_chave = request.args.get('palavra_chave', '')
    cidade = request.args.get('cidade', '')
    
    # Buscar vagas da CIEE apenas se houver busca ativa (palavra_chave ou cidade)
    # Se não houver busca ativa, usar apenas as vagas já no banco (permite ver vagas manuais)
    if palavra_chave or cidade:
        vagas_ciee = buscar_vagas_ciee(palavra_chave, cidade)
        
        # Salvar no banco de dados
        for vaga_data in vagas_ciee:
            # Pular vagas cujos títulos sejam genéricos/promocionais
            if is_generic_title(vaga_data.get('titulo')):
                continue
            # Verificar se já existe
            vaga_existente = Vaga.query.filter_by(
                titulo=vaga_data.get('titulo'), 
                cidade=vaga_data.get('cidade')
            ).first()
            if not vaga_existente:
                # Garantir que sempre tenha link para CIEE com busca otimizada
                if not vaga_data.get('link_ciee'):
                    # Criar link de busca baseado no título da vaga
                    titulo_busca = vaga_data.get('titulo', '').replace(' ', '+')
                    vaga_data['link_ciee'] = f'https://portal.ciee.org.br/portal/estudantes/vagas-de-estagio?palavra_chave={titulo_busca}'
                vaga = Vaga(**vaga_data)
                db.session.add(vaga)
        
        db.session.commit()
    else:
        # Se não houver busca ativa, garantir pelo menos vagas de exemplo
        vagas_count = Vaga.query.count()
        if vagas_count == 0:
            vagas_iniciais = criar_vagas_exemplo()
            for vaga_data in vagas_iniciais:
                vaga = Vaga(**vaga_data)
                db.session.add(vaga)
            db.session.commit()
    
    # Aplicar filtros
    query = Vaga.query
    
    periodo = request.args.getlist('periodo')
    modalidade = request.args.getlist('modalidade')
    area = request.args.getlist('area')
    localidade = request.args.getlist('localidade')
    
    if periodo:
        query = query.filter(Vaga.tipo_periodo.in_(periodo))
    if modalidade:
        query = query.filter(Vaga.modalidade.in_(modalidade))
    if area:
        query = query.filter(Vaga.area.in_(area))
    if localidade:
        # Filtrar por cidade/estado
        localidade_filtros = []
        for loc in localidade:
            if 'São Paulo Capital' in loc:
                localidade_filtros.append('São Paulo')
            elif 'Grande São Paulo' in loc:
                localidade_filtros.extend(['São Paulo', 'Santo André', 'São Caetano', 'Guarulhos'])
        if localidade_filtros:
            query = query.filter(Vaga.cidade.in_(localidade_filtros))
    
    if palavra_chave:
        query = query.filter(Vaga.titulo.contains(palavra_chave) | Vaga.area.contains(palavra_chave))
    if cidade:
        query = query.filter(Vaga.cidade.contains(cidade))
    
    vagas = query.order_by(Vaga.created_at.desc()).all()
    
    # Calcular contadores para os filtros
    filter_counts = {
        'periodo_integral': Vaga.query.filter_by(tipo_periodo='Período Integral').count(),
        'periodo_meio': Vaga.query.filter_by(tipo_periodo='Meio Período').count(),
        'modalidade_presencial': Vaga.query.filter_by(modalidade='Presencial').count(),
        'modalidade_home_office': Vaga.query.filter_by(modalidade='Home Office').count(),
        'modalidade_hibrido': Vaga.query.filter_by(modalidade='Híbrido').count(),
        'area_tecnologia': Vaga.query.filter_by(area='Tecnologia').count(),
        'area_marketing': Vaga.query.filter_by(area='Marketing').count(),
        'area_administracao': Vaga.query.filter_by(area='Administração').count(),
        'area_rh': Vaga.query.filter_by(area='RH').count(),
        'area_contabilidade': Vaga.query.filter_by(area='Contabilidade').count(),
        'area_design': Vaga.query.filter_by(area='Design').count(),
    }
    
    return render_template('vagas.html', vagas=vagas, palavra_chave=palavra_chave, cidade=cidade, filter_counts=filter_counts)

@app.route('/vaga/<int:vaga_id>/redirect')
def redirect_vaga(vaga_id):
    """
    Redireciona para a vaga na CIEE - FUNCIONALIDADE PRINCIPAL
    Usa o codigoVaga real da vaga para redirecionar corretamente ao CIEE
    """
    vaga = Vaga.query.get_or_404(vaga_id)
    
    # Se tiver código de vaga real, usar link direto
    if vaga.codigo_vaga:
        ciee_url = f'https://portal.ciee.org.br/quero-uma-vaga/?codigoVaga={vaga.codigo_vaga}'
    # Caso contrário, usar link genérico armazenado
    elif vaga.link_ciee and vaga.link_ciee.startswith('http'):
        ciee_url = vaga.link_ciee
    # Fallback: criar link de busca baseado no título
    else:
        titulo_busca = vaga.titulo.replace(' ', '+').replace('-', '+')
        ciee_url = f'https://portal.ciee.org.br/quero-uma-vaga/?q={titulo_busca}'
    
    # Redirecionamento permanente (302) para a CIEE
    return redirect(ciee_url, code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.password_hash and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name or user.email
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('vagas'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Página para solicitar redefinição de senha (envia um link por email).
    Em produção, aqui você geraria um token e enviaria um email com um link seguro.
    Para fins de demonstração, apenas exibimos uma mensagem informativa.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        # Em produção: gerar token, salvar e enviar email com link de reset.
        if user:
            # Simular envio de email (log)
            print(f"[INFO] Password reset requested for: {email}")

        # Mensagem genérica para evitar enumeração de usuários
        flash('Se o email existir em nossa base, você receberá instruções para redefinir sua senha.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name', '')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('cadastro.html')
        
        if User.query.filter_by(email=email).first():
            flash('Este email já está cadastrado.', 'error')
            return render_template('cadastro.html')
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            name=name,
            login_method='local'
        )
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.name or user.email
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('vagas'))
    
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/criar-alerta', methods=['POST'])
def criar_alerta():
    if 'user_id' not in session:
        flash('Você precisa estar logado para criar um alerta.', 'error')
        return redirect(url_for('login'))
    
    descricao = request.form.get('descricao')
    localidade = request.form.get('localidade')
    
    alerta = AlertaVaga(
        user_id=session['user_id'],
        descricao=descricao,
        localidade=localidade
    )
    
    db.session.add(alerta)
    db.session.commit()
    
    flash('Alerta criado com sucesso!', 'success')
    return redirect(url_for('vagas'))

# Rotas para login social (implementação básica - em produção usar OAuth2)
@app.route('/auth/google')
def auth_google():
    # Em produção, implementar OAuth2 do Google
    flash('Login com Google em desenvolvimento. Use login local por enquanto.', 'info')
    return redirect(url_for('login'))

@app.route('/auth/apple')
def auth_apple():
    # Em produção, implementar Sign in with Apple
    flash('Login com Apple em desenvolvimento. Use login local por enquanto.', 'info')
    return redirect(url_for('login'))

@app.route('/auth/linkedin')
def auth_linkedin():
    # Em produção, implementar OAuth2 do LinkedIn
    flash('Login com LinkedIn em desenvolvimento. Use login local por enquanto.', 'info')
    return redirect(url_for('login'))

@app.route('/atualizar-vagas')
def atualizar_vagas():
    """Rota para atualizar vagas manualmente (pode ser chamada periodicamente)"""
    try:
        vagas_ciee = buscar_vagas_ciee()
        novas_vagas = 0
        
        for vaga_data in vagas_ciee:
            # Pular vagas cujos títulos sejam genéricos/promocionais
            if is_generic_title(vaga_data.get('titulo')):
                continue
            vaga_existente = Vaga.query.filter_by(
                titulo=vaga_data.get('titulo'), 
                cidade=vaga_data.get('cidade')
            ).first()
            if not vaga_existente:
                if not vaga_data.get('link_ciee'):
                    vaga_data['link_ciee'] = 'https://portal.ciee.org.br/portal/estudantes/vagas-de-estagio'
                vaga = Vaga(**vaga_data)
                db.session.add(vaga)
                novas_vagas += 1
        
        db.session.commit()
        flash(f'{novas_vagas} novas vagas adicionadas!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar vagas: {str(e)}', 'error')
    
    return redirect(url_for('vagas'))

@app.route('/perfil')
def perfil():
    """Página de perfil do usuário"""
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar seu perfil.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('login'))
    
    # Parse skills se for string JSON
    skills_list = []
    if user.skills:
        try:
            skills_list = json.loads(user.skills) if user.skills.startswith('[') else user.skills.split(',')
        except:
            skills_list = user.skills.split(',') if user.skills else []
    
    return render_template('perfil.html', user=user, skills_list=skills_list)

@app.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    """Editar perfil do usuário"""
    if 'user_id' not in session:
        flash('Você precisa estar logado para editar seu perfil.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Atualizar campos básicos
        user.name = request.form.get('name', user.name)
        user.username = request.form.get('username', user.username)
        user.bio = request.form.get('bio', user.bio)
        user.location = request.form.get('location', user.location)
        user.timezone = request.form.get('timezone', user.timezone)
        user.website = request.form.get('website', user.website)
        user.linkedin_url = request.form.get('linkedin_url', user.linkedin_url)
        user.github_url = request.form.get('github_url', user.github_url)
        user.portfolio_url = request.form.get('portfolio_url', user.portfolio_url)
        
        # Processar skills
        skills_input = request.form.get('skills', '')
        if skills_input:
            # Se vier como string separada por vírgulas, converter para lista
            skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
            user.skills = json.dumps(skills_list) if skills_list else None
        else:
            user.skills = None
        
        user.updated_at = datetime.utcnow()
        
        # Verificar se username já existe (exceto para o próprio usuário)
        if user.username:
            existing_user = User.query.filter_by(username=user.username).first()
            if existing_user and existing_user.id != user.id:
                flash('Este nome de usuário já está em uso.', 'error')
                return redirect(url_for('editar_perfil'))
        
        db.session.commit()
        session['user_name'] = user.name or user.email
        
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil'))
    
    # Parse skills para exibição
    skills_list = []
    if user.skills:
        try:
            skills_list = json.loads(user.skills) if user.skills.startswith('[') else user.skills.split(',')
        except:
            skills_list = user.skills.split(',') if user.skills else []
    
    return render_template('editar_perfil.html', user=user, skills_list=skills_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Popular banco com vagas iniciais se estiver vazio
        if Vaga.query.count() == 0:
            vagas_iniciais = criar_vagas_exemplo()
            for vaga_data in vagas_iniciais:
                vaga = Vaga(**vaga_data)
                db.session.add(vaga)
            db.session.commit()
            print("Banco de dados inicializado com vagas de exemplo.")
        # Limpar entradas genéricas/promocionais que possam ter sido salvas
        clean_generic_vagas_db()

        # Garantir que as três vagas CIEE específicas existam no banco (códigos fornecidos pelo usuário)
        required_codes_init = ['5859819', '5859771', '5859980']
        for code in required_codes_init:
            # Usar rotina que atualiza ou cria com dados ricos
            update_or_refresh_vaga(code)
    app.run(debug=True)


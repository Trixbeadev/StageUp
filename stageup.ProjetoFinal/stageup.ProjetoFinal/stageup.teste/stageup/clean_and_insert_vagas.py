from app import app, db, Vaga

vagas_dados = [
    {
        'titulo': 'Estágio Odontologia',
        'empresa': 'JOIE ODONTOLOGIA',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 600,00 / Mês',
        'horario': '08:00:00 às 14:00:00',
        'area': 'Odontologia',
        'descricao': 'Atividade odontológica\n\nAtividades:\nAnalisar situações de clientes e orientá-los;\nAuxiliar na autorização de guias odontológicas;\nAuxiliar na higienização dos materiais\n\nRequisitos:\nCursando do 3º ao 8º semestre',
        'link_ciee': None,
        'codigo_vaga': '5859313'
    },
    {
        'titulo': 'Estágio Marketing',
        'empresa': 'CARRYBRAND SERVIÇOS DIGITAIS E PUBLICIDADE LTDA',
        'cidade': 'Sorocaba',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.400,00 / Mês',
        'horario': 'A combinar',
        'area': 'Marketing',
        'descricao': 'Agências de publicidade\n\nAtividades:\nAuxiliar a equipe de atendimento para demandas de criação;\nAuxiliar no departamento comercial de marketing;\nAssessorar no planejamento de mídia;\nAtuar no suporte em edição de vídeos\n\nRequisitos:\nCursando do 1º ao 17º semestre',
        'link_ciee': None,
        'codigo_vaga': '5859771'
    },
    {
        'titulo': 'Estágio Arquitetura e Urbanismo',
        'empresa': 'PMSP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.000,00 / Mês',
        'horario': 'A combinar',
        'area': 'Arquitetura e Urbanismo',
        'descricao': 'Administração pública em geral\n\nAtividades:\nAcessar na elaboração de projetos;\nAcompanhamento da legislação municipal;\nAcompanhamento da equipe de manutenção para reparos e adequações prediais\n\nRequisitos:\nCursando do 1º ao 3º semestre',
        'link_ciee': None,
        'codigo_vaga': '5859754'
    },
    {
        'titulo': 'Estágio Educação',
        'empresa': 'ESCOLA PORTINARI EDUCACIONAL LTDA',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.296,00 / Mês',
        'horario': '12:00:00 às 18:00:00',
        'area': 'Educação',
        'descricao': 'Educação infantil - pré-escola\n\nAtividades:\nAuxiliar nos cuidados da higiene, conforto e alimentação da criança;\nAuxiliar troca de fraldas e roupas;\nAcompanhamento ao banheiro, higiene bucal e banho quando necessário\n\nRequisitos:\nCursando do 1º ao 8º semestre\n\nBenefícios:\nAuxílio alimentação mensal',
        'link_ciee': None,
        'codigo_vaga': '5859274'
    },
    {
        'titulo': 'Estágio Direito',
        'empresa': 'SORO E TANUS ADVOGADAS ASSOCIADAS',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.200,00 / Mês',
        'horario': '09:00:00 às 15:00:00',
        'area': 'Direito',
        'descricao': 'Serviços advocatícios\n\nAtividades:\nAuxiliar na elaboração de relatórios, controles e pesquisas;\nAuxiliar rotinas administrativas jurídicas;\nAcompanhar processos\n\nRequisitos:\nCursando do 5º ao 7º semestre',
        'link_ciee': None,
        'codigo_vaga': '5858881'
    },
    {
        'titulo': 'Estágio Contabilidade',
        'empresa': 'THALASSIUS PARTICIPAÇÕES S.A.',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 2.750,00 / Mês',
        'horario': 'A combinar',
        'area': 'Contabilidade',
        'descricao': 'Holdings não-financeiras\n\nAtividades:\nAcompanhamento contábil e fiscal;\nConsulta de balancetes e lançamentos contábeis;\nElaboração de relatórios gerenciais\n\nRequisitos:\nCursando do 3º ao 18º semestre\n\nBenefícios:\nAuxílio alimentação mensal; Assistência médica; Assistência odontológica',
        'link_ciee': None,
        'codigo_vaga': '5859045'
    },
    {
        'titulo': 'Estágio Administração',
        'empresa': 'COKINOS AUDITORES & CONSULTORES',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.000,00 / Mês',
        'horario': '09:00:00 às 16:00:00',
        'area': 'Administração',
        'descricao': 'Consultoria e auditoria contábil tributária\n\nAtividades:\nAuxiliar no atendimento ao cliente;\nAuxiliar na organização de arquivos;\nAtendimento telefônico;\nDesenvolvimento de planilhas\n\nRequisitos:\nCursando do 1º ao 7º semestre',
        'link_ciee': None,
        'codigo_vaga': '5858612'
    },
    {
        'titulo': 'Estágio Psicologia',
        'empresa': 'FUNDO MUNICIPAL DE SAÚDE',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.500,00 / Mês',
        'horario': '07:00:00 às 13:15:00',
        'area': 'Psicologia',
        'descricao': 'Administração pública em geral\n\nAtividades:\nAcompanhamento das rotinas da coordenação;\nAcolhimento supervisionado de usuários;\nAcolhimento\n\nRequisitos:\nCursando do 5º ao 6º semestre\n\nBenefícios:\nAuxílio alimentação diário',
        'link_ciee': None,
        'codigo_vaga': '5858529'
    },
    {
        'titulo': 'Estágio Fisioterapia',
        'empresa': 'Confidencial',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 700,00 / Mês',
        'horario': '13:00:00 às 19:00:00',
        'area': 'Fisioterapia',
        'descricao': 'Atividades de fisioterapia\n\nAtividades:\nAuxiliar na aplicação de atividades por faixa etária;\nAjudar na demonstração de exercícios;\nAuxiliar o fisioterapeuta nos atendimentos\n\nRequisitos:\nCursando do 3º ao 9º semestre',
        'link_ciee': None,
        'codigo_vaga': '5858502'
    },
    {
        'titulo': 'Estágio Comunicação',
        'empresa': 'CATAVENTO CULTURAL',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.200,00 / Mês',
        'horario': '09:00:00 às 15:00:00',
        'area': 'Comunicação',
        'descricao': 'Organização cultural e artística\n\nAtividades:\nOrganização de documentos;\nOrganização de planilhas;\nSuporte ao marketing;\nElaboração de propostas;\nApoio em campanhas e eventos;\nMontar apresentações institucionais\n\nRequisitos:\nCursando do 2º ao 5º semestre',
        'link_ciee': None,
        'codigo_vaga': '5858494'
    },
    {
        'titulo': 'Estágio Recursos Humanos',
        'empresa': 'CHURRASCARIA E PIZZARIA LA BRAZA LTDA',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.000,00 / Mês',
        'horario': '08:00:00 às 14:00:00',
        'area': 'Recursos Humanos',
        'descricao': 'Restaurantes\n\nAtividades:\nAuxiliar departamento de RH;\nArquivar documentos;\nAcompanhar controle de prontuários e documentações\n\nRequisitos:\nCursando do 2º ao 4º semestre',
        'link_ciee': None,
        'codigo_vaga': '5858446'
    },
    {
        'titulo': 'Estágio Economia',
        'empresa': 'Confidencial',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.000,00 / Mês',
        'horario': 'A combinar',
        'area': 'Economia',
        'descricao': 'Bancos múltiplos\n\nAtividades:\nAcompanhamento de mercado financeiro;\nElaborar relatórios e planilhas\n\nRequisitos:\nCursando do 2º ao 9º semestre\n\nBenefícios:\nAuxílio alimentação mensal',
        'link_ciee': None,
        'codigo_vaga': '5858258'
    },
    {
        'titulo': 'Estágio Construção Civil',
        'empresa': 'HOSPITAL ALEMAO OSWALDO CRUZ',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 12,86 / Hora',
        'horario': '07:00:00 às 17:00:00',
        'area': 'Construção Civil',
        'descricao': 'Atendimento hospitalar\n\nAtividades:\nElaborar planilhas gerenciais;\nElaboração de relatórios;\nVistorias e perícias;\nLeitura e atualização de plantas;\nAcompanhar obras e cronogramas\n\nRequisitos:\nCursando do 6º ao 9º semestre',
        'link_ciee': None,
        'codigo_vaga': '5857773'
    }
]

with app.app_context():
    # Apagar TODAS as vagas da tabela
    try:
        deleted_count = db.session.query(Vaga).delete()
        db.session.commit()
        print(f'✗ Apagadas {deleted_count} vagas do banco.')
    except Exception as e:
        print(f'Erro ao apagar vagas: {e}')
        db.session.rollback()
    
    # Inserir APENAS as 13 vagas fornecidas
    try:
        for vaga_data in vagas_dados:
            vaga = Vaga(**vaga_data)
            db.session.add(vaga)
        db.session.commit()
        print(f'✓ Inseridas {len(vagas_dados)} vagas novas.')
        print(f'✓ Total de vagas no banco agora: {db.session.query(Vaga).count()}')
    except Exception as e:
        print(f'Erro ao inserir vagas: {e}')
        db.session.rollback()

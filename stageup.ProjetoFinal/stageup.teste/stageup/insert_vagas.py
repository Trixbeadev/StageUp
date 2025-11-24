from app import app, db, Vaga

# Lista de vagas fornecida pelo usuário (convertida para o modelo Vaga)
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
    ,
    {
        'titulo': 'Estágio Informática',
        'empresa': 'LEAD SOLUTIONS INFORMATICA LTDA',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.400,00 / Mês',
        'horario': '08:00:00 às 18:00:00',
        'area': 'Informática',
        'descricao': 'Reparação e manutenção de computadores e de equipamentos periféricos\n\nAtividades:\nAuxiliar em testes de sistemas\nAcompanhamento de testes e programas\nAcompanhamento supervisionado de testes de programas\nAcompanhamento supervisionado de elaboração de documentos de plataforma de testes\n\nRequisitos:\nCursando do 3º ao 18º semestre',
        'link_ciee': None,
        'codigo_vaga': '5861134'
    }
    ,
    {
        'titulo': 'Estágio Administrativa',
        'empresa': 'FUNDACAO PAULISTA DE EDUCACAO TECNOLOGIA E CULTURA',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.500,00 / Mês',
        'horario': 'A combinar',
        'area': 'Administrativa',
        'descricao': 'Administração pública em geral\n\nAtividades:\nAcessar arquivos diversos e elaborar relatórios sob demanda\nAcompanhamento de emissão de relatórios gerenciais\nAcompanhar a entrada e saída de documentos\n\nRequisitos:\nCursando do 1º ao 3º semestre\n\nBenefícios:\nAuxílio alimentação diário',
        'link_ciee': None,
        'codigo_vaga': '5862846'
    },
    {
        'titulo': 'Estágio Farmácia',
        'empresa': 'RAIA DROGASIL MANIPULACAO',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.500,00 / Mês',
        'horario': '09:00:00 às 16:00:00',
        'area': 'Farmácia',
        'descricao': 'Comércio varejista de produtos farmacêuticos, com manipulação de fórmulas\n\nAtividades:\nAuxiliar em gráficos, planilhas e relatórios, acompanhado do supervisor\nAuxiliar no atendimento ao cliente, sob Supervisão\n\nRequisitos:\nCursando do 1º ao 9º semestre\n\nBenefícios:\nRecesso Remunerado; Possibilidade prorrogação; Possibilidade efetivação',
        'link_ciee': None,
        'codigo_vaga': '5861166'
    },
    {
        'titulo': 'Estágio Relações Internacionais',
        'empresa': 'Confidencial',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.800,00 / Mês',
        'horario': 'A combinar',
        'area': 'Relações Internacionais',
        'descricao': 'Atividades de agenciamento marítimo\n\nAtividades:\nApoiar a área comercial\nAtualizar e alimentar o sistema\nApoiar a area comercial e demais clientes internos\n\nRequisitos:\nCursando do 1º ao 4º semestre\n\nBenefícios:\nPossibilidade efetivação; 13º Bolsa-auxílio; Auxílio alimentação diário',
        'link_ciee': None,
        'codigo_vaga': '5860901'
    },
    {
        'titulo': 'Estágio Psicologia',
        'empresa': 'GRUPO PELA VIDDA SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 895,00 / Mês',
        'horario': '10:00:00 às 14:00:00',
        'area': 'Psicologia',
        'descricao': 'Atividades de assistência social prestadas em residências coletivas e particulares\n\nAtividades:\nAcompanhar e observar os treinamentos\nObservar o supervisor psicólogo em analise de projeto e de relatórios de trabalho social\nObservar o supervisor psicólogo no acompanhamento social\n\nRequisitos:\nCursando do 6º ao 8º semestre',
        'link_ciee': None,
        'codigo_vaga': '5860391'
    },
    {
        'titulo': 'Estágio Comunicação',
        'empresa': 'XR GLOBAL BRASIL LTDA',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.500,00 / Mês',
        'horario': '13:00:00 às 19:00:00',
        'area': 'Comunicação',
        'descricao': 'Tratamento de dados, provedores de serviços de aplicação e serviços de hospedagem na internet\n\nAtividades:\nApoiar na inserção e atualização de dados no sistema\nAuxiliar na analise de relatórios gerenciais\nAuxiliar no controle de planejamento de propaganda\nContribuir na elaboração e implementação de planos de comunicação de projetos\nDesenvolver relatórios\nFornecer suporte ao desenvolvimento de planos de ação\nRealizar a participação em reuniões internas e externas\n\nRequisitos:\nCursando do 5º ao 7º semestre\n\nBenefícios:\nAuxílio alimentação mensal; Possibilidade prorrogação; Recesso Remunerado; Possibilidade efetivação',
        'link_ciee': None,
        'codigo_vaga': '5860011'
    },
    {
        'titulo': 'Estágio Comércio Exterior',
        'empresa': 'THALASSIUS A016.21 PARTICIPACOES S.A.',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 2.750,00 / Mês',
        'horario': 'A combinar',
        'area': 'Comércio Exterior',
        'descricao': 'Holdings de instituições não-financeiras\n\nAtividades:\nAtualizar relatórios e indicadores\nAuxiliar na atualização de indicadores\nAuxiliar na realização de relatórios de indicadores\nAvaliar a elaboração de relatórios de controle gerencial\nElaborar documentação relativa a formalização de processos\nFazer lançamento de dados no sistema interno\nFazer lançamento de faturas\nPreparar documentação relativa a formalização de processos\nRealizar atividades supervisionadas de aprendizado no lançamento de notas fiscais\nAuxiliar a gerencia na gestao dos relatorios para equipe\n\nRequisitos:\nCursando do 3º ao 18º semestre\n\nBenefícios:\nAssistência médica; Assistência odontológica; Auxílio alimentação mensal',
        'link_ciee': None,
        'codigo_vaga': '5859098'
    },
    {
        'titulo': 'Estágio Design',
        'empresa': 'Confidencial',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 900,00 / Mês',
        'horario': '08:00:00 às 12:00:00',
        'area': 'Design',
        'descricao': 'Atividades de consultoria em gestão empresarial\n\nAtividades:\nAuxiliar a área de criação\nAuxiliar em projetos institucionais e ações promocionais\nAuxiliar na criação de e-mail marketing\nAuxiliar na criação de layout de design gráficos e digital\nAuxiliar na edição de imagens em Photoshop\nAuxiliar na elaboração de relatórios\nAuxiliar no atendimento ao público\nAuxiliar usuários em programas de treinamentos\nFornecer suporte as atividades de projetos\nAuxiliar na producao de conteudo para redes sociais\n\nRequisitos:\nCursando do 1º ao 5º semestre\n\nBenefícios:\nAuxílio alimentação diário',
        'link_ciee': None,
        'codigo_vaga': '5855946'
    },
    {
        'titulo': 'Estágio Informática',
        'empresa': 'FOCO DESIGN E SOFTWARE PARA SERVICOS LTDA - EPP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.518,00 / Mês',
        'horario': '09:00:00 às 16:00:00',
        'area': 'Informática',
        'descricao': 'Desenvolvimento de programas de computador sob encomenda\n\nAtividades:\nRealizar Suporte Técnico aos Usuários\n\nRequisitos:\nCursando do 1º ao 5º semestre',
        'link_ciee': None,
        'codigo_vaga': '5864106'
    },
    {
        'titulo': 'Estágio Informática',
        'empresa': 'ENGETHERM ELETROTERMICA LTDA',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_periodo': 'Período Integral',
        'modalidade': 'Presencial',
        'salario': 'R$ 1.000,00 / Mês',
        'horario': '08:00:00 às 13:00:00',
        'area': 'Informática',
        'descricao': 'Fabricação de outros equipamentos e aparelhos elétricos\n\nAtividades:\nAcompanhamento das instalações de redes, micros e comunicação de dados\nAcompanhamento de ações desenvolvidas pelos analistas de sistemas\nAcompanhamento de projetos\n\nRequisitos:\nCursando do 4º ao 9º semestre',
        'link_ciee': None,
        'codigo_vaga': '5817052'
    }
]


with app.app_context():
    db.create_all()

    # Remover todas as vagas existentes (substituir pelas novas)
    try:
        deleted = Vaga.query.delete()
        if deleted:
            db.session.commit()
            print(f'→ Removidas {deleted} vagas existentes do banco.')
    except Exception as e:
        print(f'Erro ao remover vagas antigas: {e}')

    # Inserir as novas vagas
    adicionadas = 0
    for vaga_data in vagas_dados:
        vaga = Vaga(**vaga_data)
        db.session.add(vaga)
        adicionadas += 1
        print(f'✓ Adicionada: {vaga_data["empresa"]} - {vaga_data["titulo"]}')

    db.session.commit()
    print(f'\n✓ Total de vagas adicionadas: {adicionadas}')

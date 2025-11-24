from app import app, db, Vaga, update_or_refresh_vaga, clean_generic_vagas_db

codes = [
    '5859819', '5859771', '5859980',
    '5859313', '5859754', '5859274', '5858881', '5859045',
    '5858612', '5858529', '5858502', '5858494', '5858446',
    '5858258', '5857773', '5861134'
]

with app.app_context():
    # Garantir estrutura e limpar genéricos
    db.create_all()
    clean_generic_vagas_db()

    # Atualizar/criar as vagas desejadas
    for code in codes:
        print(f'Atualizando/checando vaga {code}...')
        update_or_refresh_vaga(code)

    print('\nConsulta das vagas:')
    for code in codes:
        vaga = Vaga.query.filter_by(codigo_vaga=code).first()
        if vaga:
            print('---')
            print(f'codigo_vaga: {vaga.codigo_vaga}')
            print(f'id: {vaga.id}')
            print(f'titulo: {vaga.titulo}')
            print(f'empresa: {vaga.empresa}')
            print(f'local: {vaga.cidade}, {vaga.estado}')
            print(f'salario: {vaga.salario}')
            print(f'descricao (trecho): { (vaga.descricao or "").strip()[:300]}')
            print(f'link_ciee: {vaga.link_ciee}')
        else:
            print(f'codigo_vaga {code} -> NÃO ENCONTRADA')

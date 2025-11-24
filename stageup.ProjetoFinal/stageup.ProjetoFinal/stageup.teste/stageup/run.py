#!/usr/bin/env python
"""
Script de inicialização do StageUp
Execute este arquivo para iniciar o servidor Flask
"""

from app import app, db, Vaga, criar_vagas_exemplo

if __name__ == '__main__':
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Popular banco com vagas iniciais se estiver vazio
        if Vaga.query.count() == 0:
            print("Inicializando banco de dados com vagas de exemplo...")
            vagas_iniciais = criar_vagas_exemplo()
            for vaga_data in vagas_iniciais:
                vaga = Vaga(**vaga_data)
                db.session.add(vaga)
            db.session.commit()
            print(f"✓ {len(vagas_iniciais)} vagas iniciais adicionadas ao banco de dados.")
        else:
            print(f"✓ Banco de dados já possui {Vaga.query.count()} vagas.")
        # Garantir que as vagas CIEE específicas existam no banco
        # (inclui os novos códigos fornecidos pelo usuário)
        required_codes_init = [
            '5859819', '5859771', '5859980',
            '5859313', '5859754', '5859274', '5858881', '5859045',
            '5858612', '5858529', '5858502', '5858494', '5858446',
            '5858258', '5857773', '5861134'
        ]

        # fetch_ciee_vaga_details está disponível em app.py, importar dinamicamente
        try:
            from app import fetch_ciee_vaga_details
            for code in required_codes_init:
                exists = Vaga.query.filter_by(codigo_vaga=code).first()
                if not exists:
                    details = fetch_ciee_vaga_details(code)
                    if details:
                        vaga = Vaga(**details)
                    else:
                        vaga = Vaga(
                            titulo=f'Estagio Odonto {code}',
                            empresa='CIEE',
                            cidade='São Paulo',
                            estado='SP',
                            area='Geral',
                            descricao='',
                            link_ciee=f'https://portal.ciee.org.br/quero-uma-vaga/?codigoVaga={code}',
                            codigo_vaga=code
                        )
                    db.session.add(vaga)
            db.session.commit()
        except Exception as e:
            print(f"Não foi possível garantir inserção das vagas CIEE iniciais: {e}")

        # Aplicar dados locais detalhados (se houver) para garantir que
        # as vagas tenham as informações exatas fornecidas no projeto.
        try:
            import update_vagas_info
        except Exception:
            # Se a import falhar, não interrompe a inicialização — vamos continuar.
            pass
        
        print("\n" + "="*50)
        print("🚀 StageUp está rodando!")
        print("="*50)
        print("Acesse: http://localhost:5000")
        print("="*50 + "\n")
    
    # Iniciar servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)


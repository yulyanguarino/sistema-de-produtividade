#!/usr/bin/env python
"""Script para consultar dados do banco de dados sem usar a API"""

from database import SessionLocal
from models import Colaborador, Operacao
from datetime import date

db = SessionLocal()

try:
    print("=" * 60)
    print("COLABORADORES")
    print("=" * 60)
    colabs = db.query(Colaborador).all()
    if colabs:
        for c in colabs:
            status = "✓ Ativo" if c.ativo else "✗ Inativo"
            print(f"ID: {c.id:2} | Nome: {c.nome:20} | {status}")
    else:
        print("Nenhum colaborador cadastrado")

    print("\n" + "=" * 60)
    print("OPERAÇÕES")
    print("=" * 60)
    ops = db.query(Operacao).all()
    if ops:
        for o in ops:
            print(f"ID: {o.id} | Data: {o.data} | Pedido: {o.pedido:10} | "
                  f"Sep: {o.separador_id} | Itens Sep: {o.qtd_itens_separados} | "
                  f"Conf: {o.conferente_id} | Itens Conf: {o.qtd_itens_conferidos}")
    else:
        print("Nenhuma operação cadastrada")

    print("\n" + "=" * 60)
    print("ESTATÍSTICAS")
    print("=" * 60)
    total_colabs = db.query(Colaborador).count()
    total_ativos = db.query(Colaborador).filter(Colaborador.ativo == True).count()
    total_ops = db.query(Operacao).count()
    print(f"Total de colaboradores: {total_colabs}")
    print(f"Colaboradores ativos: {total_ativos}")
    print(f"Total de operações: {total_ops}")

    if total_ops > 0:
        from sqlalchemy import func
        result = db.query(
            func.sum(Operacao.qtd_itens_separados),
            func.sum(Operacao.qtd_itens_conferidos)
        ).first()
        print(f"Total de itens separados: {result[0] or 0}")
        print(f"Total de itens conferidos: {result[1] or 0}")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()
    print("\n" + "=" * 60)
    print("✓ Conexão fechada")

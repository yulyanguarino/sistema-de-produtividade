import sys
sys.path.insert(0, '.')

from database import SessionLocal
from services import montar_dashboard

db = SessionLocal()

try:
    resultado = montar_dashboard(db)
    print("Dashboard resultado:")
    print(resultado)
except Exception as e:
    print(f"Erro: {type(e).__name__}")
    print(f"Mensagem: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

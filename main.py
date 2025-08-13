from fastapi import FastAPI
from scrapper import main as scrape_main
import sys
import io
from contextlib import redirect_stdout
from typing import Optional

app = FastAPI()

@app.get("/scrape")
def run_scraper(query: str, pages: Optional[int] = 1):
    """
    Ejecuta el scraper principal.
    Esto es una adaptación del CLI a un endpoint.
    """
    # Guardar los argumentos originales de sys.argv
    original_argv = sys.argv

    # Simular los argumentos de línea de comandos
    # sys.argv[0] es el nombre del script
    sys.argv = ["scrapper.py", query, str(pages)]

    # Capturar la salida estándar para devolverla en la respuesta
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            scrape_main()
        output = f.getvalue()
        # El scraper también guarda un archivo, podríamos devolver el nombre si quisiéramos.
        filename = f"titulos_{query.replace(' ', '_')}.txt"
        return {"status": "success", "output": output, "file_saved": filename}
    except SystemExit as e:
        # La función main llama a sys.exit(1) si los argumentos son incorrectos
        # Esto se captura aquí para evitar que el servidor se detenga.
        output = f.getvalue()
        return {"status": "error", "message": "SystemExit called, likely due to argument error.", "output": output, "exit_code": e.code}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        # Restaurar los argumentos originales de sys.argv
        sys.argv = original_argv

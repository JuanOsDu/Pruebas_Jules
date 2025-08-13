#!/usr/bin/env python3
"""
Scraper simple para títulos de MercadoLibre
Uso: python scraper.py "término de búsqueda" [páginas]
"""

import requests
from bs4 import BeautifulSoup
import sys
import time
from urllib.parse import quote_plus


class SimpleTitleScraper:
    """Scraper minimalista para títulos de MercadoLibre"""
    
    def __init__(self):
        self.base_url = "https://listado.mercadolibre.com.co"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_titles(self, query, max_pages=1):
        """
        Extraer títulos de productos
        
        Args:
            query (str): Término de búsqueda
            max_pages (int): Número máximo de páginas
            
        Returns:
            list: Lista de títulos encontrados
        """
        all_titles = []
        
        for page in range(1, max_pages + 1):
            print(f"🔍 Scrapeando página {page}...")
            
            try:
                titles = self._get_titles_from_page(query, page)
                all_titles.extend(titles)
                
                print(f"   ✅ {len(titles)} títulos encontrados")
                
                # Pausa entre páginas
                if page < max_pages:
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ❌ Error en página {page}: {e}")
                continue
        
        return all_titles
    
    def scrape_for_api(self, query, max_pages=1):
        """
        Extraer títulos de productos para la API (sin prints)

        Args:
            query (str): Término de búsqueda
            max_pages (int): Número máximo de páginas

        Returns:
            list: Lista de títulos encontrados
        """
        all_titles = []

        for page in range(1, max_pages + 1):
            try:
                titles = self._get_titles_from_page(query, page)
                all_titles.extend(titles)

                if page < max_pages:
                    time.sleep(2)

            except Exception as e:
                # En un entorno real, podrías loguear este error
                print(f"Error en página {page}: {e}")
                continue

        return all_titles

    def _get_titles_from_page(self, query, page):
        """Obtener títulos de una página específica"""
        import logging
        logging.basicConfig(filename='scraper.log', level=logging.INFO)

        # Construir URL
        encoded_query = quote_plus(query)
        url = f"{self.base_url}/{encoded_query}?page={page}"
        logging.info(f"Requesting URL: {url}")
        
        # Hacer request
        response = requests.get(url, headers=self.headers, timeout=10)
        logging.info(f"Response status code: {response.status_code}")
        with open("mercadolibre_response.html", "wb") as f:
            f.write(response.content)
        logging.info("Full response content saved to mercadolibre_response.html")
        response.raise_for_status()
        
        # Parsear HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer títulos usando diferentes selectores
        title_selectors = [
            '.ui-search-item__title',
            '.ui-search-result__content-title',
            'h2.ui-search-item__title',
            '.ui-search-item__group__element .ui-search-item__title'
        ]
        
        titles = []
        
        for selector in title_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    title = element.get_text(strip=True)
                    if title and title not in titles:
                        titles.append(title)
                break  # Usar solo el primer selector que funcione
        
        return titles
    
    def save_to_file(self, titles, filename):
        """Guardar títulos en archivo de texto"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Títulos encontrados: {len(titles)}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, title in enumerate(titles, 1):
                f.write(f"{i}. {title}\n")
        
        print(f"💾 Títulos guardados en: {filename}")


def main():
    """Función principal"""
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("❌ Uso: python scraper.py 'término de búsqueda' [páginas]")
        print("📝 Ejemplo: python scraper.py 'notebook' 3")
        sys.exit(1)
    
    query = sys.argv[1]
    pages = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    print(f"🎯 Buscando: '{query}'")
    print(f"📄 Páginas: {pages}")
    print("-" * 40)
    
    # Crear scraper y ejecutar
    scraper = SimpleTitleScraper()
    
    try:
        titles = scraper.scrape_titles(query, pages)
        
        print("\n" + "=" * 50)
        print(f"🎉 TOTAL ENCONTRADO: {len(titles)} títulos")
        print("=" * 50)
        
        # Mostrar primeros 10 títulos
        print("\n📋 Primeros títulos encontrados:")
        for i, title in enumerate(titles[:10], 1):
            print(f"   {i}. {title[:80]}{'...' if len(title) > 80 else ''}")
        
        if len(titles) > 10:
            print(f"   ... y {len(titles) - 10} más")
        
        # Guardar en archivo
        filename = f"titulos_{query.replace(' ', '_')}.txt"
        scraper.save_to_file(titles, filename)
        
        print(f"\n✨ Scraping completado exitosamente!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Scraping interrumpido por el usuario")
    except Exception as e:
        print(f"\n💥 Error general: {e}")


if __name__ == "__main__":
    main()
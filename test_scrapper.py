# Tests for scrapper.py
import unittest
from unittest.mock import patch, MagicMock, mock_open
from scrapper import SimpleTitleScraper, main
import sys
import os
import requests

class TestSimpleTitleScraper(unittest.TestCase):
    """Tests for the SimpleTitleScraper class."""

    def setUp(self):
        """Set up a scraper instance for tests."""
        self.scraper = SimpleTitleScraper()

    def test_initialization(self):
        """Test if the scraper is initialized with correct attributes."""
        self.assertEqual(self.scraper.base_url, "https://listado.mercadolibre.com.co")
        self.assertIn('User-Agent', self.scraper.headers)

    @patch('scrapper.requests.get')
    def test_get_titles_from_page_success(self, mock_get):
        """Test successfully extracting titles from a single page."""
        # Sample HTML content mimicking MercadoLibre's structure
        sample_html = """
        <html>
            <body>
                <h2 class="ui-search-item__title">Laptop Gamer Potente</h2>
                <h2 class="ui-search-item__title">Celular Nuevo Modelo</h2>
                <a class="ui-search-item__group__element ui-search-link" title="Tablet Económica">
                    <h2 class="ui-search-item__title">Tablet Económica</h2>
                </a>
            </body>
        </html>
        """
        # Configure the mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = sample_html.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        titles = self.scraper._get_titles_from_page("test query", 1)

        # Verify the returned titles
        self.assertEqual(len(titles), 3)
        self.assertIn("Laptop Gamer Potente", titles)
        self.assertIn("Celular Nuevo Modelo", titles)
        self.assertIn("Tablet Económica", titles)

        # Verify that requests.get was called correctly
        mock_get.assert_called_once_with(
            "https://listado.mercadolibre.com.co/test+query?page=1",
            headers=self.scraper.headers,
            timeout=10
        )

    @patch('scrapper.requests.get')
    def test_get_titles_from_page_request_fails(self, mock_get):
        """Test handling of a failed HTTP request."""
        # Configure the mock to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        # Expect an exception to be raised
        with self.assertRaises(requests.exceptions.RequestException):
            self.scraper._get_titles_from_page("test query", 1)

    @patch.object(SimpleTitleScraper, '_get_titles_from_page')
    def test_scrape_titles_single_page(self, mock_get_titles):
        """Test scraping a single page of titles."""
        mock_get_titles.return_value = ["Title 1", "Title 2"]

        # Capture print output
        with patch('builtins.print') as mock_print:
            titles = self.scraper.scrape_titles("query", 1)

        self.assertEqual(titles, ["Title 1", "Title 2"])
        mock_get_titles.assert_called_once_with("query", 1)

    @patch.object(SimpleTitleScraper, '_get_titles_from_page')
    @patch('scrapper.time.sleep', return_value=None) # Mock time.sleep to speed up test
    def test_scrape_titles_multiple_pages(self, mock_sleep, mock_get_titles):
        """Test scraping multiple pages of titles."""
        # Different return values for each page
        mock_get_titles.side_effect = [
            ["Page 1 - Title 1"],
            ["Page 2 - Title 1", "Page 2 - Title 2"],
            [] # Page 3 is empty
        ]

        with patch('builtins.print') as mock_print:
            titles = self.scraper.scrape_titles("query", 3)

        self.assertEqual(len(titles), 3)
        self.assertIn("Page 1 - Title 1", titles)
        self.assertIn("Page 2 - Title 2", titles)
        self.assertEqual(mock_get_titles.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2) # Called between pages 1-2 and 2-3

    @patch.object(SimpleTitleScraper, '_get_titles_from_page')
    def test_scrape_titles_with_error_page(self, mock_get_titles):
        """Test that scraping continues after a page fails."""
        mock_get_titles.side_effect = [
            ["Page 1 Title"],
            Exception("Failed to load page 2"),
            ["Page 3 Title"]
        ]

        with patch('builtins.print') as mock_print:
             with patch('scrapper.time.sleep', return_value=None):
                titles = self.scraper.scrape_titles("query", 3)

        self.assertEqual(len(titles), 2)
        self.assertIn("Page 1 Title", titles)
        self.assertNotIn("Page 2 Title", titles)
        self.assertIn("Page 3 Title", titles)
        self.assertEqual(mock_get_titles.call_count, 3)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_file(self, mock_file):
        """Test saving titles to a file."""
        titles = ["First title", "Second title"]
        filename = "test_output.txt"

        with patch('builtins.print') as mock_print:
            self.scraper.save_to_file(titles, filename)

        # Check that the file was opened correctly
        mock_file.assert_called_once_with(filename, 'w', encoding='utf-8')
        handle = mock_file()

        # Check that the content was written correctly
        self.assertIn(f"Títulos encontrados: {len(titles)}", handle.write.call_args_list[0][0][0])
        self.assertIn("1. First title", handle.write.call_args_list[2][0][0])
        self.assertIn("2. Second title", handle.write.call_args_list[3][0][0])


class TestMainFunction(unittest.TestCase):
    """Tests for the main function."""

    @patch('scrapper.SimpleTitleScraper')
    @patch('scrapper.sys.argv', ['scrapper.py', 'test query', '2'])
    def test_main_with_pages_argument(self, mock_scraper_class):
        """Test the main function with a query and page count."""
        # Create a mock instance for the scraper
        mock_scraper_instance = MagicMock()
        mock_scraper_instance.scrape_titles.return_value = ["Title A", "Title B"]
        mock_scraper_class.return_value = mock_scraper_instance

        with patch('builtins.print') as mock_print:
            main()

        # Verify that the scraper was instantiated and used correctly
        mock_scraper_class.assert_called_once()
        mock_scraper_instance.scrape_titles.assert_called_once_with('test query', 2)
        mock_scraper_instance.save_to_file.assert_called_once_with(
            ["Title A", "Title B"],
            "titulos_test_query.txt"
        )

    @patch('scrapper.SimpleTitleScraper')
    @patch('scrapper.sys.argv', ['scrapper.py', 'another query'])
    def test_main_with_default_pages(self, mock_scraper_class):
        """Test the main function with the default page count (1)."""
        mock_scraper_instance = MagicMock()
        mock_scraper_instance.scrape_titles.return_value = []
        mock_scraper_class.return_value = mock_scraper_instance

        with patch('builtins.print') as mock_print:
            main()

        mock_scraper_instance.scrape_titles.assert_called_once_with('another query', 1)

    @patch('scrapper.sys.argv', ['scrapper.py'])
    def test_main_no_arguments(self):
        """Test the main function with no arguments, expecting sys.exit."""
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        # Check for usage message
        self.assertIn("Uso: python scraper.py", mock_print.call_args_list[0][0][0])

    @patch('scrapper.SimpleTitleScraper')
    @patch('scrapper.sys.argv', ['scrapper.py', 'error query'])
    def test_main_general_exception(self, mock_scraper_class):
        """Test the main function's general exception handling."""
        # Configure the mock to raise an error
        mock_scraper_instance = MagicMock()
        mock_scraper_instance.scrape_titles.side_effect = Exception("A major error occurred")
        mock_scraper_class.return_value = mock_scraper_instance

        with patch('builtins.print') as mock_print:
            main()

        # Check that the error message was printed
        last_print_call = mock_print.call_args_list[-1][0][0]
        self.assertIn("💥 Error general: A major error occurred", last_print_call)

import unittest
from unittest.mock import patch, MagicMock

from careerfit.scraping.ind_scraper import scrape_ind_organisations


class TestScraping(unittest.TestCase):

    @patch('requests.get')
    def test_scrape_ind_organisations_expected_table_structure(self, mock_get):
        """Verify that the function preforms properly on the expected website table data."""
        expected_organisations = ['""Aa-Dee"" Machinefabriek en Staalbouw Nederland B.V.',
                                  '""AAE"" Advanced Automated Equipment B.V.']
        mock_url = "https://example.com"

        mock_response = MagicMock()
        mock_response.content = f'''
            <div class="paragraph--wysiwyg">
              <h2>Regular labour and highly skilled migrants</h2>
            <div class="responsive-table"><div class="responsive-table-inner"><table>
                <thead>
                    <tr>
                        <th>Organisation</th>
                        <th>KvK number</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th>""Aa-Dee"" Machinefabriek en Staalbouw Nederland B.V.</th>
                        <td>16051874</td>
                    </tr>
                    <tr>
                        <th>""AAE"" Advanced Automated Equipment B.V.</th>
                        <td>17037842</td>
                    </tr>
            '''
        mock_get.return_value = mock_response

        returned_organisations = scrape_ind_organisations(mock_url)

        self.assertEqual(expected_organisations, returned_organisations)

    def test_scrape_ind_organisations(self):
        organisations = scrape_ind_organisations()
        self.assertTrue(len(organisations) > 100)
        self.assertTrue("ABB B.V." in organisations)
        print(f"{len(organisations)} organisations were scraped.")

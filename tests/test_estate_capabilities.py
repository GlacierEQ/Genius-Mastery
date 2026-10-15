import unittest
from genius.estate_capabilities import match_capabilities

class TestEstateCapabilities(unittest.TestCase):
    def test_rank_and_preserve_source(self):
        catalog = {'intent_vectors': {'AUTOMATION': {'keywords': ['automation','workflow'], 'anchor_repositories': ['spiral-engine','apex-control-plane']}, 'MEMORY': {'keywords': ['memory'], 'anchor_repositories': ['aspen-grove-memory']}}}
        result = match_capabilities(catalog, 'workflow automation', limit=5)
        self.assertEqual(result[0]['intent_id'], 'AUTOMATION')
        self.assertEqual(result[0]['repositories'], ['spiral-engine','apex-control-plane'])
        self.assertEqual(result[0]['evidence_state'], 'catalog-pointer-unverified')

    def test_malformed_catalog(self):
        self.assertEqual(match_capabilities({'intent_vectors': {}}, 'automation'), [])
        self.assertEqual(match_capabilities({'intent_vectors': {'X': {'keywords': 'automation', 'anchor_repositories': ['a']}}}, 'automation'), [])

    def test_no_execution_promotion(self):
        result = match_capabilities({'intent_vectors': {'A': {'keywords': ['agent'], 'anchor_repositories': ['AKOS']}}}, 'agent')
        self.assertNotIn('execution_state', result[0])

if __name__ == '__main__':
    unittest.main()

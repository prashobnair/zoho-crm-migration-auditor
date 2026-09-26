import copy
import json
import unittest
from pathlib import Path
from migration import audit

BASE = json.loads(Path(__file__).with_name('examples.json').read_text())

class AuditTests(unittest.TestCase):
    def test_bad_sample_blocks_and_explains(self):
        result = audit(BASE)
        self.assertFalse(result['ready_for_import'])
        self.assertEqual({'possible_duplicate','orphan_organization','orphan_person','unmapped_stage'},
                         {x['code'] for x in result['issues']})
        self.assertEqual(['organizations','people','deals','activities'], result['import_order'])
        self.assertIsNone(result['target_preview_counts'])

    def test_clean_sample_passes_without_mutation(self):
        source = copy.deepcopy(BASE)
        source['people'] = source['people'][:1]
        source['deals'] = source['deals'][:1]
        before = copy.deepcopy(source)
        result = audit(source)
        self.assertTrue(result['ready_for_import'])
        self.assertEqual(result['source_counts'], result['target_preview_counts'])
        self.assertEqual(source, before)
        self.assertEqual([], result['issues'])

    def test_duplicate_id_and_orphan_activity(self):
        source = copy.deepcopy(BASE)
        source['organizations'].append(dict(source['organizations'][0]))
        source['activities'][0]['deal_id'] = 'missing'
        codes = {x['code'] for x in audit(source)['issues']}
        self.assertIn('duplicate_id', codes)
        self.assertIn('orphan_deal', codes)

    def test_reject_invalid_envelope(self):
        with self.assertRaises(ValueError):
            audit({'people': []})

    def test_output_deterministic(self):
        self.assertEqual(audit(BASE), audit(copy.deepcopy(BASE)))

if __name__ == '__main__':
    unittest.main()

import unittest
from refresh import build, note

class RefreshTests(unittest.TestCase):
    def test_trends_keep_source_rank_and_exclude_non_offense(self):
        players={'1':{'full_name':'A','position':'WR','active':True},'2':{'full_name':'B','position':'QB','active':True,'injury_status':'Out'},'3':{'position':'DEF','active':True}}
        data=build({'season':'2026','season_type':'regular','week':12},players,[{'player_id':'3','count':200},{'player_id':'2','count':100}],[])
        self.assertEqual(data['players'][0]['id'],'2')
        self.assertEqual(data['players'][0]['rank'],2)
        self.assertEqual(data['players'][1]['adds'],0)
        self.assertEqual(len(data['players']),2)
        self.assertIn('Injury flag',data['players'][0]['note'])
    def test_missing_data_fails(self):
        with self.assertRaises(AssertionError): build({}, {}, [], [])
    def test_depth_note(self):
        self.assertIn('first',note({'depth_chart_order':1}))

if __name__=='__main__': unittest.main()

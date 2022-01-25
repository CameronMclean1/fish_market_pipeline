import unittest
from fish import fish

class TestFishMethods(unittest.TestCase):

    def test_initiate(self):
        test_row = {'\ufeffSpecies': 'Smelt', 'Weight': '19.9', 'Length1': '13.8', 'Length2': '15', 'Length3': '16.2', 'Height': '2.9322', 'Width': '1.8792'}
        test_fish = fish(test_row)
        self.assertEqual(test_fish.species, 'Smelt')

    def test_update(self):
        test_row = {'\ufeffSpecies': 'Smelt', 'Weight': '19.9', 'Length1': '13.8', 'Length2': '15', 'Length3': '16.2', 'Height': '2.9322', 'Width': '1.8792'}
        test_fish = fish(test_row)
        test_fish.update(test_row)
        self.assertEqual(len(test_fish.stats['Weight']), 2)

    def test_average(self):
        test_row_1 = {'\ufeffSpecies': 'Smelt', 'Weight': '1'}
        test_row_2 = {'\ufeffSpecies': 'Smelt', 'Weight': '2'}
        test_fish = fish(test_row_1)
        test_fish.update(test_row_2)
        average_test_fish = test_fish.average()
        self.assertEqual(average_test_fish['Weight'], 1.5)

if __name__ == '__main__':
    unittest.main()

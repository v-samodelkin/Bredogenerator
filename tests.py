import unittest
import parse_text
import collections
class TextParserTests(unittest.TestCase):

    def test_separate_by_sentence(self):
        p = parse_text.words('''Это был солнечный день''')
        list_words = ["Это", "был", "солнечный", "день"]
        self.assertEqual(list_words, p) 


    def test_sentence_separate(self):
        p = parse_text.sentences('''Это был солнечный день! Прекрасная погода!!! ЖИЗНЬ ХОРОША&#^@&!!!''')
        list_words = ["Это был солнечный день", " Прекрасная погода", " ЖИЗНЬ ХОРОША"]
        self.assertEqual(list_words, p) 
        
    def test_bigramms(self):
        p = parse_text.bigramms('''Привет всем вам! Как дела?''')
        self.assertEqual({'всем': collections.Counter({'вам': 1}),
                          'Как': collections.Counter({'дела': 1}),
                          'Привет' : collections.Counter({'всем' : 1})}, p)   
                          
    def test_rate_words(self):
        p = parse_text.rate_words('один два два три три три')
        self.assertEqual(p,[('три',3), ('два', 2), ('один', 1)])

        
    def test_nowords(self):
        f = open('test_nowords.txt', 'rt')
        p = parse_text.nowords(f, 'Привет 1 всем! 22 Как 333 дела? 11 2 3333')
        f.close()
        self.assertEqual(p, 'Привет всем! Как дела? 11 2 3333')
        
    def test_all_pairs(self):
        a = parse_text.all_pairs('Давайте. Сделаем биграммы. По целым предложениям. Окей?',
                                      1,
                                      False,
                                      False)
        self.assertEqual(sorted(a), [(("По", "целым"), 1), (("Сделаем", "биграммы"), 1), (("целым", "предложениям"), 1)])
        
if __name__=="__main__":
    unittest.main()
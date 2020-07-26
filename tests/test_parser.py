import unittest
import bibtexparser as bp

class TestBibtexparser(unittest.TestCase):

    def setUp(self):
        bp.reset_to_default_settings()
        self.parser = bp.bibparser.BibTexParser()
    def tearDown(self):
        bp.BibDefinitions.reset()
        del self.parser

    def test_processing_entry_type(self):
        # the entry type should be put in lower case. Else it should not be changed.
        test_string = """
        @article{id,
        author = {Test. M},
        title = {Title},""" 
        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry["ENTRYTYPE"],"article")

        test_string = """
        @BOOK{id,
        author = {Test. M},
        title = {Title},""" 
        test_entry = self.parser.parse(test_string)

        self.assertEqual(test_entry["ENTRYTYPE"],"book")

        test_string = """
        @rEport4{id,
        author = {Test. M},
        title = {Title},""" 
        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry["ENTRYTYPE"],"report4")

    def test_processing_key_with_standard_replacements(self):
        # this should put the proccessed key in lower case also the key should be changed according parser. entry_key_replacements. 
        test_string = """
        @article{id,
        AUTHOR = {Test. M},
        title = {Title},
        keyw = {a,t,bhie,jfie},
        url = "www.test.de",
        Editors = "marta",
        }
        """ 
        test_entry = self.parser.parse(test_string)

        self.assertIn("author",test_entry.keys())
        self.assertIn("title",test_entry.keys())
        self.assertIn("keyword",test_entry.keys())
        self.assertIn("link",test_entry.keys())
        self.assertIn("editor",test_entry.keys())
        
        self.assertNotIn("AUTHOR",test_entry.keys())
        self.assertNotIn("Editors",test_entry.keys())
        self.assertNotIn("url",test_entry.keys())
        self.assertNotIn("keyw",test_entry.keys())
        self.assertNotIn("editors",test_entry.keys())

    def test_processing_key_clear_replacements(self):
        test_string = """
        @article{id,
        AUTHOR = {Test. M},
        title = {Title},
        keyw = {a,t,bhie,jfie},
        url = "www.test.de",
        Editors = "marta",
        }
        """
        
        self.parser.clear_all_key_replacements()
        test_entry = self.parser.parse(test_string)
        
        self.assertIn("author",test_entry.keys())
        self.assertIn("title",test_entry.keys())
        self.assertIn("keyw",test_entry.keys())
        self.assertIn("url",test_entry.keys())
        self.assertIn("editors",test_entry.keys())
        
        self.assertNotIn("AUTHOR",test_entry.keys())
        self.assertNotIn("Editors",test_entry.keys())
        self.assertNotIn("link",test_entry.keys())
        self.assertNotIn("keyword",test_entry.keys())
        self.assertNotIn("editor",test_entry.keys())
        
    def test_processing_key_add_replacements(self):
        test_string = """
        @article{id,
        AUTHOR = {Test. M},
        title = {Title},
        keyw = {a,t,bhie,jfie},
        url = "www.test.de",
        party = "www.test.de",
        Editors = "marta",
        }
        """
        
        self.parser.add_key_replacement("author","writer")
        self.parser.add_key_replacement(["title","url"],["titel","address"])
        self.parser.add_key_replacement(["party","editors"],"extras")
        
        test_entry = self.parser.parse(test_string)
        self.assertIn("writer",test_entry.keys())
        self.assertIn("titel",test_entry.keys())
        self.assertIn("keyword",test_entry.keys())
        self.assertIn("address",test_entry.keys())
        self.assertIn("extras",test_entry.keys())
        
        self.assertNotIn("author",test_entry.keys())
        self.assertNotIn("Editors",test_entry.keys())
        self.assertNotIn("editors",test_entry.keys())
        self.assertNotIn("url",test_entry.keys())
        self.assertNotIn("link",test_entry.keys())
        self.assertNotIn("keyw",test_entry.keys())
        self.assertNotIn("title",test_entry.keys())

    def test_processing_key_remove_replacements(self):
        # this should put the proccessed key in lower case also the key should be changed according parser. entry_key_replacements. 
        test_string = """
        @article{id,
        AUTHORs = {Test. M},
        Title = {Title},
        keyw = {a,t,bhie,jfie},
        url = "www.test.de",
        Editors = "marta",
        }
        """
        self.parser.remove_key_replacement("editors")
        self.parser.remove_key_replacement(["url","keyw"])
        
        test_entry = self.parser.parse(test_string)

        self.assertIn("author",test_entry.keys())
        self.assertIn("title",test_entry.keys())
        self.assertIn("keyw",test_entry.keys())
        self.assertIn("url",test_entry.keys())
        self.assertIn("editors",test_entry.keys())
        
        self.assertNotIn("authors",test_entry.keys())
        self.assertNotIn("editor",test_entry.keys())
        self.assertNotIn("link",test_entry.keys())
        self.assertNotIn("keyword",test_entry.keys())


    def test_processing_key_overwrite_replacements(self):
        # this should put the proccessed key in lower case also the key should be changed according parser. entry_key_replacements. 
        test_string = """
        @article{id,
        AUTHORs = {Test. M},
        Title = {Title},
        keyw = {a,t,bhie,jfie},
        url = "www.test.de",
        Editors = "marta",
        }
        """
        self.parser.overwrite_key_replacements({"title":"publisher", "url": "address"})

        test_entry = self.parser.parse(test_string)

        self.assertIn("authors",test_entry.keys())
        self.assertIn("publisher",test_entry.keys())
        self.assertIn("keyw",test_entry.keys())
        self.assertIn("address",test_entry.keys())
        self.assertIn("editors",test_entry.keys())
        
        self.assertNotIn("author",test_entry.keys())
        self.assertNotIn("title",test_entry.keys())
        self.assertNotIn("url",test_entry.keys())
        self.assertNotIn("keyword",test_entry.keys())
        self.assertNotIn("editor",test_entry.keys())

    def test_processing_normal_strings(self):
        test_entry = {"ENTRYTYPE":"article","ID":"test"}

        self.parser.set_entry_field(test_entry,"note","hello")
        self.assertEqual(test_entry["note"],"hello")
        self.parser.set_entry_field(test_entry,"note","{Variation}")
        self.assertEqual(test_entry["note"],"{Variation}")
        self.parser.set_entry_field(test_entry,"note","{L}yapunov and {CO}")
        self.assertEqual(test_entry["note"],"{L}yapunov and {CO}")
        self.parser.set_entry_field(test_entry,"note","Lyapunov and CO")
        self.assertEqual(test_entry["note"],"Lyapunov and CO")
        self.parser.set_entry_field(test_entry,"note","latext strings \"{u}")
        self.assertEqual(test_entry["note"],"latext strings \"{u}")
        self.parser.set_entry_field(test_entry,"note","I call for HELP")
        self.assertEqual(test_entry["note"],"I call for HELP")
        
    def test_processing_protected_uppercase(self):
        test_entry = {"ENTRYTYPE":"article","ID":"test"}

        self.parser.set_entry_field(test_entry,"journal","hello")
        self.assertEqual(test_entry["journal"],"hello")
        self.parser.set_entry_field(test_entry,"journal","Variation")
        self.assertEqual(test_entry["journal"],"Variation")
        self.parser.set_entry_field(test_entry,"journal","{L}yapunov and {CO}")
        self.assertEqual(test_entry["journal"],"Lyapunov and CO")
        self.parser.set_entry_field(test_entry,"journal","Lyapunov and CO")
        self.assertEqual(test_entry["journal"],"Lyapunov and CO")
        self.parser.set_entry_field(test_entry,"journal",'latext strings \\"{u}')
        self.assertEqual(test_entry["journal"],'latext strings \\"{u}')
        self.parser.set_entry_field(test_entry,"journal","I call for HELP")
        self.assertEqual(test_entry["journal"],"I call for HELP")


    def test_processing_latex_strings(self):
        test_entry = {"ENTRYTYPE":"article","ID":"test"}

        self.parser.set_entry_field(test_entry,"title","hello")
        self.assertEqual(test_entry["title"],"hello")
        self.parser.set_entry_field(test_entry,"title","{Variation}")
        self.assertEqual(test_entry["title"],"{Variation}")
        self.parser.set_entry_field(test_entry,"title","{L}yapunov and {CO}")
        self.assertEqual(test_entry["title"],"Lyapunov and CO")
        self.parser.set_entry_field(test_entry,"title","Lyapunov and CO")
        self.assertEqual(test_entry["title"],"Lyapunov and CO")
        self.parser.set_entry_field(test_entry,"title","latext strings \\\"{u}")
        self.assertEqual(test_entry["title"],"latext strings ü")
        self.assertNotEqual(test_entry["title"],"latext strings \\\"{u}")
        self.parser.set_entry_field(test_entry,"title","I call for HELP")
        self.assertEqual(test_entry["title"],"I call for HELP")

    def test_processing_internal_integer_fields(self):
        test_entry = {"ENTRYTYPE":"article","ID":"test"}

        self.parser.set_entry_field(test_entry,"month","hello")
        self.assertEqual(test_entry["month"],"hello")
        self.parser.set_entry_field(test_entry,"month","June")
        self.assertEqual(test_entry["month"],6)
        self.parser.set_entry_field(test_entry,"month","7")
        self.assertEqual(test_entry["month"],7)
        self.parser.set_entry_field(test_entry,"month","dec")
        self.assertEqual(test_entry["month"],12)
        self.assertIn("hello",bp.BibDefinitions.get_non_recognised_string_fields("month"))

    def test_processing_author_fields(self):
        test_entry = {"ENTRYTYPE":"article","ID":"test"}

        self.parser.set_entry_field(test_entry,"author","{S. St\\\"{u}dli} and Peters, Edwin")
        self.assertEqual(len(test_entry["author"]),2)
        self.assertIn("S. Stüdli", test_entry["author"])
        self.assertIn("Peters, Edwin", test_entry["author"])

    def test_adding_internal_integer_fields(self):
        bp.BibDefinitions.add_stored_as_integer('author',{"s. stüdli":1,"stüdli, s.":1,"e. peters": 2,"peters, e.":2, "peters, edwin":2},['',"Stüdli, S.", "Peters, E."])
        test_entry = {"ENTRYTYPE":"article","ID":"test"}

        self.parser.set_entry_field(test_entry,"author","{S. St\\\"{u}dli} and Peters, Edwin and R. Holland")
        self.assertIn(1, test_entry["author"])
        self.assertIn(2, test_entry["author"])
        self.assertIn("R. Holland", test_entry["author"])
        self.assertIn("r. holland", bp.BibDefinitions.get_non_recognised_string_fields("author"))
        self.assertEqual(len(test_entry["author"]),3)
        
    def test_basic_bibtex_string_parse(self):
        test_string = """
        @article{id,
        author = {Test. M},
        title = {Title},
        journal = {Journal Name},
        volume = {85},
        number = {8},
        pages = {1130 - 1145},
        year = {2012},
        doi = {10.1080/00207179.2012.679970},
        URL = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},
        eprint = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},}"""

        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry['ENTRYTYPE'], 'article')
        self.assertEqual(test_entry['ID'], 'id')
        self.assertEqual(test_entry['author'], ['Test. M'])
        self.assertEqual(test_entry['title'], 'Title')
        self.assertEqual(test_entry['journal'], 'Journal Name')
        self.assertEqual(test_entry['volume'], '85')
        self.assertEqual(test_entry['number'], '8')
        self.assertEqual(test_entry['pages'], '1130 - 1145')
        self.assertEqual(test_entry['doi'], '10.1080/00207179.2012.679970')
        self.assertEqual(test_entry['year'], '2012')
        self.assertEqual(test_entry['link'], 'http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970')
        
    def test_basic_bibtex_string_parse_with_comma_in_title(self):
        test_string = """
        @article{id,
        author = {Test. M},
        title = {Title, that is long, and filled with commas},
        journal = {Journal Name},
        volume = {85},
        number = {8},
        pages = {1130 - 1145},
        year = {2012},
        doi = {10.1080/00207179.2012.679970},
        URL = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},
        eprint = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},}"""

        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry['ENTRYTYPE'], 'article')
        self.assertEqual(test_entry['ID'], 'id')
        self.assertEqual(test_entry['author'], ['Test. M'])
        self.assertEqual(test_entry['title'], 'Title, that is long, and filled with commas')
        self.assertEqual(test_entry['journal'], 'Journal Name')
        self.assertEqual(test_entry['volume'], '85')
        self.assertEqual(test_entry['number'], '8')
        self.assertEqual(test_entry['pages'], '1130 - 1145')
        self.assertEqual(test_entry['doi'], '10.1080/00207179.2012.679970')
        self.assertEqual(test_entry['year'], '2012')
        self.assertEqual(test_entry['link'], 'http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970')

    def test_basic_bibtex_string_parse_with_strings(self):
        test_string = """
        @article{id,
        author = {Test. M},
        title = {Title},
        journal = journalname # etc,
        volume = 85,
        number = 8,
        pages = 1130 - 1145,
        year = {2012},
        doi = {10.1080/00207179.2012.679970},
        URL = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},
        eprint = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},}"""

        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry['ENTRYTYPE'], 'article')
        self.assertEqual(test_entry['ID'], 'id')
        self.assertEqual(test_entry['author'], ['Test. M'])
        self.assertEqual(test_entry['title'], 'Title')
        self.assertEqual(test_entry['journal'], 'journalname # etc')
        self.assertEqual(test_entry['volume'], '85')
        self.assertEqual(test_entry['number'], '8')
        self.assertEqual(test_entry['pages'], '1130 - 1145')
        self.assertEqual(test_entry['doi'], '10.1080/00207179.2012.679970')
        self.assertEqual(test_entry['year'], '2012')
        self.assertEqual(test_entry['link'], 'http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970')

    def test_real_bibtex_string_parse(self):
        test_string= """
        @arTicle{evcharging2012ijc,
        author = {St\\"{u}dli, S. and Crisostomi, E. and Middleton, R. and Shorten, R.},
        year = {2012},
        doi = {10.1080/00207179.2012.679970},
        journal = {International Journal of Control},
        number = {8},
        pages = {1130 - 1145},
        publisher = {Taylor \& Francis},
        title = {A flexible distributed framework for realising electric and plug-in hybrid vehicle charging policies},
        volume = {85},
        }
        """
        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry['ENTRYTYPE'], 'article')
        self.assertEqual(test_entry['ID'], 'evcharging2012ijc')
        self.assertEqual(test_entry['author'], ['Stüdli, S.','Crisostomi, E.','Middleton, R.', 'Shorten, R.'])
        self.assertEqual(test_entry['title'], 'A flexible distributed framework for realising electric and plug-in hybrid vehicle charging policies')
        self.assertEqual(test_entry['journal'], 'International Journal of Control')
        self.assertEqual(test_entry['number'], '8')
        self.assertEqual(test_entry['pages'], '1130 - 1145')
        self.assertEqual(test_entry['publisher'], 'Taylor & Francis')
        self.assertEqual(test_entry['doi'], '10.1080/00207179.2012.679970')
        self.assertEqual(test_entry['year'], '2012')
        self.assertEqual(test_entry['volume'], '85')
        self.assertNotIn('link',test_entry.keys())

    def test_real_bibtex_string_parse_with_string_delimineters(self):
        test_string= """
        @arTicle{evcharging2012ijc,
        author = "St\\"{u}dli, S. and Crisostomi, E. and Middleton, R. and Shorten, R.",
        year = "2012",
        doi = "10.1080/00207179.2012.679970",
        journal = "International Journal of Control",
        number = "8",
        pages = "1130 - 1145",
        publisher = "Taylor \& Francis",
        title = "A flexible distributed framework for realising electric and plug-in hybrid vehicle charging policies",
        volume = "85",
        }
        """
        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry['ENTRYTYPE'], 'article')
        self.assertEqual(test_entry['ID'], 'evcharging2012ijc')
        self.assertEqual(test_entry['author'], ['Stüdli, S.','Crisostomi, E.','Middleton, R.', 'Shorten, R.'])
        self.assertEqual(test_entry['title'], 'A flexible distributed framework for realising electric and plug-in hybrid vehicle charging policies')
        self.assertEqual(test_entry['journal'], 'International Journal of Control')
        self.assertEqual(test_entry['number'], '8')
        self.assertEqual(test_entry['pages'], '1130 - 1145')
        self.assertEqual(test_entry['publisher'], 'Taylor & Francis')
        self.assertEqual(test_entry['doi'], '10.1080/00207179.2012.679970')
        self.assertEqual(test_entry['year'], '2012')
        self.assertEqual(test_entry['volume'], '85')
        self.assertNotIn('link',test_entry.keys())

    def test_real_bibtex_string_parse_with_double_delimineters(self):
        test_string= """
        @arTicle{evcharging2012ijc,
        author = {{Corporation and Inc}},
        year = {"2012"},
        doi = "10.1080/00207179.2012.679970",
        journal = {"International Journal of Control"},
        number = ""8"",
        pages = "{1130 - 1145}",
        publisher = "Taylor \& Francis",
        title = "A flexible distributed framework for realising electric and plug-in hybrid vehicle charging policies",
        volume = {{85}},
        }
        """
        test_entry = self.parser.parse(test_string)
        
        self.assertEqual(test_entry['ENTRYTYPE'], 'article')
        self.assertEqual(test_entry['ID'], 'evcharging2012ijc')
        self.assertEqual(test_entry['author'], ['Corporation and Inc'])
        self.assertEqual(test_entry['title'], 'A flexible distributed framework for realising electric and plug-in hybrid vehicle charging policies')
        self.assertEqual(test_entry['journal'], '"International Journal of Control"')
        self.assertEqual(test_entry['number'], '"8"')
        self.assertEqual(test_entry['pages'], '{1130 - 1145}')
        self.assertEqual(test_entry['publisher'], 'Taylor & Francis')
        self.assertEqual(test_entry['doi'], '10.1080/00207179.2012.679970')
        self.assertEqual(test_entry['year'], '"2012"')
        self.assertEqual(test_entry['volume'], '{85}')
        self.assertNotIn('link',test_entry.keys())

        
    def test_load_function(self):
        test_string = """
        @article{id,
        author = {Test. M},
        title = {Title},
        journal = {Journal Name},
        volume = {85},
        number = {8},
        pages = {1130 - 1145},
        year = {2012},
        doi = {10.1080/00207179.2012.679970},
        URL = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},
        eprint = {http://www.tandfonline.com/doi/abs/10.1080/00207179.2012.679970},}"""        
        self.assertEqual(self.parser.parse(test_string),bp.load(test_string))
        
if __name__ =="__main__":
    unittest.main()


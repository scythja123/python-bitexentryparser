import unittest
import bibtexparser as bp

class TestBibtexparser(unittest.TestCase):

    def setUp(self):
        bp.reset_to_default_settings()
        self.writer= bp.bibwriter.BibTexWriter()
    def tearDown(self):
        bp.BibDefinitions.reset()
        del self.writer

    def test_writing_normal_basic(self):
        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 6,
            "note": "Normal string output \\\"{u}"
        }

        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"{S. St\\\"{u}dli and E. Peters}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"{{L}yapunov and {CO}: {L}atex strings \\\"{u}}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"{June}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"{Normal string output \\\"{u}}")

        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": "test",
            "note": "Normal string output \\\"{u}"
        }

        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"{S. St\\\"{u}dli and E. Peters}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"{{L}yapunov and {CO}: {L}atex strings \\\"{u}}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"{test}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"{Normal string output \\\"{u}}")

        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 90,
            "note": "Normal string output \\\"{u}"
        }

        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"{S. St\\\"{u}dli and E. Peters}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"{{L}yapunov and {CO}: {L}atex strings \\\"{u}}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"{90}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"{Normal string output \\\"{u}}")


    def test_writing_normal_option_opening_closing_character(self):
        self.writer.opening_field_character = "\""
        self.writer.closing_field_character = "\""
        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 3,
            "note": "Normal string output \\\"{u}"
        }

        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"\"S. St\\\"{u}dli and E. Peters\"")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"\"{L}yapunov and {CO}: {L}atex strings \\\"{u}\"")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"\"March\"")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"\"Normal string output \\\"{u}\"")

    def test_writing_string(self):
        self.writer.add_write_as_string_field("month",['','january','february','march','april'])
        self.writer.add_write_as_string_field("note")

        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 3,
            "note": "Test"
        }
        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"{S. St\\\"{u}dli and E. Peters}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"{{L}yapunov and {CO}: {L}atex strings \\\"{u}}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"march")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"Test")

        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 10,
            "note": 0,
        }
        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"{S. St\\\"{u}dli and E. Peters}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"{{L}yapunov and {CO}: {L}atex strings \\\"{u}}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"{October}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"0")

        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": "unknown",
            "note": "Test"
        }
        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"{S. St\\\"{u}dli and E. Peters}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"{{L}yapunov and {CO}: {L}atex strings \\\"{u}}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"{unknown}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"Test")

        self.writer.remove_write_as_string_field("month")

        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 3,
            "note": "Test"
        }
        self.assertEqual(self.writer.get_entry_field(test_entry,"author"),"{S. St\\\"{u}dli and E. Peters}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"title"),"{{L}yapunov and {CO}: {L}atex strings \\\"{u}}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"month"),"{March}")
        self.assertEqual(self.writer.get_entry_field(test_entry,"note"),"Test")

    def test_write_full_basic(self):
        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 3,
            "note": "Test"
        }
        expected_output = """@article{test,\n    author = {S. St\\\"{u}dli and E. Peters},\n    month = {March},\n    note = {Test},\n    title = {{L}yapunov and {CO}: {L}atex strings \\\"{u}},\n}\n"""
        self.assertEqual(self.writer.write(test_entry),expected_output)

    def test_write_full_option_display_order(self):
        self.writer.display_order = ["title","author"]
        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 3,
            "note": "Test"
        }
        expected_output = """@article{test,\n    title = {{L}yapunov and {CO}: {L}atex strings \\\"{u}},\n    author = {S. St\\\"{u}dli and E. Peters},\n    month = {March},\n    note = {Test},\n}\n"""
        self.assertEqual(self.writer.write(test_entry),expected_output)

    def test_write_full_option_not_display(self):
        self.writer.do_not_display_fields = {"note"}
        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 3,
            "note": "Test"
        }
        expected_output = """@article{test,\n    author = {S. St\\\"{u}dli and E. Peters},\n    month = {March},\n    title = {{L}yapunov and {CO}: {L}atex strings \\\"{u}},\n}\n"""
        self.assertEqual(self.writer.write(test_entry),expected_output)
        
    def test_write_full_option_only_display(self):
        self.writer.do_only_display_fields = {"author","title"}
        test_entry = {
            "ID": "test",
            "ENTRYTYPE": "article",
            "author": ["S. Stüdli","E. Peters"],
            "title": "Lyapunov and CO: Latex strings ü",
            "month": 3,
            "note": "Test"
        }
        expected_output = """@article{test,\n    author = {S. St\\\"{u}dli and E. Peters},\n    title = {{L}yapunov and {CO}: {L}atex strings \\\"{u}},\n}\n"""
        self.assertEqual(self.writer.write(test_entry),expected_output)
        
if __name__ =="__main__":
    unittest.main()


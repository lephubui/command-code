import unittest
from unittest.mock import patch, mock_open
import io
import sys
from word_counter import count_words # Import the function to test

class TestCountWords(unittest.TestCase):
    """Test with a valid file content and custom top_n=3"""
    def test_valid_file_and_top_n(self):
        mock_text = "hello hello word word count from command and code"
        expected = [('hello', 2), ('word', 2), ('count', 1)]
        with patch('word_counter.open', mock_open(read_data=mock_text)):
            result = count_words('fake_path', 3)
            self.assertEqual(result, expected)

    """Test default top_n=5 with sample test"""
    def test_default_top_n(self):
        mock_text = "hello hello hello word word count from command and code"
        expected = [('hello', 3), ('word', 2), ('count', 1), ('from', 1), ('command', 1)]
        with patch('word_counter.open', mock_open(read_data=mock_text)):
            result = count_words('fake_path')
            self.assertEqual(result, expected)

    """Test file not found FileNotFoundError handling"""
    def test_file_not_found(self):
        with patch('word_counter.open') as mock_file:
            mock_file.side_effect = FileNotFoundError("No such file")
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                result = count_words('fake_path')
                self.assertIsNone(result)
                output = fake_out.getvalue().strip()
                self.assertEqual(output, "Yo, we got an error: No such file")

# Driver code
if __name__ == '__main__':
    unittest.main()

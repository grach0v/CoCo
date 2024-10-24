import numpy as np
import re
from typing import List, Tuple, Union
from base_data_collector import BaseDataSampler

class SimpleSplitDataSampler(BaseDataSampler):
    def __init__(
            self, 
            files: List[str], 
            max_prefix: int, 
            max_middle: int, 
            max_suffix: int, 
            splitters: List[str],
        ):
        """
        Initializes the SimpleSplitDataSampler with the given files, maximum lengths for prefix, middle, and suffix, and splitters.

        Args:
            files (List[str]): List of file paths to sample from.
            max_prefix (int): Maximum length of the prefix.
            max_middle (int): Maximum length of the middle part.
            max_suffix (int): Maximum length of the suffix.
            splitters (List[str]): List of splitters to use for splitting lines.
        """
        super().__init__(files, max_prefix, max_middle, max_suffix)
        self.pattern = '|'.join(map(re.escape, splitters))

    def finish_line(
            self, 
            lines: List[str], 
            max_tries: int = 3, 
            max_lines_pred: int = 3
        ) -> Tuple[bool, Union[str, None], Union[str, None], Union[str, None], Union[str, None]]:
        """
        Attempts to finish a line by finding a match for the pattern within the given lines.

        Args:
            lines (List[str]): The lines to search within.
            max_tries (int): The maximum number of attempts to find a match.
            max_lines_pred (int): The maximum number of lines to predict. Defaults to 3.

        Returns:
            Tuple[bool, Union[str, None], Union[str, None], Union[str, None], Union[str, None]]: 
            A tuple containing a success flag, the prefix, the middle part, the suffix, and a label.
        """
        for _ in range(max_tries):
            cursor_line = np.random.randint(len(lines))
            matches = [match.start() for match in re.finditer(self.pattern, lines[cursor_line])]

            if len(matches) == 0:
                continue

            cursor_pos = np.random.choice(matches, 1)[0]
            lines_pred = np.random.randint(min(max_lines_pred, len(lines) - cursor_line))

            prefix = ''.join(lines[:cursor_line + 1]) + lines[cursor_line][:cursor_pos]
            middle = lines[cursor_line][cursor_pos:] + lines[cursor_line + lines_pred]
            suffix = ''.join(lines[cursor_line + lines_pred + 1:])

            if len(middle) <= self.max_middle:
                break

            prefix = prefix[-self.max_prefix:]
            suffix = suffix[:self.max_suffix]

        else:
            return False, None, None, None, None
        
        return True, prefix, middle, suffix, 'finish_line'
    
    def finish_words(
            self, 
            lines: List[str], 
            max_tries: int = 3, 
            max_letters_word: int = 2, 
            max_words_pred: int = 20
        ) -> Tuple[bool, Union[str, None], Union[str, None], Union[str, None], Union[str, None]]:
        """
        Attempts to finish words by finding matches for the pattern within the given lines.

        Args:
            lines (List[str]): The lines to search within.
            max_tries (int): The maximum number of attempts to find a match.
            max_letters_word (int): The maximum number of letters to shift. Defaults to 2.
            max_words_pred (int): The maximum number of words to predict. Defaults to 20.

        Returns:
            Tuple[bool, Union[str, None], Union[str, None], Union[str, None], Union[str, None]]: 
            A tuple containing a success flag, the prefix, the middle part, the suffix, and a label.
        """
        file = ''.join(lines)
        matches = [match.start() for match in re.finditer(self.pattern, file)]
        matches.append(len(file))
           
        for _ in range(max_tries):
        
            match_i = np.random.randint(len(matches) - 1)
            max_shift = min(max_letters_word, matches[match_i + 1] - matches[match_i])
            shift = np.random.randint(max_shift)

            cursor_pos = match_i + shift
            match_end = np.random.randint(match_i + 1, match_i + max_words_pred + 1)
            match_end = min(match_end, len(matches) - 1)
            cursor_end = matches[match_end]

            prefix = file[:cursor_pos]
            middle = file[cursor_pos: cursor_end]
            suffix = file[cursor_end:]

            if len(middle) <= self.max_middle:
                break

            prefix = prefix[-self.max_prefix:]
            suffix = suffix[:self.max_suffix]

        else:
            return False, None, None, None, None
        
        return True, prefix, middle, suffix, 'finish_words'

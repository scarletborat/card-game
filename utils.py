import re

def one_str_occurrence(string, substring):
    pattern = r'^[^{0}]*{0}[^{0}]*$'.format(re.escape(substring))
    matches = re.findall(pattern, string)
    return len(matches) == 1

def text_bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"

    return bold_start + text + bold_end
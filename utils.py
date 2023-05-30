import re

def one_str_occurrence(string, substring):
    pattern = r'^[^{0}]*{0}[^{0}]*$'.format(re.escape(substring))
    matches = re.findall(pattern, string)
    return len(matches) == 1
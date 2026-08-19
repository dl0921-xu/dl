import re

with open('global-emerging-markets-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ALL Chinese quotes in the entire file
content = content.replace('\u201c', '\\u201c')  # "
content = content.replace('\u201d', '\\u201d')  # "

# Also fix any broken unicode escapes
content = content.replace('\\\\u201c', '\\u201c')
content = content.replace('\\\\u201d', '\\u201d')

with open('global-emerging-markets-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed all Chinese quotes in entire file')

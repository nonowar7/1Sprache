import re
s = "a//b/c f/d"

print(re.split('/|//', s)[-1])
print(re.sub(r'(^|\s).+?(//|/)', ' ', s).strip())
print(re.search(r'(.*)/(.*)', s).group(2))
import re
def key(self, item):
    result = re.search(r"\\[a-zA-Z]+\d*\s?",item)
    print(result)

def main():
    # ^ 
    print(re.search("^[0123456789]$","12"))
    # 转义
    print(re.search(r"^[012\]345]$", "2345")) 

main()
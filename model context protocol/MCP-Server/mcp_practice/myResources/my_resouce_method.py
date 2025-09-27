

def read_docs():
    with open("myResources/my_python.py") as f:
        content = f.read()
        return content
    
def read_docs_dynamic(path: str):
    with open(f"myResources/{path}") as f:
        content = f.read()
        return content
from fastapi import FastAPI
from app.codesearch import codesearch
from app.welcome import welcome

def create_app():
    app = FastAPI()
    app.include_router(codesearch.csrouter)
    app.include_router(welcome.wrouter)
    return app

app = create_app()

# codebase = None
# encoder_nl = None
# encoder_pl = None
# classifier = None


@app.get("/")
def root():
    return {"message":"hello! welcome to use code search"}

# @app.on_event("startup")
# def load_data():
#     logging.info("加载模型...")
#     print(type(codebase))
#     config = Config()
#     encoder_nl,encoder_pl,classifier = load_model(config)
#     codebase = load_codebase("./data/code_snippets/java_test_1.jsonl",config,encoder_pl)
#     print("加载完成.")
#     print(type(codebase))


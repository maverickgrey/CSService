from transformers import RobertaTokenizer
from definitions import MODEL_DIR,CODE_DIR,CODE_VEC_DIR

class Config:
    def __init__(self,
                code_path = CODE_DIR,
                model_path = MODEL_DIR,
                code_vec_path = CODE_VEC_DIR,
                use_cuda = False,
                max_seq_length=512,
                filter_K = 5,
                final_K = 15,
                confidence = 0.5,
                distance_type = "cosine"
                ):
        self.code_path = code_path
        self.model_path = model_path
        self.code_vec_path = code_vec_path
        self.use_cuda = use_cuda
        self.max_seq_length = max_seq_length
        self.filter_K = filter_K
        self.final_K = final_K
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base-mlm")
        self.confidence = confidence
        self.distance_type = distance_type
# from util.config_class import Config
from util.model import CasEncoder,SimpleCasClassifier
from util.datastruct import CodeBase,CodeStruct
import logging
import torch
import os
import json

def load_model(config):
    encoder_nl = CasEncoder(encode='one')
    encoder_pl = CasEncoder(encode='one')
    classifier = SimpleCasClassifier()
    logging.info("开始加载模型...")
    if os.path.exists(config.model_path+"/encoder3.pt"):
        encoder_nl.load_state_dict(torch.load(config.saved_path+"/encoder3.pt"))
        encoder_pl.load_state_dict(torch.load(config.saved_path+"/encoder3.pt"))

    if os.path.exists(config.model_path+"/classifier2.pt"):
        classifier.load_state_dict(torch.load(config.saved_path+"/classifier2.pt"))

    if config.use_cuda == True:
        encoder_nl = encoder_nl.cuda()
        encoder_pl = encoder_pl.cuda()
        classifier = classifier.cuda()
    
    return encoder_nl,encoder_pl,classifier


# 目前而言load codebase是将某个代码片段及其表示向量存放到CodeStruct数据结构中，然后用CodeBase（一个封装过的列表）来存放这些数据结构
# 采用了空间换时间的策略，先把所有代码段的向量生成出来保存到一个jsonl文件中，这样每次应用启动时就不必用encoder重新生成向量而是直接从文件读取向量
# code_path:存放代码段的文件路径
# vec_path:存放代码段向量的文件路径
def load_codebase(code_path,vec_path,config)->CodeBase:
    code_base = []
    code_file = open(code_path,'r')
    vec_file = open(vec_path,'r')
    codes = code_file.readlines()
    vecs = vec_file.readlines()
    for vec in vecs:
        vec_js = json.loads(vec)
        code_no = vec_js['code_no']
        code_vec = vec_js['code_vec']
        code_js = json.loads(codes[code_no-1])
        code = code_js['code']
        code_tokens = ' '.join(code_js['code_tokens'])
        code_tokens = config.tokenizer.tokenize(code_tokens)
        code_struct = CodeStruct(code_vec,code_tokens,code,code_no)
        code_base.append(code_struct)
    return CodeBase(code_base)
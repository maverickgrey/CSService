# import sys
# sys.path.append("../../")

from fastapi import APIRouter
from script.load_data import load_codebase
from util.request import QueryRequest
from util.response import QueryResponse
import logging
import datetime
from util.utils import query_to_vec,rerank,cos_similarity,get_priliminary,get_info
from util.config_class import Config
from util.model import CasEncoder,SimpleCasClassifier
import os
import torch

csrouter = APIRouter(
    prefix="/codesearch",
    tags=['codesearch']
)

def init():
    config = Config()
    codebase = load_codebase(config.code_path+"/java_test_new.jsonl",config.code_vec_path+"/java_test_new_vec.jsonl",config)
    encoder = CasEncoder('one')
    if os.path.exists(config.model_path+"/encoder3.pt") and config.use_cuda==False:
        encoder.load_state_dict(torch.load(config.model_path+"/encoder3.pt",map_location=torch.device('cpu')))
    elif os.path.exists(config.model_path+"/encoder3.pt") and config.use_cuda==True:
        encoder.load_state_dict(torch.load(config.model_path+"/encoder3.pt"))

    classifier = SimpleCasClassifier()
    if os.path.exists(config.model_path+"/classifier2.pt") and config.use_cuda==False:
        classifier.load_state_dict(torch.load(config.model_path+"/classifier2.pt",map_location=torch.device('cpu')))
    elif os.path.exists(config.model_path+"/classifier2.pt") and config.use_cuda==True:
        classifier.load_state_dict(torch.load(config.model_path+"/classifier2.pt"))
    return encoder,classifier,codebase,config


encoder,classifier,codebase,config = init()


@csrouter.post("/query")
def query_codes(request:QueryRequest):
    query_info = request.query
    query_result,time = query(query_info,config,classifier,encoder,codebase)
    query_result = get_info(query_result)
    response = {"query results":query_result,"time cost":time}
    # response = QueryResponse(query_result)
    return response


def query(query,config,classifier,encoder_nl,codebase):
    res = []
    start_time = datetime.datetime.now()
    query_tokens = query.split(' ')
    query_vec = query_to_vec(query,config,encoder_nl).cpu()
    scores = cos_similarity(query_vec,codebase.code_vecs)
    scores = scores.detach().numpy()
    pre = get_priliminary(scores,codebase,config)
    for _pre in pre:
        final = rerank(query_tokens,_pre,classifier,config)
        res = final
    final_time = datetime.datetime.now()
    time_cost = (final_time-start_time).seconds
    logging.info("本次查询消耗时间：{}s".format(time_cost))
    return res,time_cost


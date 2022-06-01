
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

from query_expander import QueryExpander

api = FastAPI(
    title='Query Expansion API',
    description='API for expanding search query using relationships captured in an entity graph',
    version='1.0.0'
)


class QueryData(BaseModel):
    query: str

    class Config:
        schema_extra = {
            'example': {'query': 'apple computers'}
        }


@api.get("/query_expand",
         summary='Obtain query expanded by entity relation graph',
         response_description="Dictionary of expanded terms that are related to the entities in the orignal query",
         responses={
             200: {
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             'error_message': '',
                             'expanded_query': {'0_4': {'iPhone': 1, 'Mac': 1}}
                         }
                     }
                 }
             }
         })
def get_expanded_query(query_data: QueryData) -> Dict[str, Dict[str, int]]:
    '''
    Returned data has a following structure:

    {
        '[startindex]_[endindex]' : {
                                        '[related_entity_string]' : number_of_hops_from_original
                                    }
        }

    startindex: starting string index of the entity in the orginal query
    endindex: ending string index (inclusive) of the entity in the orginal query
    related_entity_string: the entity related to the query entity in the form of a text string
    number_of_hops_from_original: number of edges between the original entity and related entity

    '''

    body = {}
    body['error_message'] = ''
    query_expander = QueryExpander()
    expanded_query_list = query_expander.expand(query_data.query)
    body['expanded_query'] = expanded_query_list
    body['status'] = 'success'
    return body

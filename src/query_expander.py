
from typing import Dict

import requests


class QueryExpander():

    NER_URL = 'http://test:8000/test/'
    ENTITY_LINKING_URL = 'http://test:8001/test/'
    RELATED_ENTITY_URL = ''

    def expand(self, query: str) -> Dict[str, Dict[str, int]]:
        body = {'sentence': query}

        # entities is a dict with key '{startindex}_{endindex}': 'PNERClass}', sorted in increasing order by startindex
        entities = requests.get(
            self.NER_URL, json=body)

        body['entity_locations'] = self._get_entity_location_list(entities)

        # entity_ids is a list of integer ids of the entities in location list
        entity_ids = requests.get(
            self.ENTITY_LINKING_URL, json=body)

        body = {'entity_ids': entity_ids}

        # related_entities is a list of dict of  that are related to the original entity

        # related_entities[i] is a dict which items are entities related to i
        # the key that is the related entity string,
        # the value is the number of hops from the original entity i
        related_entities = requests.get(
            self.RELATED_ENTITY_URL, json=body)

        return related_entities

    def _get_entity_location_list(self, entities):
        entity_location_list = []

        for location_string in entities:
            start_index, end_index = location_string.split('_')
            entity_location_list.append((int(start_index), int(end_index)))

        return entity_location_list

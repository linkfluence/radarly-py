"""
The pivot table is a Radarly's feature which allows you to perform
cross data analysis.
"""

from .api import RadarlyApi
from .utils._internal import CallableDict, id_to_value
from .utils.misc import to_snake_case


class PivotTable(dict):
    """Dict-like object storing data of the pivot table.
    It is strongly advised to use ``pandas`` to explore this object.

    >>> import pandas as pd
    >>> table
    PivotTable(pivot='Elegance', against='focuses')
    >>> df_table = pd.DataFrame(table)
    >>> df_table.head()
                             CHANEL F&B  Dior F&B
    doc ARMANI Fragrances          6722      5196
        BURBERRY Fragrances        5472      3494
        CHANEL Fragrances        130240     21481
        CLINIQUE Fragrances        1150       835
        DIOR Fragrances           21516     83880
    """
    def __init__(self, data, focuses=None, fields=None):
        super().__init__()
        if focuses is None: focuses = {}
        if fields is None: fields = {}
        translator = CallableDict(focuses, fields)
        self.pivot = data['pivot']
        self.against = data['against']
        for focus in data[to_snake_case(self.pivot)]:
            for element in focus[to_snake_case(self.against)]:
                focus_id = element['term'].replace('focus_', '')
                term = translator(focus_id)
                self.setdefault(term, dict())
                self[term].update({
                    (metric, translator.get(
                        focus['term'].replace('focus_', ''), focus['term'])
                    ): element['counts'][metric]
                    for metric in focus['counts']
                })

    def __repr__(self):
        return '<PivotTable.pivot={0.pivot}.against={0.against}>'.format(self)

    @classmethod
    def fetch(cls, project_id, parameter,
              autotranslate=False, focuses=None, fields=None,
              api=None):
        """Retrieve data from the API in order to build the pivot table object.

        Args:
            project_id (int): identifier of the project
            parameter (PivotParameter): parameter used to restrict data
                used to build the pivot table. See ``PivotParameter``
                documentation to see how to build this object.
            autotranslate (bool): whether or not translate the headers and the
                index in order to have labels and not integer ids. If True, it
                will consume one extra request.
            focuses (dict, optional): dictionary used to translate the headers
                (if *against* is set to 'focus' in the parameter)
            fields (dict, optional): dictionary used to translate the index
            api (RadarlyApi, optional): API used to make the
                request. If None, the default API will be used.
        Returns:
            PivotTable: data from the pivot table. You can use ``pandas`` to
            interact with it.
        """
        api = api or RadarlyApi.get_default_api()
        url = api.router.pivot_table['fetch'].format(project_id=project_id)
        data = api.post(url, data=parameter)

        if autotranslate and not focuses and not fields:
            from .project import Project
            project = Project.find(pid=project_id)
            focuses = id_to_value(getattr(project, 'focuses'), 'focuses')
            fields = id_to_value(getattr(project, 'tags'), 'tags')

        return cls(data, focuses, fields)

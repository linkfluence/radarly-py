"""
Radarly gives you an option in order to get the geographical distribution
of your publications. You can also compute some advanced search using, for
example, a polygon made of coordinates in order to get statistics in a specific
region.
"""

from .api import RadarlyApi
from .utils.router import Router


class GeoGrid(list):
    """List-like object used to store the data related to the geographical
    disitribution. Each item corresponds to a geographical point. This object
    is compatible with ``pandas``.

    Example:

        >>> import pandas as pd
        >>> geo_distribution
        GeoGrid(nb_points=1004)
        >>> df_geo = pd.DataFrame(geo_distribution)
        >>> df_geo.head()
            doc geohash       lat        lon
        0  2857     u09  48.85482    2.33683
        1  1995     ucf  55.74689   37.58481
        2   976     dr5  40.68962  -74.01365
        3   969     gcp  51.47043   -0.20134
        4   851     wec  22.30178  114.15957
    """
    def __init__(self, data):
        super().__init__()
        for geoitem in data:
            geoitem.update(geoitem.pop('centroid'))
            geoitem.update(geoitem.pop('counts'))
            self.append(geoitem)

    def __repr__(self):
        return '<GeoGrid.length={}>'.format(len(self))

    @classmethod
    def fetch(cls, project_id, search_parameter, api=None):
        """Retrive geographical distribution from the API.

        Args:
            project_id (int): unique identifier of the project
            search_parameter (GeoParameter): parameter to specify how to
                compute the geographical distribution. See ``GeoParameter``
                documentation to see how to build this object.
            api (RadarlyApi, optional): API used to make the
                request. If None, the default API will be used.
        Returns:
            GeoGrid: list-like object compatible with ``pandas``
        """
        api = api or RadarlyApi.get_default_api()
        url = Router.geogrid['fetch'].format(project_id=project_id)
        data = api.post(url, data=search_parameter)
        return cls(data)
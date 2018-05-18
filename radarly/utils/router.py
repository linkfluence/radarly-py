"""
Module to handle all roads used to retrieve data.
"""


class Router:
    """Roads defined by the Radarly's API. Each attribute is a dictionary
    storing URLs of the same category."""
    analytics = {
        'global': '/projects/{project_id}/insights.json',
        'occupation': '/projects/{project_id}/insights/occupation.json'
    }
    benchmark = {
        'fetch': '/projects/{project_id}/benchmark.json',
    }
    cloud = {
        'fetch': '/projects/{project_id}/insights/cloud.json',
    }
    cluster = {
        'fetch': '/projects/{project_id}/stories.json',
    }
    distribution = {
        'fetch': '/projects/{project_id}/inbox/distribution.json',
    }
    geogrid = {
        'fetch': '/projects/{project_id}/geogrid.json',
    }
    influencer = {
        'search': '/projects/{project_id}/influencers.json',
        'find': '/projects/{project_id}/influencer.json',
    }
    localization = {
        'fetch': '/projects/{project_id}/insights/geo/{region_type}.json',
    }
    pivot_table = {
        'fetch': '/projects/{project_id}/insights/pivot.json',
    }
    project = {
        'find': '/projects/{project_id}.json',
    }
    publication = {
        'search': '/projects/{project_id}/inbox/search.json',
        'metadata': '/projects/{project_id}/documents.json',
        'raw': '/projects/{project_id}/documents/raw.json',
    }
    social_performance = {
        'fetch': '/projects/{project_id}/performance.json',
    }
    topicwheel = {
        'fetch': '/projects/{project_id}/topicwheel.json',
    }
    user = {
        'me': '/users.json',
    }

import syncclientlog


def pages():
    """
    Return the pages exposed for this plugin to Roam
    :return: list of pages for Roam to show
    """
    return [syncclientlog.SyncClientLogPlugin]


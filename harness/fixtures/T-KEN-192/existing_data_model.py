class Scene:
    def __init__(self, id, title, performers):
        self.id = id
        self.title = title
        self.performers = performers  # a list, needs flattening for CSV

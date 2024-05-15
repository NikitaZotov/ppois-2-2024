from view.SearchByFilterDialog import SearchByFilterDialog


class DeleteByFilter(SearchByFilterDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete by filter")

    def get_search_criteria(self):
        return super().get_search_criteria()
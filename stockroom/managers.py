from django.db import models

class CategoryChildrenManager(models.Manager):
    def get_query_set(self):
        return super(CategoryChildrenManager, self).get_query_set().filter(parent=self.id)

class ActiveInventoryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveInventoryManager, self).get_query_set().filter(for_sale=True)

class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name == 'user':
            return 'users_db'
        elif model._meta.model_name == 'product':
            return 'products_db'
        elif model._meta.model_name == 'order':
            return 'orders_db'
        return 'default'
    
    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'user':
            return db == 'users_db'
        elif model_name == 'product':
            return db == 'products_db'
        elif model_name == 'order':
            return db == 'orders_db'
        return db == 'default'
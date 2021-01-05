from app import admin, db
from flask import abort, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from app.models import Adopter, User, Statistic, Host


class CustomModelView(ModelView):

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminOnlyView(CustomModelView):
    can_create = False
    can_edit = True
    can_delete = True
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False


class MixedPermissionModelView(CustomModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            self.can_create = False
            self.can_edit = True
            self.can_delete = True
            self.can_export = True
            return True

        if current_user.has_role('readonly'):
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
            self.can_export = False
            return True

        return False

class UserView(AdminOnlyView):
    form_excluded_columns = ('password')
    column_exclude_list = ('password')


admin.add_view(MixedPermissionModelView(Adopter, db.session))
admin.add_view(MixedPermissionModelView(Statistic, db.session))
admin.add_view(MixedPermissionModelView(Host, db.session))
admin.add_view(UserView(User, db.session))


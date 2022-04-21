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
            self.can_edit = False
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

class AdopterView(MixedPermissionModelView):
    column_list = ['adopter_key', 'send_errors', 'send_usage', 'contact_me', 'first_name', 'last_name',
        'organisation_name', 'department_name', 'country', 'postal_code',
        'city', 'street', 'street_no', 'email', 'created', 'updated']
    column_searchable_list = ['adopter_key']

class StatisticView(MixedPermissionModelView):
    column_list = ['statistic_key', 'adopter_key', 'job_count', 'event_count',
        'series_count', 'user_count', 'ca_count', 'total_minutes', 'created',
        'updated', 'version', 'tenant_count']
    column_searchable_list = ['statistic_key', 'adopter_key']

class HostView(MixedPermissionModelView):
    column_list = ['statistic_key', 'hostname', 'cores', 'max_load', 'memory', 'disk_space', 'services']
    column_searchable_list = ['statistic_key']

class UserView(AdminOnlyView):
    form_excluded_columns = ('password')
    column_exclude_list = ('password')


admin.add_view(AdopterView(Adopter, db.session))
admin.add_view(StatisticView(Statistic, db.session))
admin.add_view(HostView(Host, db.session))
admin.add_view(UserView(User, db.session))


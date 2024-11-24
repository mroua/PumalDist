# middleware/api_log_middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from django.http import HttpResponseForbidden


class APILogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        """if request.user.is_authenticated:
            action_flag = None
            if request.method == 'POST':
                action_flag = ADDITION
            elif request.method in ['PUT', 'PATCH']:
                action_flag = CHANGE
            elif request.method == 'DELETE':
                action_flag = DELETION

            if action_flag:
                # Define the content type or model being acted on
                content_type = ContentType.objects.get_for_model(request.user)

                # Save the log entry to django_admin_log
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=content_type.pk,
                    object_id=request.user.pk,
                    object_repr=force_str(request.user),
                    action_flag=action_flag,
                    change_message=f"{request.method} request on API endpoint {request.path}"
                )"""
        return None
from django.contrib.auth.mixins import UserPassesTestMixin

class MultiGroupRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access based on multiple groups."""
    groups_required = []  

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_active and user.groups.filter(name__in=self.groups_required).exists()

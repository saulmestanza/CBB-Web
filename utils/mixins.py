from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class MultiGroupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to restrict access based on multiple groups."""
    groups_required = []  

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_active and user.groups.filter(name__in=self.groups_required).exists()
    
    def get_context_data(self, **kwargs):
        # Get the current user's groups and add them to the context
        context = super().get_context_data(**kwargs)
        user_group_names = self.request.user.groups.values_list('name', flat=True)
        context['user_group_names'] = user_group_names
        return context

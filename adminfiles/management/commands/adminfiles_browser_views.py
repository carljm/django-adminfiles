from django.core.management.base import NoArgsCommand, CommandError

from adminfiles.settings import ADMINFILES_BROWSER_VIEWS
from adminfiles.views import import_browser, DisableView, BaseView

class Command(NoArgsCommand):
    """
    List all browser views from ADMINFILES_BROWSER_VIEWS and display
    whether each one is enabled or disabled, and why.

    """
    def handle_noargs(self, **options):
        print "Adminfiles browser views available:"
        print
        for browser_path in ADMINFILES_BROWSER_VIEWS:
            try:
                view_class = import_browser(browser_path)
                view_class().check()
                message = 'enabled'
            except (DisableView, ImportError), e:
                message = 'disabled (%s)' % e.args[0]
            if not issubclass(view_class, BaseView):
                message = 'disabled (not subclass of adminfiles.views.BaseView)'
            print " * %s: %s" % (browser_path, message)
            

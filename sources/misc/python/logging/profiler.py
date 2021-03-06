import cProfile
import StringIO
import pstats


class Profiler(object):

    def __init__(self, parent=None, enabled=False, contextstr=None, logger=None):
        self.parent = parent
        self.enabled = enabled

        self.stream = StringIO.StringIO()
        self.contextstr = contextstr or str(self.__class__)

        self.profiler = cProfile.Profile()
        self.logger = logger

    def __enter__(self, *args):

        if not self.enabled:
            return None

        # Start profiling.
        self.stream.write("profile: {}: enter\n".format(self.contextstr))
        self.profiler.enable()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if not self.enabled:
            return

        self.profiler.disable()

        sort_by = 'cumulative'
        ps = pstats.Stats(self.profiler, stream=self.stream).sort_stats(sort_by)
        ps.print_stats(1.0)

        self.stream.write("profile: {}: exit\n".format(self.contextstr))

        return False

    def print_profile_data(self):
        value = self.stream.getvalue()
        print(value)

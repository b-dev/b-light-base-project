# -*- coding: utf-8 -*-

### profiling decorator by Bryan Helmig ###
# Will print hits and time spent for each line of the 'followed' functions, sample usage:

# def get_number():
#     for x in xrange(100000):
#         yield x
#
#
# class HomepageView(TemplateView):
#     template_name = 'homepage.html'
#
#     @do_profile(follow=[get_number])
#     def dispatch(self, request, *args, **kwargs):
#         for x in get_number():
#             x ^ x ^ x
#         return super(HomepageView, self).dispatch(request, *args, **kwargs)


try:
    from line_profiler import LineProfiler

    def do_profile(follow=[]):
        def inner(func):
            def profiled_func(*args, **kwargs):
                try:
                    profiler = LineProfiler()
                    profiler.add_function(func)
                    for f in follow:
                        profiler.add_function(f)
                    profiler.enable_by_count()
                    return func(*args, **kwargs)
                finally:
                    profiler.print_stats()
            return profiled_func
        return inner

except ImportError:
    def do_profile(follow=[]):
        """Helpful if you accidentally leave in production!"""
        def inner(func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)
            return nothing
        return inner

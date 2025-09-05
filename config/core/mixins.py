from django.db.models.functions import Lower

class SearchAndSortMixin:
    search_fields = []
    sort_fields = []
    default_sort = None

    def get_queryset(self):
        queryset = super().get_queryset() # type: ignore
        q = self.request.GET.get("q") # type: ignore


        # Apply search
        if q and self.search_fields:
            from django.db.models import Q
            search_query = Q()
            for field in self.search_fields:
                search_query |= Q(**{f"{field}__icontains": q})
            queryset = queryset.filter(search_query)

        # Apply sorting
        sort = self.request.GET.get("sort") or self.default_sort # type: ignore
        if sort in self.sort_fields or (sort and sort.lstrip("-") in self.sort_fields):
            queryset = queryset.order_by(Lower(sort))

        return queryset
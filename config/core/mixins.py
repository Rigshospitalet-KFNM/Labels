from django.db.models.functions import Lower

class SearchAndSortMixin:
    search_fields = []
    sort_fields = []
    default_sort = None  # e.g., "name"

    def get_queryset(self):
        queryset = super().get_queryset()  # type: ignore
        q = self.request.GET.get("q", "") # type: ignore

        # --- Search ---
        if q and self.search_fields:
            from django.db.models import Q
            search_query = Q()
            for field in self.search_fields:
                search_query |= Q(**{f"{field}__icontains": q})
            queryset = queryset.filter(search_query)

        # --- Sorting ---
        sort_param = self.request.GET.get("sort") or self.default_sort # type: ignore
        if sort_param:
            field_name = sort_param.lstrip("-")
            if field_name in self.sort_fields:
                ordering = Lower(field_name)
                if sort_param.startswith("-"):
                    ordering = ordering.desc()
                queryset = queryset.order_by(ordering)

        return queryset


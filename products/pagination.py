from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Product


class ProductPagination(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        next_page_query = (self.get_next_link().split('/')[-1]
                           if self.get_next_link() else None)

        previous_page_query = (self.get_previous_link().split('/')[-1]
                               if self.get_previous_link() else None)

        max_price = Product.objects.order_by('-price')[0].price
        min_price = Product.objects.order_by('price')[0].price
        max_data = Product.objects.order_by('-data')[0].data
        min_data = Product.objects.order_by('data')[0].data
        max_contract = Product.objects.order_by('-contract_length')[0].contract_length
        min_contract = Product.objects.order_by('contract_length')[0].contract_length

        return Response({
            'pages_count': self.page.paginator.num_pages,
            'products_count': self.page.paginator.count,
            'ordering': self.request.GET.get('ordering'),
            'max_price': max_price,
            'min_price': min_price,
            'max_data': max_data,
            'min_data': min_data,
            'max_contract': max_contract,
            'min_contract': min_contract,
            'current': self.page.number,
            'next': next_page_query,
            'previous': previous_page_query,
            'products': data
        })

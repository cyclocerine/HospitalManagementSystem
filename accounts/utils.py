"""
Utility functions for the hospital management system.
Includes pagination, search, and other common utilities.
"""

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(queryset, request, items_per_page=10):
    """
    Paginate a queryset and return paginated data
    
    Args:
        queryset: Django queryset to paginate
        request: HTTP request object
        items_per_page: Number of items per page (default: 10)
    
    Returns:
        Dictionary with paginated data and page object
    """
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'items': page_obj.object_list,
        'is_paginated': paginator.num_pages > 1,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }


def format_currency(amount):
    """Format currency as Indonesian Rupiah"""
    return f"Rp{amount:,.0f}".replace(",", ".")


def format_phone(phone):
    """Format Indonesian phone number"""
    if phone.startswith("0"):
        return f"+62{phone[1:]}"
    return phone

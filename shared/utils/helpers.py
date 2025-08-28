from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(queryset, page_number, per_page=10):
    """Helper function to paginate querysets"""
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def add_success_message(request, message):
    """Add a success message"""
    messages.success(request, message)


def add_error_message(request, message):
    """Add an error message"""
    messages.error(request, message)

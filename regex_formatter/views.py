import re

from django.shortcuts import render
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

from regex_formatter.utils import html_formatted


# Create your views here.

class RequiredFieldError(Exception):
    pass


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        context = {}
        status = 200
        try:
            regex_str = request.POST.get('regex_str')
            format_str = request.POST.get('format_str')
            if not regex_str:
                raise RequiredFieldError('Регулярное выражение не заполненно')
            if not format_str:
                raise RequiredFieldError('Текст не заполнен')
            context = {'regex_placeholder': regex_str}
            format_str = BeautifulSoup(format_str.strip(), 'html.parser').get_text()
            format_placeholder = re.sub(regex_str,
                                        lambda m: f'<span class="highlight">{m.group()}</span>',
                                        format_str)
            all_matches = re.findall(regex_str, format_placeholder)
            context.update({'format_placeholder': mark_safe(format_placeholder),
                            'matches_count': 'бесконечно' if '' in all_matches else len(all_matches)})
        except (re.error, RequiredFieldError) as e:
            context.update({'format_placeholder': format_str,
                            'error': True,
                            'error_description': str(e)})
            status = 400
        return render(request, 'index.html', context, status=status)

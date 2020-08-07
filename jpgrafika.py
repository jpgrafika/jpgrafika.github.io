import os
import sys

from staticjinja import Site

if __name__ == "__main__":
    projects = os.listdir('projects')

    if len(projects) == 2:
        projects += projects
        projects += projects
        projects += projects
        projects += projects
    else:
        projects = sorted(projects, reverse=True)

    photos = []
    k = 0
    for photo in projects:
        k += 1
        position_id = k % 24 or 24
        class_name = f'photo-{chr(position_id + 96)}'
        photos.append({'url': photo, 'class': class_name})

    index_context = {
        'page_name': 'index',
        'photos': photos,
        'photos2': photos
    }
    about_context = {
        'page_name': 'about',
        'text': open('texts/about').read()
    }
    contact_context = {
        'page_name': 'contact'
    }

    site = Site.make_site(contexts=[
        ('index.html', index_context),
        ('about.html', about_context),
        ('contact.html', contact_context),
    ])
    site.render(use_reloader=int(sys.argv[1]) == 1 if len(sys.argv) > 1 else False)

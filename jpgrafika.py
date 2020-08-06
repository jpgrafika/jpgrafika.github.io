import json
import os

from staticjinja import Site


if __name__ == "__main__":
    projects = os.listdir('projects')

    if len(projects) == 2:
        projects += projects
        projects += reversed(projects)

    photos = []
    k = 0
    for photo in projects:
        k += 1
        print(photo)
        photos.append({'url': photo, 'class': f'photo-{chr(k + 96)}'})

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
    site.render(use_reloader=True)

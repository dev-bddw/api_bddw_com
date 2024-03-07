from .special_cases import special_cases

def handle_special_cases(slug : str) -> str:
    '''
    compare slug to list of special cases, change slug if found in special cases
    '''
    if slug not in special_cases.keys():
        slug = slug.lower().replace("-", " ").replace("captains", "captain's").replace("admirals", "admiral's")
    else:
        slug = special_cases[slug]

    return slug



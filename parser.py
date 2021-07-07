import re


def fix_domain(domain: str) -> str:
    sub_domain = [sd for sd in domain.split(';')]

    # fix iso-thes:subGroup URI references
    sub_domain[3] = sub_domain[3].replace(
        '/mt', '/?idg=mt').replace('>', '&idt=th1>')

    # add skos:member
    sub_domain.insert(-2,
                      sub_domain[3].replace('iso-thes:subGroup', 'skos:member'))

    return ';'.join(sub_domain)


def fix_group(group: str) -> str:
    sub_group = [sg for sg in group.split(';')]

    # fix iso-thes:superGroup URI references
    sub_group[-3] = sub_group[-3].replace('/d',
                                          '/?idg=d').replace('>', '&idt=th1>')

    return ';'.join(sub_group)


def fix_added(added: str) -> str:
    sub_added = [sa for sa in added.split(';')]

    iso_thes_subgroup = re.compile(r'(iso-thes:subGroup)')
    iso_thes_supergroup = re.compile(r'(iso-thes:superGroup)')

    if iso_thes_subgroup.search(added):
        # fix iso-thes:subGroup URI references
        sub_added[3] = sub_added[3].replace(
            '/G', '/?idg=G').replace('>', '&idt=th1>')
        # add skos:member
        sub_added.insert(-2,
                         sub_added[3].replace('iso-thes:subGroup', 'skos:member'))
    elif iso_thes_supergroup.search(added):
        # fix iso-thes:superGroup URI references
        sub_added[3] = sub_added[3].replace(
            '/G', '/?idg=G').replace('>', '&idt=th1>')

    return ';'.join(sub_added)


def fix_turtle(element: str) -> str:
    collection = re.compile('a skos:Collection;')
    domain = re.compile(
        r'^<http:\/\/vocabularies.unesco.org\/thesaurus\/\?idg=domain')
    group = re.compile(
        r'^<http:\/\/vocabularies.unesco.org\/thesaurus\/\?idg=mt')
    added = re.compile(
        r'^<http:\/\/vocabularies.unesco.org\/thesaurus\/\?idg=G')

    if collection.search(element):
        if domain.search(element):
            element = fix_domain(element)
        elif group.search(element):
            element = fix_group(element)
        elif added.search(element):
            element = fix_added(element)

    return element


def main():
    with open('data/opentheso.ttl', 'r', encoding='UTF-8') as f:
        turtle = f.read()

    elements = turtle.split('\n\n')

    elements = [fix_turtle(element) for element in elements]

    with open('data/new_opentheso.ttl', 'w', encoding='UTF-8') as f:
        f.write('\n\n'.join(elements))


if __name__ == "__main__":
    main()

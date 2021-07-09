import re

isothes_supergroup = re.compile(
    r'(iso-thes:superGroup)')
isothes_subgroup = re.compile(
    r'(iso-thes:subGroup)')
collection = re.compile(
    r'a skos:Collection;')
domain = re.compile(
    r'^<http:\/\/vocabularies.unesco.org\/thesaurus\/\?idg=domain')
group = re.compile(
    r'^<http:\/\/vocabularies.unesco.org\/thesaurus\/\?idg=mt')
added = re.compile(
    r'^<http:\/\/vocabularies.unesco.org\/thesaurus\/\?idg=G')


def fix_subgroup(element: str, ref: str) -> str:
    if isothes_subgroup.search(element):
        element = element.replace(
            f'/{ref}', f'/?idg={ref}').replace('>', '&idt=th1>')

    return element


def fix_supergroup(element: str, ref: str) -> str:
    if isothes_supergroup.search(element):
        element = element.replace(
            f'/{ref}', f'/?idg={ref}').replace('>', '&idt=th1>')

    return element


def fix_domain(domain: str, ref2: str = 'mt') -> str:
    # fix iso-thes:subGroup URI references
    sub_domain = [fix_subgroup(element=sd, ref=ref2)
                  for sd in domain.split(';')]

    # add skos:member
    # sub_domain.insert(-2, sub_domain[3].replace('iso-thes:subGroup', 'skos:member'))

    return ';'.join(sub_domain)


def fix_group(group: str, ref2: str = 'd') -> str:
    # fix iso-thes:superGroup URI references
    sub_group = [fix_supergroup(element=sg, ref=ref2)
                 for sg in group.split(';')]

    return ';'.join(sub_group)


def fix_turtle(element: str) -> str:
    if collection.search(element):
        if domain.search(element):
            element = fix_domain(element)
        elif group.search(element):
            element = fix_group(element)
        elif added.search(element) and isothes_subgroup.search(element):
            element = fix_domain(domain=element, ref2='G')
        elif added.search(element) and isothes_supergroup.search(element):
            element = fix_group(group=element, ref2='G')

    return element


def main():
    with open('data/opentheso.ttl', 'r', encoding='UTF-8') as f:
        turtle = f.read()

    elements = turtle.split('\n\n')

    print(len(elements))

    elements = [fix_turtle(element) for element in elements]

    with open('data/th1.ttl', 'w', encoding='UTF-8') as f:
        f.write('\n\n'.join(elements))


if __name__ == "__main__":
    main()

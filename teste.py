import re

isothes_supergroup = re.compile(r'(iso-thes:superGroup)')
isothes_subgroup = re.compile(r'(iso-thes:subGroup)')


def fix_subgroup(element: str) -> str:
    if isothes_subgroup.search(element):
        element = element.replace('/mt', '/?idg=mt').replace('>', '&idt=th1>')

    return element


def fix_supergroup(element: str, ref: str) -> str:
    if isothes_supergroup.search(element):
        element = element.replace(
            f'/{ref}', f'/?idg={ref}').replace('>', '&idt=th1>')

    return element


def fix_domain(domain: str) -> str:
    # fix iso-thes:subGroup URI references
    sub_domain = [fix_subgroup(sd) for sd in domain.split(';')]

    # add skos:member
    sub_domain.insert(-2,
                      sub_domain[3].replace('iso-thes:subGroup', 'skos:member'))

    return ';'.join(sub_domain)


def fix_group(group: str, ref: str = 'd') -> str:
    # fix iso-thes:superGroup URI references
    sub_group = [fix_supergroup(element=sg, ref=ref) for sg in group.split(';')]

    return ';'.join(sub_group)


with open('teste.ttl', 'r', encoding='UTF-8') as f:
    turtle = f.read()

print(turtle)
print()

print(fix_group(turtle, ref='G'))
# print(fix_domain(turtle))

from json import load


with open('definitions.json') as fh:
    defs = load(fh)


with open('constants.py', 'w') as fh:
    fh.write(
        '''
class TransportProvider:
  def __init__(self, id):
    self.id = id

'''
    )

    fh.write('  def localized_name(self):\n')
    fh.write('    match self.id:\n')
    for mapping in defs['transport']:
        fh.write(f'      case "{mapping["id"]}":\n')
        fh.write(f'        return _(\'{mapping["translation_key"]}\')\n')

    fh.write('\n')
    fh.write('class TransportProviders:\n')

    for mapping in defs['transport']:
        fh.write(f'  {mapping["id"].upper()} = TransportProvider("{mapping["id"]}")\n')



class RedeemCodeProviders:
    name = 'RedeemCodeProviders'
#

from .conf import test
from buildz import pyz

pyz.lc(locals(), test)


'''

python -c "from buildz import pyz;pyz._pth.add(r'D:\rootz\wsl\gits\musicz_pygm_upd')"

python -m musicz_pygm.run
'''
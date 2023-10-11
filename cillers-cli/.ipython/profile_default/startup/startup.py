
ipy = get_ipython()  # noqa: F821
ipy.run_line_magic('load_ext', 'autoreload')
ipy.run_line_magic('autoreload', '0')

import os  # noqa: E402, F401
import cillers_cli  # noqa: E402

cillers_cli.log.init()

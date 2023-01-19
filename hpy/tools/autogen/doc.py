from .autogenfile import AutoGenFile
import textwrap

from .parse import toC
from .ctx import autogen_ctx_h

CTX_NAME = '_HPyContext_s'

RST_DISCLAIMER = """
.. note: DO NOT EDIT THIS FILE!
    This file is automatically generated by {clsname}
    See also hpy.tools.autogen and hpy/tools/public_api.h

    Run this to regenerate:
        make autogen
"""

class AutoGenRstFile(AutoGenFile):
    LANGUAGE = 'rst'
    PATH = None
    DISCLAIMER = None

    def __init__(self, api):
        if self.DISCLAIMER is None and self.LANGUAGE == 'rst':
            self.DISCLAIMER = RST_DISCLAIMER
        self.api = api


class autogen_function_index(AutoGenRstFile):
    PATH = 'docs/api-reference/function-index.rst'
    LANGUAGE = 'rst'

    def generate(self):
        lines = []
        w = lines.append
        w('HPy Core API Function Index')
        w('###########################')
        w('')
        for func in self.api.functions:
            if func.name[0] != '_':
                w(f'* :c:func:`{func.name}`')
        return '\n'.join(lines)


class autogen_hpy_ctx(AutoGenRstFile):
    PATH = 'docs/api-reference/hpy-ctx.rst'

    def generate(self):
        lines = []
        w = lines.append
        w(textwrap.dedent(
            '''
            HPy Context
            ===========
            
            The ``HPyContext`` structure is also part of the API since it provides handles
            for built-in objects. For a high-level description of the context, please also
            read :ref:`api:hpycontext`.
            
            .. warning:: It is fine to use handles from the context (e.g. ``ctx->h_None``)
                but it is **STRONGLY** discouraged to directly call any context function.
                This is because, for example, when compiling for :term:`CPython ABI`, the
                context functions won't be used.
            '''))
        # Put all variable declarations into a list in order
        # to be able to sort them by their given context index.
        var_decls = list(self.api.variables)

        # sort the list of var declaration by 'decl.ctx_index'
        var_decls.sort(key=lambda x: x.ctx_index)

        w(f'.. c:struct:: {CTX_NAME}')
        w(f'    :module: {autogen_ctx_h.PATH}')
        w('')
        w(f'    .. c:member:: const char *{CTX_NAME}.name')
        w('')
        w(f'    .. c:member:: int {CTX_NAME}.abi_version')
        for var in var_decls:
            w('')
            w(f'    .. c:member:: {toC(var.node)}')
        return '\n'.join(lines)


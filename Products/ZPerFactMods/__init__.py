import logging
logger = logging.getLogger('Products.ZPerFactMods')

fixes = [
    'dbutilsPermissions',
    'defaultError',
    'pageTemplateDefaults',
    'protectedURLs',
    'disableConnectOnLoad',
    # 'logAllEvents',
    ]


# Apply the fixes
for fix in fixes:
    __import__('Products.ZPerFactMods.%s' % fix)
    try:
        logger.info('Applied %s patch' % fix)
    except:
        logger.warn('Could not apply %s' % fix)

import chameleon.zpt.template
from AccessControl.SecurityInfo import ClassSecurityInfo 
# Declare Macros public
chameleon.zpt.template.Macros.security = ClassSecurityInfo()
chameleon.zpt.template.Macros.security.declareObjectPublic()
chameleon.zpt.template.Macros.__allow_access_to_unprotected_subobjects__ = True
logger.info('Patches installed')
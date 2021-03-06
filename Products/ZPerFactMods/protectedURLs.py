#
# Hook into event handlers to add security for protected URLs.
#

import ZPublisher.pubevents
import zope.event
import types
import AccessControl
import logging
logger = logging.getLogger('Products.ZPerFactMods.protectedURLs')

def protectedURLHandler(event):
    # Default to unprotected
    protected = False
    # Paranoia always wins.
    try:      
        # We hook into the publisher right before rendering the page
        if isinstance(event, ZPublisher.pubevents.PubAfterTraversal):
            # Managers may view anything they want.
            if event.request.AUTHENTICATED_USER.has_role('Manager'):
                return
            # Two possibilities: either we have an instancemethod, or a
            # product instance (Python Script or others)
            if isinstance(event.request.PUBLISHED, types.MethodType):
                # For methods we need the immediate parent
                obj = event.request.PARENTS[0]
            else:
                # For product instances we take the object itself.
                obj = event.request.PUBLISHED

            def is_protected(obj):
                # If there's an ID, we control private behaviour by ending the
                # name with an underscore (_)
                if hasattr(obj, 'getId') and obj.getId().endswith('_'):
                    return True

                if hasattr(obj, 'title'):
                    if callable(obj.title):
                        if obj.title().startswith('_protected'):
                            return True
                    elif (isinstance(obj.title, basestring) 
                            and obj.title.startswith('_protected')):
                        return True
                # break recursion if in root object
                if obj.isTopLevelPrincipiaApplicationObject:
                    return False
                # recurse to parent
                return is_protected(obj.aq_parent)

            protected = is_protected(obj)
                
    except:
        logger.info('Exception raised in protectedURLHandler. '
                    'Debug by enabling the "raise" statement.')
        # raise
    
    # Private items which were attempted to publish directly
    # land in the log file and get "Unauthorized"
    if protected:
        logger.info('PROTECTED: '+str(event.request.URL))
        raise AccessControl.Unauthorized()
    
zope.event.subscribers.append(protectedURLHandler)

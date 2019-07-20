# -*- coding: utf-8 -*-
from decorators import *

def get_month(m):
    dict_months = {
                    1: _('January'), 
                    2: _('Februrary'), 
                    3: _('March'), 
                    4: _('April'), 
                    5: _('May'), 
                    6: _('June'), 
                    7: _('July'), 
                    8: _('August'), 
                    9: _('September'), 
                    10: _('Oktober'), 
                    11: _('November'), 
                    12: _('December')
                    }
    return dict_month[m]

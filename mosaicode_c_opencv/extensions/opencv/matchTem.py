#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the MatchTem class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class MatchTem(Plugin):
    """
    This class contains methods related the MatchTem class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.help = "Operação de filtragem destinada a suavizar uma imagem."
        self.label = "Match Template"
        self.color = "180:180:10:150"
        self.in_ports = [{"type":"mosaicode_c_opencv.extensions.ports.image",
                          "name":"first_image",
                          "label":"First Image"},
                         {"type":"mosaicode_c_opencv.extensions.ports.image",
                          "name":"second_image",
                          "label":"Second Image"}
                         ]
        self.out_ports = [{"type":"mosaicode_c_opencv.extensions.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Feature Detection"

        self.properties = [{"label": "Scale Factor",
                            "name": "scaleFactor",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 99,
                            "step": 1,
                            "value":6
                            },
                           {"label": "Method",
                            "name": "method",
                            "type": MOSAICODE_COMBO,
                            "value":'CV_TM_SQDIFF',
                            "values": ["CV_TM_CCOEFF_NORMED", "CV_TM_CCOEFF",
                                       "CV_TM_CCORR_NORMED", "CV_TM_CCORR",
                                       "CV_TM_SQDIFF_NORMED", "CV_TM_SQDIFF"
                                       ]
                            }
                           ]

        # ------------------------------C/OpenCv code--------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_t0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

        self.codes[2] =  \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            '\tdouble width$id$ = block$id$_img_i0->width - ' + \
            'block$id$_img_i1->width +1;\n' + \
            '\tdouble height$id$ = block$id$_img_i0->height - ' + \
            'block$id$_img_i1->height +1;\n' + \
            '\tCvSize size$id$ = cvSize(width$id$,height$id$);\n' + \
            '\tblock$id$_img_t0 = cvCreateImage(size$id$,32,1);\n' + \
            '\tblock$id$_img_o0 = cvCreateImage(size$id$,8,1);\n' + \
            '\tcvMatchTemplate(block$id$_img_i0 , block$id$_img_i1, ' + \
            'block$id$_img_t0, $method$);\n' + \
            '\tcvConvertScale(block$id$_img_t0, block$id$_img_o0, pow(10,-($scaleFactor$)),0);\n' + \
            '}\n'

        self.codes[3] = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_t0);\n' + \
            'cvReleaseImage(&block$id$_img_i1);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n'
        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------

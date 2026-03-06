"""CSS styles for PDF """

def get_styles(margins):
    """
    Return CSS styles 
    
    Args:
        margins: Dictionary with top, bottom, left, right margins
    
    Returns:
        CSS style string
    """
    return f"""
    <style>
        @page {{ 
            size: letter; 
            margin-top: {margins['top']}in;
            margin-bottom: {margins['bottom']}in;
            margin-left: {margins['left']}in;
            margin-right: {margins['right']}in;

            @frame footer_frame {{
                -pdf-frame-content: footer_content;
                left: {margins['left']}in;
                width: {8.5 - margins['left'] - margins['right']}in;
                top: {12 - margins['bottom'] - 0.5}in;
                height: 0.5in;
            }}
        }}
        body {{ 
            font-family: Helvetica, Arial, sans-serif; 
            font-size: 8pt; 
            line-height: 1.2; 
            color: #000000; 
            margin: 0;
            padding: 0;
        }}
        
        /* Page container for proper footer positioning */
        .page {{
            position: relative;
            min-height: 100vh;
            page-break-inside: avoid;
        }}
        
        /* Footer positioned at bottom right */
        .page-footer {{
            position: absolute;
            bottom: 0;
            right: 0;
            font-size: 6pt;
            color: #666666;
            text-align: right;
            padding: 5px;
        }}
        
        /* Your existing styles below - keep them all */
        /* Baltimore Header Format */
        .office-info {{
            font-size: 8pt;
            margin-bottom: 15px;
            line-height: 1.4;
        }}
        .responsible-party {{
            margin-top: 20px;
            font-size: 8pt;
        }}
        .date {{
            text-align: right;
            font-weight: bold;
            margin: 10px 0 20px 0;
            font-size: 8pt;
        }}
        .service-title {{
            text-align: center;
            font-size: 13pt;
            font-weight: bold;
            margin: 20px 0;
        }}
        .care-recipient {{
            text-align: center;
            font-size: 8pt;
            margin-bottom: 20px;
        }}
        
        /* Baltimore Table Format */
        .admin-grid {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 15px 0; 
            border: 1px solid #000000;
        }}
        .admin-grid th {{ 
            border: 1px solid #000000; 
            background-color: #f2f2f2; 
            font-size: 7pt; 
            padding: 6px; 
            text-align: center;
            font-weight: bold;
        }}
        .admin-grid td {{ 
            border: 1px solid #000000; 
            padding: 8px; 
            text-align: center; 
            font-weight: bold; 
            font-size: 8pt; 
        }}
        
        /* Section Headers - Baltimore uses bold underlined */
        .section-title {{ 
            font-weight: bold; 
            text-decoration: underline; 
            margin: 12px 0 4px 0;
            font-size: 8pt;
        }}
        .legal-text {{ 
            text-align: justify; 
            margin-bottom: 8px;
            font-size: 8pt;
        }}
        
        /* Baltimore Signature Format */
        .signature-table {{ 
            width: 100%; 
            margin-top: 30px; 
            border-collapse: collapse; 
        }}
        .signature-box {{ 
            border-top: 2px solid #000000; 
            text-align: center; 
            font-size: 7pt; 
            padding-top: 4px; 
            margin-top: 4px;
        }}
        
        /* Baltimore Footer with BA and date - KEEP FOR BACKWARD COMPATIBILITY */
        .ba-footer {{
            width: 100%;
            margin-top: 20px;
            font-size: 6pt;
            color: #666666;
        }}
        .ba-left {{
            float: left;
            width: 33.33%;
            text-align: left;
        }}
        .ba-center {{
            float: left;
            width: 33.33%;
            text-align: center;
        }}
        .ba-right {{
            float: left;
            width: 33.33%;
            text-align: right;
        }}
        .clear {{
            clear: both;
        }}
        
        /* Baltimore List Format - FIXED VERSION */
        ol, ul {{ 
            padding-left: 25px; 
            margin-top: 5px; 
            margin-bottom: 10px;
        }}
        li {{ 
            margin-bottom: 4px; 
            text-align: justify; 
            font-size: 8pt;
        }}
        
        /* Main numbered lists */
        ol.main-list {{
            list-style-type: decimal;
            padding-left: 26px;
        }}
        
        /* Alphabetical sub-lists */
        ol.alpha-list {{
            list-style-type: lower-alpha;
            padding-left: 24px;
        }}
        
        /* Roman numeral sub-sub-lists */
        ol.roman-list {{
            list-style-type: lower-roman;
            padding-left: 24px;
        }}
        
        /* Ensure nested lists display properly */
        ol.main-list li,
        ol.alpha-list li,
        ol.roman-list li {{
            margin-bottom: 3px;
        }}
        
        /* Fix for nested list items - important for PDF rendering */
        li > ol {{
            margin-top: 2px;
            margin-bottom: 5px;
        }}
        
        /* Force proper list numbering */
        ol {{
            display: block;
            list-style-position: outside;
        }}
        
        /* Baltimore Nested Lists - Legacy support */
        .nested-list {{
            padding-left: 40px;
            list-style-type: lower-alpha;
        }}
        .double-nested {{
            padding-left: 60px;
            list-style-type: lower-roman;
        }}
        
        /* Baltimore Page Break */
        .page-break {{
            page-break-before: always;
        }}
        
        /* Baltimore Form Fields */
        .form-field {{
            border-bottom: 1px solid #000000;
            min-height: 20px;
            margin: 5px 0;
        }}
        .form-label {{
            font-weight: bold;
            margin-top: 10px;
        }}
        
        /* Baltimore Void Check Box */
        .void-box {{
            border: 2px double #000000;
            padding: 25px;
            text-align: center;
            margin: 20px 0;
            font-weight: bold;
            font-size: 9pt;
        }}
        
        /* Baltimore Checkbox */
        .checkbox {{
            font-family: "Segoe UI Symbol", Arial, sans-serif;
            font-size: 10pt;
        }}
        
        /* Baltimore Indentation */
        .indent {{
            padding-left: 20px;
        }}
        .double-indent {{
            padding-left: 40px;
        }}
        
    </style>
    """
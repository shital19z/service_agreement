"""Footer and header utilities for PDF generation"""

def get_header_tag(branch, care_state, page_num):
    """Get header tag for page (like BA, DC in the example)"""
    if page_num == 2:
        if branch in ['dchomecare', 'dchomecare_staging']:
            return "DC"
        elif branch in ['bahomecare', 'bahomecare_staging']:
            return "BA"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MN"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GB"
        else:
            return branch[:2].upper()
    return ""

def get_footer_tag(branch, care_state, page_num):
    """Get footer tag (like MD 2019-09-16 in the example)"""
    # Page 1 footer
    if page_num == 1:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2019-09-16"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-02"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH 2019-09-16"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH 09-16-2019"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2019-09-16"
        elif branch in ['nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging']:
            return "VA 2019-09-16"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL 2017-06-19"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC 2019-09-16"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC 2020-04-29"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA 2017-06-19"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "IN 2019-09-16"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2019-09-16"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
        elif branch in ['nspahomecare', 'nspahomecare_staging']:
            return "NSPA 2022-01-02"
    
    # Page 2 footer
    elif page_num == 2:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-06-19"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-02"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH 2017-06-19"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH 06-19-2017"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-06-19"
        elif branch in ['nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging']:
            return "VA 2017-06-19"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL 2017-06-19"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA 2019-09-16"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-09-16"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-06-19"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2019-09-12"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA 2020-04-30"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
    
    # Page 3 footer
    elif page_num == 3:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-04-12"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-03"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH - 2016-08-08"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH - 08-08-2016"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-04-12"
        elif branch in ['nvahomecare', 'nvahomecare_staging']:
            return "NVA - 2017-04-12"
        elif branch in ['rihomecare', 'rihomecare_staging']:
            return "RIVA - 2017-04-12"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL - 2017-05-18"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC - 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC - 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA - 2017-04-12"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-04-26"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2020-04-27"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA - 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
    
    elif page_num == 4:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-04-12"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-03"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH - 2016-08-08"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH - 08-08-2016"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-04-12"
        elif branch in ['nvahomecare', 'nvahomecare_staging']:
            return "NVA - 2017-04-12"
        elif branch in ['rihomecare', 'rihomecare_staging']:
            return "RIVA - 2017-04-12"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL - 2017-05-18"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC - 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC - 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA - 2017-04-12"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-04-26"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2020-04-27"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA - 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
        
    elif page_num == 5:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-04-12"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-03"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH - 2016-08-08"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH - 08-08-2016"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-04-12"
        elif branch in ['nvahomecare', 'nvahomecare_staging']:
            return "NVA - 2017-04-12"
        elif branch in ['rihomecare', 'rihomecare_staging']:
            return "RIVA - 2017-04-12"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL - 2017-05-18"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC - 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC - 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA - 2017-04-12"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-04-26"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2020-04-27"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA - 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
    
    return ""
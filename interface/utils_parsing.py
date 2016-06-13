# -*- coding: utf-8 -*-
import re


TODAY = u'((至今)|(目前)|(现在)|今|([Pp]resent)|([Nn]ow))'
CHNUMBERS = u'一二三四五六七八九十'
SP = u'\s '  # [\xa0]
ASP = u'[' + SP + u']'
SEP = u'\-–—―\\\\~～/'
UNIBRALEFT = ur'[（\(\[【]'
UNIBRARIGHT = ur'[）\)\]】]'
DATESEP = u'['+SEP+SP+u'至]+'
DATE = ur'((\d{4}'+ASP+u'?['+SEP+u'\.．年]'+ASP+u'?((\d{1,2}('+ASP+u'?月)?)|(['+CHNUMBERS+u']{1,3}月)))|'+TODAY+')'
PERIOD = u'(?P<from>' + DATE + ur')' + DATESEP + ASP+ u'*(?P<to>' + DATE + ')'
DURATION = ur'(?P<duration>(\d{1,2}'+ASP+u'?年'+ASP+u'?(\d{1,2}'+ASP+u'?个月)?)|(\d{1,2}'+ASP+u'?个月))'
SENTENCESEP = ur'、，。：:\|'
# Exclude date related characters to avoid eating duration
COMPANYTAIL = UNIBRALEFT+u'[^年月（\(\[【]+?'+UNIBRARIGHT
# use re.DOTALL for better results
COMPANY = ur'[^' + SENTENCESEP + '=\n\*]+('+COMPANYTAIL+u')?'
POSITION = ur'[^=\n\*：:\|]+'


fix_today = lambda x: re.compile('^'+TODAY+'$').sub(u'至今', x)
fix_sep = lambda x: re.compile(u'['+SP+SEP+u'\.．年]+').sub('.', x)
fix_trail = lambda x: x.replace(u'月', '').strip()
zero_date = lambda x: str.zfill(str(x.group()), 2)
fix_trailing = lambda x: re.compile(ur'\d+$').sub(zero_date, x)
fix_date = lambda x: fix_trailing(fix_sep(fix_trail(fix_today(x))))

remove_escape = lambda x: x.group(1)
fix_escape = lambda x: re.compile(u'\\\\([_'+SEP+'])').sub(remove_escape, x)
fix_name = lambda x: re.compile(ASP+'+').sub(' ', fix_escape(x)).strip()
fix_duration = lambda x: re.compile(ASP+'+').sub('', x).strip()


WORKXP = PERIOD + ur'[:：\ufffd]?\s*' + UNIBRALEFT + DURATION + UNIBRARIGHT +ASP+ ur'*[：:\| ]*(?P<company>'+COMPANY+u')[：:\| ]*(?P<position>'+POSITION+u'?)((?='+DATE+u')|('+ASP+ ur'*$))'
STUDIES = '\s*'+DATE+' - '+DATE+u'\s*:?\s*(?P<expe>[^\(].+?)(?='+DATE+'|$)'



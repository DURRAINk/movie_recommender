import warnings
import pandas as pd
from taipy.gui import Gui
import func

warnings.filterwarnings('ignore')

df=func.df
title=func.title
year=func.year
val=False
posters=func.posters(df)
cast=list(func.cast)

pay_CBR= pd.DataFrame({'Title':[],'genre':[],'Ratings':[]})
CBR={'genre':'' ,'lang':None, 'data':pay_CBR}

pay_RBR=pd.DataFrame({'Title':[], 'genre':[], "release date":[], 'Rating':[]})
RBR={'title':'', 'year':None, 'data': pay_RBR}

pay_CF=pd.DataFrame({'Title':[], 'Cast':[], 'Rating':[]})
CF={'cast':'', 'data':pay_CF}

page="""
<|part|class_name=screen|
<|part|class_name=header|
<|movie_logo.png|image|id=logo|height=80px|width=120px|>

<|Movie Recommendation System|text|id=heading|>

<nav>
    <ul>
      <li><a href="#">Content-Based</a></li>
      <li><a href="#CBR_table">Rating-Based</a></li>
      <li><a href="#RBR_table">Cast-Filter</a></li>
    </ul>
</nav>

<|True|toggle|theme|>
|>

<|part|class_name=content|
<|part|class_name=RC|
<|Content-Based Recommendation|text|id=CBR|>

<|part|class_name=CBR_selectors|
<|{CBR['genre']}|selector|lov=Action;Adventure;Animation;Comedy;Crime;Documentary;Drama;Family;Fantasy;History;Horror;Movie;Music;Mystery;Romance;Sci-Fi;TV;Thriller;War;Western|dropdown|multiple|height=200px|width=400px|class_name=CBR_genre|label=select genre|on_change=on_change_genre|>

<|{CBR['lang']}|selector|lov={func.lang}|dropdown|on_change=on_change_lang|class_name=CBR_lang|label=select language|>

<|{'recommend'}|button|class_name=CBR_button|on_action=on_action_CBR|>
|>

<|{CBR['data']}|table|auto_loading=False|editable=False|allow_all_rows=True|page_size=10|id=CBR_table|>

<|Rating-Based Recommendation|text|id=RBR|>
<|part|class_name=RBR_selectors|
<|{RBR['title']}|input|label=Eneter Title|on_change=on_change_title|>

<|{RBR['year']}|selector|lov={year}|dropdown|filter|label=Select Year|on_change=on_change_year|>

<|{'recommend'}|button|class_name=RBR_button|on_action=on_action_RBR|>
|>

<|{RBR['data']}|table|auto_loading=False|editable=False|allow_all_rows=True|page_size=10|id=RBR_table|>

<|{'Cast Filter'}|text|id=cast|>

<|part|class_name=cast_selector|
<|{CF['cast']}|input|label=Enter Cast Name|on_change=on_change_cast|change_delay=-1|>

<|{'recommend'}|button|class_name=cast_button|on_action=on_action_CF|>
|>
<|{CF['data']}|table|auto_loading=False|editable=False|allow_all_rows=True|page_size=10|id=CF_table|>
|>
<|part|class_name=posters|

<|{posters[0]}|image|>
<|{posters[1]}|image|>
<|{posters[2]}|image|>


|>
|>
|>

"""


style={
  "color_primary": "#42daf5",
  "color_secondary": "#1C1C1C",
}


def on_action_CBR(state):
  genre= ' '.join(CBR['genre'])
  rec=func.recommend1(df,genre,CBR['lang'])
  state.CBR['data']=rec.sort_values('Ratings',ascending=False)[['Title','genre','Ratings']]
  
def on_change_genre(state,var_name,var_val):
  state.CBR['genre']=var_val
  return

def on_change_lang(state,var_name,var_val):
  state.CBR['lang']= var_val
  return

def on_change_title(state,var_name,var_value):
  state.RBR['title']=var_value
  return

def on_change_year(state,var_name,var_value):
  state.RBR['year']=var_value
  return

def on_action_RBR(state):
  if RBR['year']!=None:
    data=df[df['release_year']==RBR['year']]
  else:
    data=df
  rec=func.recommend2(RBR['title'],data)
  rec=rec.astype('str')
  state.RBR['data']=rec.sort_values('Ratings',ascending=False)[['Title','genre','release','Ratings']]
  
def on_change_cast(state,var_name,var_value):
  name=func.cast_search(var_value)
  state.CF['cast']=name
  return

def on_action_CF(state):
  rec=func.recommender3(CF['cast']).sort_values('Ratings',ascending=False)[['Title','Cast','Ratings']]
  rec=rec.astype('str')
  state.CF['data']=rec


if __name__=='__main__':
  Gui(page=page,css_file='style.css').run(use_reloader=True,stylekit=style,debug=True)
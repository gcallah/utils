" mappings for html editing

" create html skeleton
map g i<html><head><link href="style.css" rel="stylesheet" type="text/css"/><title></title></head><body><h1></h1></body></html>
" details and summary
map > i<details><summary></summary></details>
" break up a line
map \ s
" insert a list item
map  o<li></li>
" create hyperlink
map  o<a href=""></a>3hi
" create a list
map  0o<ul><li></li></ul>
" insert an empty line
map  o
" insert a break
map  0o<br />
" create new paragraph
map  0o<p></p>kO
" create a table
map  0o<table><tr><th></th></tr><tr><td></td></tr></table>
" figure with caption
map  0o<figure>    <img src="">    <figcaption>    </figcaption></figure>
" multiple choice question
map  i<ol><li></li><li><ol type="a"><li></li><li><li></li><li></li></ol></ol>
" headings 1-4:
map <F1> 0o<h1></h1>ki
map <F2> 0o<h2></h2>ki
map <F3> 0o<h3></h3>ki
map <F4> 0o<h4></h4>ki
" an ordered list
map <F6> 0o<ol><li></li></ol>
" centered text
map <F7> o<div style="text-align:center"><p></p></div>
" insert chars at beg. of line
map <F8> j0i    
" delete chars at beg. of line
map <F9> j04x

ab ahr <a href="">
ab blq <blockquote>
ab bl/ </blockquote>
ab emp &empty;
ab ge &ge;
ab gt &gt;
ab inf &infin;
ab le &le;
ab lt &lt;
ab nb &nbsp;
ab ne &ne;
ab omega &omega;
ab sigma &sigma;
ab sq &radic;
ab sup2 <sup>2</sup>
ab sup3 <sup>3</sup>
ab sube &sube;
ab subs &sub;
ab theta &theta;
ab uni &cup;

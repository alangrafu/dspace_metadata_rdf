<div id="ds-options">
<h3 class="ds-option-set-head" id="ds-search-option-head">Search Repository</h3>
<div class="ds-option-set" id="ds-search-option">
<fieldset>
<input type="text" class="ds-text-field " id="query" name="query" value="" />
<input value="Go" id="searchButton" type="submit" name="submit" class="ds-button-field" />
</fieldset>
</div>
<h3 class="ds-option-set-head">Browse</h3>
<div id="aspect_artifactbrowser_Navigation_list_browse" class="ds-option-set">
 <ul class="ds-options-list">
  <li>
   <h4 class="ds-sublist-head">All of Repository</h4>
   <ul class="ds-simple-list">
    <li>
     <a href="{{lodspk.home}}contributors" class="">All contributors</a>
    </li>
   </ul>
  </li>
  <li>
   <h4 class="ds-sublist-head">Linked Data</h4>
   <ul class="ds-simple-list">
    <li>
     <a href="{{lodspk.home}}linkeddata" class="">What is Linked Data?</a>
    </li>
   </ul>
  </li>
  <li>
   <h4 class="ds-sublist-head">Other resources</h4>
   <ul class="ds-simple-list">
    <li>
     <a href="http://tw.rpi.edu" class="">Tetherless World Constellation</a>
    </li>
    <li>
     <a href="http://logd.tw.rpi.edu" class="">Linking Open Government Data</a>
    </li>
   </ul>
  </li>
 </ul>
</div>
</div>
<script type="text/javascript">
function changeSearchUrl(ev){
var action = "{{lodspk.home}}search/"+document.getElementById("query").value;
console.log(action);
window.location=action;
ev.stopPropagation();
}
elem = document.getElementById("searchButton");
elem.addEventListener("click", changeSearchUrl, false);
</script>
</body>
</html>

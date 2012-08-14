<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
<meta name="Generator" content="DSpace 1.7.2" />
<link type="text/css" rel="stylesheet" media="screen" href="/projects/dataservices/repository/themes/Reference/lib/style.css" />
<script type="text/javascript">
                                //Clear default text of emty text areas on focus
                                function tFocus(element)
                                {
                                        if (element.value == ' '){element.value='';}
                                }
                                //Clear default text of emty text areas on submit
                                function tSubmit(form)
                                {
                                        var defaultedElements = document.getElementsByTagName("textarea");
                                        for (var i=0; i != defaultedElements.length; i++){
                                                if (defaultedElements[i].value == ' '){
                                                        defaultedElements[i].value='';}}
                                }
                                //Disable pressing 'enter' key to submit a form (otherwise pressing 'enter' causes a submission to start over)
                                function disableEnterKey(e)
                                {
                                     var key;
                                
                                     if(window.event)
                                          key = window.event.keyCode;     //Internet Explorer
                                     else
                                          key = e.which;     //Firefox and Netscape
                                
                                     if(key == 13)  //if "Enter" pressed, then disable!
                                          return false;
                                     else
                                          return true;
                                }
            </script>
<title>Repository Home</title>
</head>
<body>
<div id="ds-main">
<div id="ds-header">
<a href="{{lodspk.home}}">
<span id="ds-header-logo"> </span>
</a>
<h1 class="pagetitle">Repository Home</h1>
<h2 class="static-pagetitle">Repository/Manakin Repository</h2>
<ul id="ds-trail">
<li class="ds-trail-link first-link last-link">
<a href="{{lodspk.home}}">Data.Rpi.Edu</a>
</li>
</ul>
</div>

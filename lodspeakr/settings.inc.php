<?

$conf['endpoint']['local'] = 'http://dydra.com/agraves/datarpi/sparql';
$conf['endpoint']['local'] = 'http://localhost:3030/rpi/query';
$conf['home'] = '/var/www/html/lodspeakr/';
$conf['basedir'] = 'http://aquarius.tw.rpi.edu/projects/dataservices/';
$conf['debug'] = false;

/*ATTENTION: By default this application is available to
 * be exported and copied (its configuration)
 * by others. If you do not want that, 
 * turn the next option as false
 */ 
$conf['export'] = true;

#If you want to add/overrid a namespace, add it here
$conf['ns']['local']   = 'http://data.rpi.edu/';
$conf['ns']['base']   = 'http://graves.cl/data.rpi.edu/';

$conf['mirror_external_uris'] = $conf['ns']['local'];

$conf['disableComponents'] = false;
$conf['root'] = 'home';
?>

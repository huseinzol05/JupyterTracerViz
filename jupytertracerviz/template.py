base = """
<!DOCTYPE html>
<!--
Copyright (c) 2014 The Chromium Authors. All rights reserved.
Use of this source code is governed by a BSD-style license that can be
found in the LICENSE file.
Original LICENSE file: 
https://github.com/catapult-project/catapult/blob/master/tracing/LICENSE
-->
<head>
<!-- WebComponent V0 polyfill. You may want to host this in a more suitable
     place. See https://crbug.com/1036492 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/0.7.24/webcomponents.min.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/components/prism-core.min.js" integrity="sha512-hqRrGU7ys5tkcqxx5FIZTBb7PkO2o3mU6U5+qB9b55kgMlBUT4J2wPwQfMCxeJW1fC8pBxuatxoH//z0FInhrA==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/components/prism-python.min.js" integrity="sha512-EXseTM1JV8e3AonU5PfOUmzbPkUTRm4c4hVxv206gVeWZE/FwzSQBNWrUBaHsN3Idq9k76BEjUlXpluX1UFx6Q==" crossorigin="anonymous"></script>
<script>
'use strict';

function onTraceViewerImportFail() {
  document.addEventListener('DOMContentLoaded', function() {
    document.body.textContent =
        'tracing/bin/trace_viewer_full.html is missing. ' +
        'Run vulcanize_trace_viewer from $$TRACE_VIEWER and reload.';
  });
}
</script>
<!-- <link rel="import" href="trace_viewer_full.html"
      onerror="onTraceViewerImportFail(event)"> -->

$trace_viewer_full


<style>
  html, body {
    box-sizing: border-box;
    overflow: hidden;
    margin: 0px;
    padding: 0;
    width: 100%;
    height: 100%;
  }
  #trace-viewer {
    width: 100%;
    height: 100%;
  }
  #trace-viewer:focus {
    outline: none;
  }
  #right-part {
    display: none;
  }
</style>
<script>
'use strict';

var json_data;
(function() {
  let viewer;
  let url;
  let model;

  // You can set this to true if you want to hide the WebComponentsV0 polyfill
  // warning.
  window.__hideTraceViewerPolyfillWarning = true;
  json_data = $json_data

  function load() {
    const req = new XMLHttpRequest();
    const isBinary = /[.]gz$$/.test(url) || /[.]zip$$/.test(url);
    req.overrideMimeType('text/plain; charset=x-user-defined');
    req.open('GET', url, true);
    if (isBinary) req.responseType = 'arraybuffer';

    req.onreadystatechange = function(event) {
      if (req.readyState !== 4) return;

      window.setTimeout(function() {
        if (req.status === 200) {
          onResult(isBinary ? req.response : req.responseText);
        } else {
          onResultFail(req.status);
        }
      }, 0);
    };
    req.send(null);
  }

  function onResultFail(err) {
    const overlay = new tr.ui.b.Overlay();
    overlay.textContent = err + ': ' + url + ' could not be loaded';
    overlay.title = 'Failed to fetch data';
    overlay.visible = true;
  }

  function onResult(result) {
    model = new tr.Model();
    const i = new tr.importer.Import(model);
    const p = i.importTracesWithProgressDialog([result]);
    p.then(onModelLoaded, onImportFail);
  }

  function onModelLoaded() {
    viewer.model = model;
    viewer.viewTitle = url;
  }

  function onImportFail(err) {
    const overlay = new tr.ui.b.Overlay();
    overlay.textContent = tr.b.normalizeException(err).message;
    overlay.title = 'Import error';
    overlay.visible = true;
  }

  document.addEventListener('WebComponentsReady', function() {
    const container = document.createElement('track-view-container');
    container.id = 'track_view_container';

    viewer = document.createElement('tr-ui-timeline-view');
    viewer.track_view_container = container;
    Polymer.dom(viewer).appendChild(container);

    viewer.id = 'trace-viewer';
    viewer.globalMode = true;
    Polymer.dom(document.body).appendChild(viewer);

    //url = '../test_data/big_trace.json';
    //load();
    model = new tr.Model();
    const i = new tr.importer.Import(model);
    const p = i.importTracesWithProgressDialog([json_data]);
    p.then(onModelLoaded, onImportFail);
  });

}());

</script>
</head>
<body>
</body>
</html>
"""

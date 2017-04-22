jQuery.noConflict();

function gdToJson(gd) {
    var res = {};
    var geo = gd.shapes[0].geometry;
    for (var prop in geo) {
        res[prop] = geo[prop];
    }
    res.class = gd.text;
    return res;
}
function jsonToXml(json) {
    var doc = jQuery.parseXML("<xml/>")
    var xml = doc.getElementsByTagName("xml")[0]
    var key, elem

    for (key in json) {
        if (json.hasOwnProperty(key)) {
            elem = doc.createElement(key)
            jQuery(elem).text(json[key])
            xml.appendChild(elem)
        }
    }

    console.log(xml.outerHTML)
}
jQuery(document).ready(function ($) {
    function onSave () {
        $('#result').empty();
        var annos = anno.getAnnotations();
        for (var i=0; i<annos.length; i++) {
            var res = gdToJson(annos[i]);
            $('<p>').text(JSON.stringify(res)).appendTo($('#result'));
            jsonToXml(res);
        }
    }
    $('#save_btn').on('click', onSave);

    $(document).on('mouseup', function () {
        $('.annotorious-editor-text').val($("input:radio[name=label]:checked").val());
    });

    $(document).keypress(function(e){
        
        if (e.keyCode == 49) {
            // onPress button 1
            $('input:radio[name=label][value=person]').attr('checked', false);
            $('input:radio[name=label][value=car]').attr('checked', true);
        } else if (e.keyCode == 50) {
            // onPress button 2
            $('input:radio[name=label][value=car]').attr('checked', false);
            $('input:radio[name=label][value=person]').attr('checked', true);
        } else if (e.keyCode == 51) {
            // onPress button 3
            onSave();
        }
    });
});

jQuery.noConflict();

function gdToObject(gd) {
    var res = {};
    var geo = gd.shapes[0].geometry;
    for (var prop in geo) {
        res[prop] = geo[prop];
    }
    res.class = gd.text;
    return res;
}

function jsonToXmlString(json) {
    var xml = "";
    for (var key in json) {
        if (!json.hasOwnProperty(key))
            continue;
        xml += "<" + key + ">";
        if (typeof json[key] == "object")
            xml += jsonToXmlString(new Object(json[key]));
        else
            xml += json[key];
        xml += "</" + key + ">";
    }
    return xml;
}

function jsonToXml (json) {
    var doc = jQuery.parseXML("<annotation>" + jsonToXmlString(json) + "</annotation>");
    var xml = doc.getElementsByTagName("annotation")[0];
    return xml;
}


jQuery(document).ready(function ($) {

    function onSave () {
        $('#result').empty();
        var annos = anno.getAnnotations();
        var body = {};
        body['filename'] = '00001.jpg';
        body['object'] = [];
        for (var i=0; i<annos.length; i++) {
            var res = gdToObject(annos[i]);
            console.log("res from json", res)
            $('<p>').text(JSON.stringify(res)).appendTo($('#result'));
            body['object'].push(res)
        }
        retXml = jsonToXml(body);
        console.log("retXml", retXml)
    }

    function onReset(){
        $('#result').empty();
        $('<p>').text('Clear...').appendTo($('#result'));
    }

    $('#save_btn').on('click', onSave);
    $('#rest_btn').on('click', onReset);

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
        } else if (E.keyCode == 52){
            // onPress button 4
            onReset();
        }
    });
});

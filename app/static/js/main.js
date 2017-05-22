$.noConflict();

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
        if (Array.isArray(json[key])) {
            for (var i=0; i<json[key].length; i++) {
                xml += "<" + key + ">";
                xml += jsonToXmlString(json[key][i]);
                xml += "</" + key + ">";
            }
            return xml;
        }

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
        window.body = {}; // This body would be sented to Sever 
        body['filename'] = '00001.jpg';
        body['object'] = [];
        for (var i=0; i<annos.length; i++) {
            var res = gdToObject(annos[i]);
            console.log("res from json", res)
            $('<p>').text(JSON.stringify(res)).appendTo($('#result'));
            body['object'].push(res)
        }
        retXml = jsonToXml(body);
        console.log("retXml", retXml);
        body['xml_data'] = retXml;
    }

    function onReSet(){
        $('#result').empty();
        $('<p>').text('Clear...').appendTo($('#result'));
    }

    function onNext(){
        console.log('this is onNext..');
        $.post('http://127.0.0.1:5000/next_image', 
        {
            key1:"value1",
            key2:"value2"
        }, function(data, status){
            // new image url example : http://127.0.0.1:5000/static/datacenter/images/dog.jpg
            console.log("data from post : ", data);
            console.log("status from post : ", status);
        });
        // $.get("http://127.0.0.1:5000/next_image", function(data, status){
        //     console.log("data from server : ", data)
        //     console.log('status from server : ', status)
        // });
    }

    $('#save_btn').on('click', onSave);
    $('#reset_btn').on('click', onReSet);
    $('#next_btn').on('click', onNext);
    
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
            onReSet();
        }
    });
});

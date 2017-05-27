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
    console.log(json);
    for (var key in json) {
        if (!json.hasOwnProperty(key))
            continue;
        if (Array.isArray(json[key])) {
            for (var i = 0; i < json[key].length; i++) {
                xml += "<" + key + ">";
                xml += jsonToXmlString(json[key][i]);
                xml += "</" + key + ">";
            }
        } else {
            xml += "<" + key + ">";
            if (typeof json[key] == "object")
                xml += jsonToXmlString(new Object(json[key]));
            else
                xml += json[key];
            xml += "</" + key + ">"; 
        }
    }
    console.log(xml);
    return xml;
}


function jsonToXml(json) {
    console.log(json);
    var doc = jQuery.parseXML("<annotation>" + jsonToXmlString(json) + "</annotation>");
    var xml = doc.getElementsByTagName("annotation")[0];
    return xml;
}



jQuery(document).ready(function ($) {
    var imgDir = "/static/datacenter/images/";
    window.body = {};

    function setAnnotations(g, filename) {
        var ad = new Ad("rect",g);
        window.an = new Gd(imgDir + filename,'',ad);
        anno.addAnnotation(an);
    }

    function getObjectsFromXmlString (xmlStr) {
        var objectTags = $(xmlStr)[0].getElementsByTagName('object');
        var objs = [];
        var copyKeys = ['xmin', 'xmax', 'ymin', 'ymax'];
        for (var i=0; i<objectTags.length; i++) {
            var obj = {};
            for (var j=0; j<copyKeys.length; j++) {
                obj[copyKeys[j]] = parseFloat(objectTags[i].getElementsByTagName(copyKeys[j])[0].innerText);
            }
            obj.name = objectTags[i].getElementsByTagName('name')[0].innerText;
            objs.push(obj);
        }
        return objs;
    }

    function setImage (data) {
        body['filename'] = data.new_file_name;
        body['xml'] = data.new_xml_data;
        console.log(data.new_xml_data);
        $("#target_image").attr("src",imgDir + body.filename);
        $('#status').empty();
        $('<p>').text("Total Image Number : " + data.total_image_number).appendTo($('#status'));
        $('<p>').text("Current Image Number : "+data.current_image_number).appendTo($('#status'));
    }

    $.get('/start_labeling', setImage);

    function onSave() {
        $('#result').empty();
        var annos = anno.getAnnotations();
        
        body['object'] = [];
        // set image size
        var width = $('#target_image').width(), height = $('#target_image').height();
        $('<p>').text("width:"+width+", height:"+height).appendTo($('#result'));
        body['size'] = {"width":width, "height":height, "depth":3};
        
        for (var i = 0; i < annos.length; i++) {
            var res = gdToObject(annos[i]);
            var xmin = res.x*width;
            var ymin = res.y*height;
            var xmax = xmin + res.width*width;
            var ymax = ymin + res.height*height;
            console.log("res from json", res)
            $('<p>').text(JSON.stringify({"xmin":xmin, "ymin":ymin, "xmax":xmax, "ymax":ymax, "name":res.class})).appendTo($('#result'));
            body['object'].push({"name":res.class, "xmin":xmin, "ymin":ymin, "xmax":xmax, "ymax":ymax});
        }
        
        retXml = jsonToXml(body);
        console.log("retXml", retXml);
        body['xml_data'] = retXml;

        onNext();
    }

    function onReSet() {
        $('#result').empty();
        $('<p>').text('Clear...').appendTo($('#result'));
        anno.reset();
    }

    // add image load event
    $('#target_image').on('load', function () {
        onReSet();
        if (body.xml) {
            var width = $('#target_image').width(), height = $('#target_image').height();
            var objs = getObjectsFromXmlString(body.xml);
            console.log(objs);
            for (var i=0; i<objs.length; i++) {
                var objWidth = objs[i].xmax - objs[i].xmin;
                var objHeight = objs[i].ymax - objs[i].ymin;
                var g = {x:objs[i].xmin/width, y:objs[i].ymin/height, width:objWidth/width, height:objHeight/height};
                setAnnotations(g, body['filename']);
            }
        }
        delete body.xml;
    });

    function onNext() {
        console.log('this is onNext..');
        console.log("body", body)
        $.post('/next_image',
            {
                file_name: body.filename,
                xml_data: vkbeautify.xml(body.xml_data.outerHTML)
            }, setImage);
    }

    function onSkip(){
        console.log('this is onSkip...');
        $.post('/skip_image',
        {
            file_name: body.filename,

        }, setImage);
    }

    $('#save_btn').on('click', onSave);
    $('#reset_btn').on('click', onReSet);
    $('#skip_btn').on('click', onSkip);

    $(document).on('mouseup', function () {
        $('.annotorious-editor-text').val($("input:radio[name=label]:checked").val());
    });

    $(document).keypress(function (e) {

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
        } else if (E.keyCode == 52) {
            // onPress button 4
            onReSet();
        }
    });
});

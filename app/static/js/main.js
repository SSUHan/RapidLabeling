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

function _(el) {
    return document.getElementById(el);
}

jQuery(document).ready(function ($) {
    var imgDir = "/static/datacenter/images/";
    window.params = {};
    var width = 448, height = 448;


    function setAnnotations(g, filename, name) {
        var ad = new Ad("rect", g);
        var an = new Gd(imgDir + filename, name, ad);
        anno.addAnnotation(an);
    };

    function getObjectsFromXmlString(xmlStr) {
        var objectTags = $(xmlStr)[0].getElementsByTagName('object');
        var objs = [];
        var copyKeys = ['xmin', 'xmax', 'ymin', 'ymax'];
        for (var i = 0; i < objectTags.length; i++) {
            var obj = {};
            for (var j = 0; j < copyKeys.length; j++) {
                obj[copyKeys[j]] = parseFloat(objectTags[i].getElementsByTagName(copyKeys[j])[0].innerText);
            }
            obj.name = objectTags[i].getElementsByTagName('name')[0].innerText;
            objs.push(obj);
        }
        return objs;
    }

    function setImage(data) {
        params['filename'] = data.new_file_name;
        params['xml'] = data.new_xml_data;
        console.log(data.new_xml_data);
        $("#target_image").attr("src", imgDir + params.filename);
        $('#status').empty();
        $('<p>').text("Total Image Number : " + data.total_image_number).appendTo($('#status'));
        $('<p>').text("Current Image Number : " + data.current_image_number).appendTo($('#status'));
    }

    function onSave() {
        $('#result').empty();
        var annos = anno.getAnnotations();
        params['object'] = [];
        params['owner'] = {name: $('#login-username').get(0).value};
        // set image size
        $('<p>').text("width:" + width + ", height:" + height).appendTo($('#result'));
        params['size'] = {"width": width, "height": height, "depth": 3};

        for (var i = 0; i < annos.length; i++) {
            var res = gdToObject(annos[i]);
            var xmin = res.x * width;
            var ymin = res.y * height;
            var xmax = xmin + res.width * width;
            var ymax = ymin + res.height * height;
            console.log("res from json", res)
            $('<p>').text(JSON.stringify({
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax,
                "name": res.class
            })).appendTo($('#result'));
            params['object'].push({"name": res.class, "xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax});
        }

        retXml = jsonToXml(params);
        console.log("retXml", retXml);
        params['xml_data'] = retXml;

        onNext();
    }

    function onReSet() {
        $('#result').empty();
        $('<p>').text('Clear...').appendTo($('#result'));
        anno.reset();
    }


    function onBack() {
        console.log('this is onBack...');
        window.params = {};
        $.get('/back_image', setImage);
    }

    // add image load event
    $('#target_image').on('load', function () {
        width = $('#target_image').get(0).naturalWidth;
        height = $('#target_image').get(0).naturalHeight;
        onReSet();
        if (params.xml) {
            var objs = getObjectsFromXmlString(params.xml);
            console.log(objs);
            for (var i = 0; i < objs.length; i++) {
                var objWidth = objs[i].xmax - objs[i].xmin;
                var objHeight = objs[i].ymax - objs[i].ymin;
                var g = {
                    x: objs[i].xmin / width,
                    y: objs[i].ymin / height,
                    width: objWidth / width,
                    height: objHeight / height
                };
                setAnnotations(g, params['filename'], objs[i].name);
            }
            window.objs = objs;
        }
        delete params.xml;
    });

    function onNext() {
        console.log('this is onNext..');
        console.log("params", params)
        $.post('/next_image',
            {
                file_name: params.filename,
                xml_data: vkbeautify.xml(params.xml_data.outerHTML)
            }, setImage);
    }

    function onSkip() {
        console.log('this is onSkip...');
        $.post('/skip_image',
            {
                file_name: params.filename,

            }, setImage);
    }

    $('#back_btn').on('click', onBack);
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
        } else if (e.keyCode == 81) {
            // onPress button q
            onBack();
        } else if (e.keyCode == 87) {
            // onPress button w
            onSave();
        } else if (e.keyCode == 69) {
            // onPress button e
            onSkip();
        }
    });

    // set file uploader
    function progressHandler(event) {
        _("loaded_n_total").innerHTML = "Uploaded " + event.loaded + " bytes of " + event.total;
        var percent = (event.loaded / event.total) * 100;
        _("progressBar").value = Math.round(percent);
        _("file_status").innerHTML = Math.round(percent) + "% uploaded... please wait";
    }

    function completeHandler(event) {
        var res = JSON.parse(event.target.responseText);
        _("file_status").innerHTML = "Done. Token of your video is '" + res.new_hashid + "'";
        _("token").value = res.new_hashid;
        _("progressBar").value = 0;
    }

    function errorHandler(event) {
        _("file_status").innerHTML = "Upload Failed";
    }

    function abortHandler(event) {
        _("file_status").innerHTML = "Upload Aborted";
    }

    uploadFile = function () {
        var file = _("video_file").files[0];
        if (typeof file === "undefined") {
            _("file_status").innerHTML = "ERROR: Please browse for a file before clicking the upload button";
            _("progressBar").value = 0;
            return;
        }

        if (file.type !== "video/mp4" && file.type !== 'video/avi') {
            var typewarn = "ERROR: You have to select a MP4 or AVI File";
            _("file_status").innerHTML = typewarn;
            _("progressBar").value = 0;
            return;
        }

        var sizelimit = 100*1024*1024;
        if (sizelimit < file.size) {
            var sizewarn = "ERROR: The File is too big! The maximum file size is ";
            sizewarn += sizelimit / (1024 * 1024);
            sizewarn += "MB";
            _("file_status").innerHTML = sizewarn;
            _("progressBar").value = 0;
            return;
        }

        var formdata = new FormData();
        formdata.append("file", file);
        formdata.append("size", file.size);
        var ajax = new XMLHttpRequest();
        ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);
        ajax.open("POST", "/make_dir");
        ajax.send(formdata);
    };


    $.get('/start_labeling', setImage);
});

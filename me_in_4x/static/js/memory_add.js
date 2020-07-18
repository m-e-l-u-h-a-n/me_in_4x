var inputs = document.querySelectorAll('.box__file');
var filearr = []; //final list of valid files that will be added to memory.
var allFiles = []; //list of all files that are sent to server.
Array.prototype.forEach.call(inputs, function(input) {
    var label = input.nextElementSibling,
        labelVal = label.innerHTML;

    input.addEventListener('change', function(e) {

        var fileName = '';
        allFiles = this.files;
        console.log(allFiles);
        if (this.files && this.files.length > 1)
            fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
        else
            fileName = e.target.value.split('\\').pop();

        if (fileName)
            label.querySelector('span').innerHTML = fileName;
        else
            label.innerHTML = labelVal;
    });
});

var isAdvancedUpload = function() {
    var div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}();

var $form = $('.box');
var $memory_form = $('.memory-form');
var $input = $('.box__file')
if (isAdvancedUpload) {
    $form.addClass('has-advanced-upload');

    var droppedFiles = false;

    $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
        })
        .on('dragover dragenter', function() {
            $form.addClass('is-dragover');
        })
        .on('dragleave dragend drop', function() {
            $form.removeClass('is-dragover');
        })
        .on('drop', function(e) {
            droppedFiles = e.originalEvent.dataTransfer.files;
        })
}
$form.on('submit', function(e) {
    if ($form.hasClass('is-uploading')) return false;

    $form.addClass('is-uploading').removeClass('is-error');

    if (isAdvancedUpload) {
        e.preventDefault();

        var ajaxData = new FormData($form.get(0));
        if (droppedFiles) {
            $.each(droppedFiles, function(i, file) {
                ajaxData.append($input.attr('name'), file);
                allFiles.push(file);
            });
        }
        console.log($input.files);
        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: ajaxData,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            complete: function() {
                $form.removeClass('is-uploading');
            },
            success: function(data, status, xhr) {
                $form.addClass(data.success == true ? 'is-success' : 'is-error');
                if (!data.success) $errorMsg.text(data.error);
                if (data.success) {
                    if (data.invalid_files.length > 0) {
                        let newdiv, newli;
                        let info_list = document.getElementById("info-list");
                        for (let i = 0; i < data.invalid_files.length; i++) {
                            newdiv = document.createElement('div')
                            newdiv.className += 'col-7';
                            newdiv.className += 'text-muted';
                            newdiv.innerHTML = "File " + data.invalid_files[i] + " is not supprted!";
                            newli = document.createElement('li')
                            newli.appendChild(newdiv);
                            info_list.appendChild(newli);
                        }
                        iziToast.error({
                            title: "Error",
                            color: 'red',
                            message: data.message,
                            position: "bottomRight",
                        });
                    } else {
                        iziToast.success({
                            title: "Success",
                            message: data.message,
                            position: "bottomRight",
                        });
                    }
                    for (let i = 0; i < allFiles.length; i++) {
                        for (let j = 0; j < data.valid_files.length; j++) {
                            if (allFiles[i].name == data.valid_files[j]) {
                                filearr.push(allFiles[i]);
                                break;
                            }
                        }
                    }
                    console.log(filearr);
                    if (filearr.length > 0) {
                        msg = String()
                        for (let i = 0; i < filearr.length - 1; i++) {
                            msg += (filearr[i].name + ", ");
                        }
                        msg += filearr[filearr.length - 1].name
                        document.getElementById('added-files-info').innerHTML = msg + "<strong> will be added to your memory on pressing save changes</strong>";
                    }
                } else {
                    iziToast.error({
                        title: "Error",
                        color: "red",
                        message: data.message,
                        position: "bottomRight",
                    });
                }
            },
            error: function(xhr, status, err) {
                iziToast.info({
                    title: "Error",
                    color: "red",
                    message: "Facing server issues, contact site admin if problem persists",
                    position: "bottomRight",
                })
            }
        });
    } else {
        // ajax for legacy browsers that do not support 'drag n drop'
        var iframeName = 'uploadiframe' + new Date().getTime();
        $iframe = $('<iframe name="' + iframeName + '" style="display: none;"></iframe>');

        $('body').append($iframe);
        $form.attr('target', iframeName);

        $iframe.one('load', function() {
            var data = JSON.parse($iframe.contents().find('body').text());
            $form
                .removeClass('is-uploading')
                .addClass(data.success == true ? 'is-success' : 'is-error')
                .removeAttr('target');
            if (!data.success) $errorMsg.text(data.error);
            $form.removeAttr('target');
            $iframe.remove();
        });
    }
});
$memory_form.on('submit', function(e) {
    e.preventDefault();
    console.log('hello');
    console.log("filearr = ", filearr);
    var orgdata = new FormData($memory_form.get(0)); //ajax data for original memory addition form
    $.each(filearr, function(i, file) {
        orgdata.append("files", file);
    });
    $.ajax({
        url: $memory_form.attr('action'),
        type: $memory_form.attr('method'),
        data: orgdata,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        success: function(data, status, xhr) {
            if (data.success) {
                iziToast.success({
                    position: "center",
                    message: data.message,
                    timeout: 5000,
                    transitionIn: 'bounceInDown',
                    // onClosing: function(instance, toast) {
                    //     window.location.replace("{% url 'home' %}");
                    // },
                });
            }
        },
        error: function(xhr, status, err) {
            iziToast.error({
                psoition: "bottomRight",
                message: "Internal server error!",
                color: "red"
            });
        },
    });
});
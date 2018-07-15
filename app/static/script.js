$(document).ready(function () {
  //Resetting the UI from cached values and fetching the current upload-rights
  $('#ToggleForm')[0].reset();
  $('#UploadForm > form')[0].reset();
  $('#YoutubeForm > form')[0].reset();
  checkUploadingAccess();

  //Starting the playlist loop
  loadPlaylist();

  $('#UploadForm > form > button').click(function () {
    var fd = $("input[type='file']").prop("files")[0];
    var form_data = new FormData();
    form_data.append('file', fd);
    $('#UploadForm > form > button').prop('disabled', true);
    $('input[type="file"]').prop('disabled', true);
    $.ajax({
      xhr: function () {
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener("progress", function (evt) {
          if (evt.lengthComputable) {
            var percentComplete = Math.round((evt.loaded / evt.total) * 100);
            $("#UploadForm > form > progress").show();
            $("#UploadForm > form > progress")[0].value = percentComplete;
          }
        }, false);
        return xhr;
      },
      url: '/upload',
      type: 'POST',
      dataType: 'text',
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      success: function (response) {
        var alert_data = $.parseJSON(response);
        if (alert_data.upload == false) {
          alert(alert_data.reason);
        } else {
          $("#UploadForm > form")[0].reset()
        };
      },
      error: function (response, xhr, status, e) {
        alert('Upload error: ' + status);
      },
      complete: function () {
        $('#UploadForm > form > button').prop('disabled', false);
        $('input[type="file"]').prop('disabled', false);
        $("#UploadForm > form > progress").hide();
        $("#UploadForm > form > progress")[0].value = "0";
        checkUploadingAccess();
      }
    });
  });

  $('#YoutubeForm > form > button').click(function () {
    $('#YoutubeForm > form > button').prop('disabled', true);
    $('#YoutubeForm > form')[0].link.disabled = true;
    var form_data = JSON.stringify({
      link: $('#YoutubeForm > form')[0].link.value
    });
    $.ajax({
      xhr: function () {
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener("progress", function (evt) {
          if (evt.lengthComputable) {
            var percentComplete = Math.round((evt.loaded / evt.total) * 100);
            $("#YoutubeForm > form > progress").show();
            $("#YoutubeForm > form > progress")[0].value = percentComplete;
          }
        }, false);
        return xhr;
      },
      url: '/youtube',
      type: 'POST',
      dataType: 'text',
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      success: function (response) {
        var alert_data = $.parseJSON(response);
        if (alert_data.upload == false) {
          alert(alert_data.reason);
        } else {
          $("#YoutubeForm > form")[0].reset()
        };
      },
      error: function (response, xhr, status, e) {
        alert('Upload error: ' + status);
      },
      complete: function () {
        $('#YoutubeForm > form > button').prop('disabled', false);
        $('#YoutubeForm > form')[0].link.disabled = false;
        $("#YoutubeForm > form > progress").hide();
        $("#YoutubeForm > form > progress")[0].value = "0";
        checkUploadingAccess();
      }
    });
  });

  $('#ToggleForm').change(function (event) {
    switch (event.target.value) {
      case 'youtube':
        $('#UploadForm').hide();
        $('#YoutubeForm').show();
        break;
      default:
        $('#UploadForm').show();
        $('#YoutubeForm').hide();
    }
  });
});

function loadPlaylist() {
  $.get('/playlist', function (data, status) {
    $('#Playlist').children().remove();
    var len = data.length;
    while (len--) {
      $('<li>', {
        text: data[len]
      }).appendTo('#Playlist');
    }
    $('#Playlist > li').after('<hr/>');
    setTimeout(loadPlaylist, 15000);
  });
}

function checkUploadingAccess() {
  var access = true;
  var checking = function () {
    $.get('/allowed', function (data, status) {
      if (data.upload_allowed == access) {
        if (access) {
          return;
        } else {
          setTimeout(checking, 10000);
        }
      } else {
        if (access) {
          $('#UploadForm > form > button').prop('disabled', true);
          $('#YoutubeForm > form > button').prop('disabled', true);
          $('#UploadWarning').css("visibility", "visible");
          access = !access;
          setTimeout(checking, 10000);
        } else {
          $('#UploadForm > form > button').prop('disabled', false);
          $('#YoutubeForm > form > button').prop('disabled', false);
          $('#UploadWarning').css("visibility", "hidden");
        }
      }
    });
  };
  checking();
}
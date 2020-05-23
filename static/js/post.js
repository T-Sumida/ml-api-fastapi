// 画像をリサイズして、HTMLで表示する
$(function () {
  var file = null;
  var blob = null;
  const RESIZED_WIDTH = 300;
  const RESIZED_HEIGHT = 300;

  $("input[type=file]").change(function () {
    file = $(this).prop("files")[0];

    // ファイルチェック
    if (file.type != "image/jpeg" && file.type != "image/png") {
      file = null;
      blob = null;
      return;
    }

    var result = document.getElementById("result");
    result.innerHTML = "";

    // 画像をリサイズする
    var image = new Image();
    var reader = new FileReader();
    reader.onload = function (e) {
      image.onload = function () {
        var width, height;

        // 縦or横の長い方に合わせてリサイズする
        if (image.width > image.height) {
          var ratio = image.height / image.width;
          width = RESIZED_WIDTH;
          height = RESIZED_WIDTH * ratio;
        } else {
          var ratio = image.width / image.height;
          width = RESIZED_HEIGHT * ratio;
          height = RESIZED_HEIGHT;
        }

        var canvas = $("#canvas").attr("width", width).attr("height", height);
        var ctx = canvas[0].getContext("2d");
        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(
          image,
          0,
          0,
          image.width,
          image.height,
          0,
          0,
          width,
          height
        );

        // canvasからbase64画像データを取得し、POST用のBlobを作成する
        var base64 = canvas.get(0).toDataURL("image/jpeg");
        var barr, bin, i, len;
        bin = atob(base64.split("base64,")[1]);
        len = bin.length;
        barr = new Uint8Array(len);
        i = 0;
        while (i < len) {
          barr[i] = bin.charCodeAt(i);
          i++;
        }
        blob = new Blob([barr], { type: "image/jpeg" });
        console.log(blob);
      };
      image.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });

  // アップロード開始ボタンがクリックされたら
  $("#post").click(function () {
    if (!file || !blob) {
      return;
    }

    var name,
      fd = new FormData();
    fd.append("files", blob);

    // API宛にPOSTする
    $.ajax({
      url: "/api/image_recognition",
      type: "POST",
      dataType: "json",
      data: fd,
      processData: false,
      contentType: false,
    })
      .done(function (data, textStatus, jqXHR) {
          // 通信が成功した場合、結果を出力する
        var response = JSON.stringify(data);
        var response = JSON.parse(response);
        console.log(response);
        var result = document.getElementById("result");
        result.innerHTML = "この画像...「" + response["response"] + "」やんけ";
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
          // 通信が失敗した場合、エラーメッセージを出力する
        var result = document.getElementById("result");
        result.innerHTML = "サーバーとの通信が失敗した...";
      });
  });
});

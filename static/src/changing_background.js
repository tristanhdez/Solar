var d = new Date();
      var n = d.getHours();
      if (n > 19 || n < 6)
        $("body").css("background", "url('../images/wallpaper/wallpaper_dark.jpg')");
      else if (n > 16 && n < 19)
        $("body").css("background", "url('../images/wallpaper/wallpapers_light.jpg')");
      else
        $("body").css("background", "url('../images/wallpaper/wallpapers_light.jpg')");
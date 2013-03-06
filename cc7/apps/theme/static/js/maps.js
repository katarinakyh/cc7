    var initmap = function(){
        //jQuery(window).ready(function(){
        jQuery(window).ready(function(){
            gMapInit();
            jQuery("#watchPositionBtn").click(get_current_postion);
        });
    }
        function gMapInit(){
          var google_tile = "http://maps.google.com/maps/api/staticmap?sensor=false&center=-34.397,150.644&zoom=8&size=300x400"
          jQuery("#googleMap").html(
              jQuery(document.createElement("img")).attr("src", google_tile)
          );
        }
        var watchProcess = null;

        function get_current_postion() {
          if (watchProcess == null) {
              watchProcess = navigator.geolocation.getCurrentPosition(handle_geolocation_query, handle_errors);
          }
        }




        function handle_errors(error)
        {
            switch(error.code)
            {
                case error.PERMISSION_DENIED: alert("user did not share geolocation data");
                break;

                case error.POSITION_UNAVAILABLE: alert("could not detect current position");
                break;

                case error.TIMEOUT: alert("retrieving position timedout");
                break;

                default: alert("unknown error");
                break;
            }
        }

        function handle_geolocation_query(position) {
          var text = "latitude: "  + position.coords.latitude  + "<br/>" +
                     "longitude: " + position.coords.longitude + "<br/>" +
                     "timestamp: " + new Date(position.timestamp);
          jQuery("#APIReturnValues").html(text);
          jQuery("#APIReturnValues").css("border","3px solid green");

          var image_url = "http://maps.google.com/maps/api/staticmap?sensor=false&center=" + position.coords.latitude + ',' + position.coords.longitude +
                          "&zoom=14&size=300x400&markers=color:blue|label:S|" + position.coords.latitude + ',' + position.coords.longitude;
          
          jQuery("#googleMap").html(
              jQuery(document.createElement("img")).attr("src", image_url)
          );
        }

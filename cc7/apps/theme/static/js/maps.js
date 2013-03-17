    var initmap = function(){


        //jQuery(window).ready(function(){
        jQuery(window).ready(function(){
            gMapInit();
            jQuery("#watchPositionBtn").click(get_current_postion);
        });
    }
        function gMapInit(){
            var google_tile = "http://maps.google.com/maps/api/staticmap?sensor=false&center=Stockholm&zoom=9&size=300x400",
                lat = 44.88623409320778,
                lng = -87.86480712897173,
                latlng = new google.maps.LatLng(lat, lng),
                image = 'http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png';


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


        function moveMarker(placeName, latlng) {
            marker.setIcon(image);
            marker.setPosition(latlng);
            infowindow.setContent(placeName);
            //infowindow.open(map, marker);
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
          lat = position.coords.latitude;
          lng = position.coords.longitude;
          var text = "latitude: "  + lat  + "<br/>" +
                     "longitude: " + lng + "<br/>" +
                     "timestamp: " + new Date(position.timestamp);

            initialize_adress();
            codeLatLng(lat, lng);



            var image_url = "http://maps.google.com/maps/api/staticmap?sensor=false&center=" + position.coords.latitude + ',' + position.coords.longitude +
                          "&zoom=14&size=300x400&markers=color:blue|label:S|" + position.coords.latitude + ',' + position.coords.longitude;

   ;
          jQuery("#googleMap").html(
              jQuery(document.createElement("img")).attr("src", image_url)
          );
        }

        var i = 1;
        var more_posts = function(){
            if($(document).height() == $(window).scrollTop()+$(window).height()){
                if(i == 1){
                    i++;
                    $('.more_post').eq(0).trigger('click');
                }
            }
        }   

        $(function(){
            $(window).scroll(function(e){
                e.stopPropagation();
                more_posts();
            });
         });
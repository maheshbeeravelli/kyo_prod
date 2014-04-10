$(document).ready(function(){  
//Functions 
  $("a[data-key]").click(function() {
    key=$(this).attr("data-key");
    var title=$(this).parent().siblings(".item-title").text();
    $("#modal-title").text(title);
    var link = $(this).attr("data-link");
    $("#coupon-code").text($(this).attr("data-code"));
    $('#offer_modal').modal();
    $.ajax("/offer",{
            type: 'GET',
            data: {key:key},
            success: function(data,status){
            window.setTimeout(function(){
            },3000);
            window.open(link, '_blank');
    //        coupon = (data.coupon_code=="") ?  "NO CODE": data.coupon_code;
            },
             async: false
        });
     
   });

//DataManipulaters
  $(".posted_on" ).each(function( index ) {
      // console.log( index + ": " + $( this ).text() );
      var date=$(this).text();
      var posted_split = date.split(",");
      var posted_date =new Date(posted_split[0]+","+posted_split[1])
      var today=new Date();
      var timeDiff = Math.abs(today.getTime() - posted_date.getTime());
      var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); 
      diffDays--;
      if(diffDays>30)
      {
        var months = Math.ceil(diffDays/30);
        $( this ).text(months+ "months ago");
      }
      else if(diffDays>6)
      {
        weeks =diffDays/7;
        if(weeks<2){
          $( this ).text("1 week ago");
        }
        else{
          week=Math.ceil(weeks);
          $( this ).text(week + " weeks ago");
        }
      }
      else if(diffDays>1)
      {
        $( this ).text(diffDays+ " days ago");
      }
      else if (diffDays==1){
        $( this ).text("Yesterday");
      }
      else{
        $( this ).text("Today");
      }
  });
  
  $( ".expires-on" ).each(function( index ) {
      var date=$.trim($(this).text());
      var expiry_split = date.split(",");
      var expiry_date =new Date(expiry_split[0]+","+expiry_split[1]);
      var today=new Date();
      var timeDiff = Math.abs(today.getTime() - expiry_date.getTime());
      var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); 
      diffDays;
      if(date=="Nov. 1, 1991")
      {
        $( this ).text("No Expiry Date");
      }
      if(diffDays==7)
      {
        $( this ).text("1 week left");
      }
      else if (diffDays==1){
        $( this ).text("1 day left");
      }
      else if(diffDays==0){
        $(this).text("Last Day");
      }
      else if(diffDays<0)
      {
        $(this).text("Expired");
      }
      
  });
  $(".contactus").click(function(){
      $("#contactus_modal").modal();
  });
  $("#mobile-search").focus(function(){
    $("#mobile-nav li").hide();
  });
  
  $("#mobile-search").blur(function(){
    $("#mobile-nav li").show();
  });
  
  $("#contactus_send").click(function(){
    $(this).addClass("btn-primary");
    $(this).text("Sending..");
    data = {contact_us:$("#contactus_name").val(), contactus_email:$("#contactus_email").val(),contactus_desc:$("#contactus_desc").val()};
    $.post( "/contactus", data).done(function( data ) {
      $("#contactus_send").removeClass("btn-primary");
      $("#contactus_send").addClass("btn-success");
      $("#contactus_send").text("Successfully Submited");
      window.setTimeout(function(){
        $("#contactus_send").removeClass("btn-success");
        $("#contactus_send").addClass("btn-default");
        $("#contactus_modal").modal('hide');
        $("#contactus_send").text("Send");
      },3000);
    });
  });// End of Contactus_send
});
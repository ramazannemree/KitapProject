$(document).ready(function(){
    $('#id_phone').mask('500-000-0000');
    var ilpost = $('#il_div').text();
    var ilcepost = $('#ilce_div').text();
    console.log("ilpost"+ilpost);

    $('#id_ilce').attr('disabled', 'disabled');
    $('#id_ilce').append("<option value=''> İlçe Seçiniz </option>");
    $('#id_il').append("<option value=''> İl Seçiniz </option>");
    $.getJSON("../../static/js/kullanici/il-bolge.json", function(sonuc){

        $.each(sonuc, function(index, value){
            var row="";
            console.log("zxcxc"+value.il);
                if(value.il==ilpost){
                    row +='<option selected value="'+value.il+'">'+value.il+'</option>';
                    $("#id_il").append(row);
                    console.log(ilcepost);

                        console.log(ilcepost);
                        $("#id_ilce").attr("disabled", false).html("<option value=''>İlçe Seçiniz</option>");
                                $.getJSON("../../static/js/kullanici/il-ilce.json", function(sonuc){
                                    $.each(sonuc, function(index, valuee){
                                        var row="";
                                        if(valuee.il==ilpost)
                                        {
                                            if(valuee.ilce==ilcepost){
                                                row +='<option selected value="'+valuee.ilce+'">'+valuee.ilce+'</option>';
                                                $("#id_ilce").append(row);
                                            }
                                            row +='<option value="'+valuee.ilce+'">'+valuee.ilce+'</option>';
                                            $("#id_ilce").append(row);
                                        }
                                    });
                                });

                }

                row +='<option value="'+value.il+'">'+value.il+'</option>';
                $("#id_il").append(row);


        })
});
console.log("angara");
$("#id_il").on("change", function(){
    var il=$(this).val();
    $("#id_ilce").attr("disabled", false).html("<option value=''>İlçe Seçiniz</option>");
    $.getJSON("../../static/js/kullanici/il-ilce.json", function(sonuc){
        $.each(sonuc, function(index, value){
            var row="";
            if(value.il==il)
            {
                row +='<option value="'+value.ilce+'">'+value.ilce+'</option>';
                $("#id_ilce").append(row);
            }
        });
    });
});

});
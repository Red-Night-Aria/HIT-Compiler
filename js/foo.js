function foo(e){
    fileName = e.files[0].name
    if (fileName.length>23){
        fileName = fileName.substring(0, 15) + "..." + fileName.substring(fileName.length-8)
    }
    $('head').append("<style>#fileLabel::after{ content: \""+ fileName + "\"!important }</style>");
}

function analyze(){
    reader = new FileReader()
    reader.onload = function(e){
        data = {
            'code': $('#input_area').val(),
            'rule': e.target.result
        }

        $.post('LifeIsSoHard', data, function(rData, status){
            splitstr = ""
            for (var i=0;i<50;i++){
                splitstr += '-'
            }
            splitstr += '\n'
            result = rData.split(splitstr)
            $('#token').val(result[0])
            $('#first').val(result[1])
            $('#follow').val(result[2])
            $('#predict').val(result[3])
            $('#code').val(result[4])
            $('#symbol').val(result[5])
            $('#tree').val(result[6])
        });
    }
    reader.readAsText($('#file')[0].files[0])
}
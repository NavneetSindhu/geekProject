$(document).ready(function () {
    $('.image-section').hide();
    $('.loader').hide();
    $('#result-card').hide();

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide().fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result-card').hide();
        readURL(this);
    });

    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).hide();
        $('.loader').show();

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (response) {
                $('.loader').hide();
                $('#result-card').fadeIn(600);

                $('#disease-name').text("Disease Detected: " + response.disease);
                $('#confidence').text("Confidence: " + response.confidence + "%");
                $('#advice').text(response.advice);

                console.log('Prediction Success!');
            },
            error: function (error) {
                $('.loader').hide();
                alert("An error occurred during prediction.");
                console.log('Error:', error);
            }
        });
    });
});
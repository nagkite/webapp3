$(document).ready(function() {
  $("#logFileForm").on("submit", function(e) {
      e.preventDefault();
      analyzeLogFile();
  });
});

function analyzeLogFile() {
  var file = $('#logFile')[0].files[0];
  var formData = new FormData();
  formData.append('logFile', file);

  $.ajax({
      url: "/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
          $("#analysisResults").html(JSON.stringify(response, null, 4));  // Display the JSON result

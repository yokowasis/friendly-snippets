<?php

$apiEndpoint = 'https://example.com/api';

// Data to be sent in JSON format
$data = array(
  'key1' => 'value1',
  'key2' => 'value2'
);

// Convert data to JSON format
$jsonData = json_encode($data);

// Initialize cURL session
$ch = curl_init($apiEndpoint);

// Set cURL options
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
  'Content-Type: application/json',
  'Content-Length: ' . strlen($jsonData)
));

// Execute cURL session and get the response
$response = curl_exec($ch);

// Check for cURL errors
if (curl_errno($ch)) {
  echo 'Curl error: ' . curl_error($ch);
}

// Close cURL session
curl_close($ch);

// Process the response
echo $response;
